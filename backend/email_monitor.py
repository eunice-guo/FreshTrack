"""
Email monitoring service for receiving receipt images
Monitors specified email account and processes incoming receipt images
"""
import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
import logging

from ocr_service import ReceiptOCRService
from models import User, FoodItem, FoodShelfLife
from database import SessionLocal


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailMonitorService:
    """Service for monitoring email inbox and processing receipt images"""

    def __init__(self, email_address: str, password: str, imap_server: str = "imap.gmail.com"):
        """
        Initialize email monitor service

        Args:
            email_address: Email address to monitor (e.g., receipt@freshtrack.app)
            password: Email password or app-specific password
            imap_server: IMAP server address
        """
        self.email_address = email_address
        self.password = password
        self.imap_server = imap_server
        self.ocr_service = ReceiptOCRService()
        self.scheduler = BackgroundScheduler()

    def connect_to_mailbox(self) -> imaplib.IMAP4_SSL:
        """
        Connect to email server using IMAP

        Returns:
            IMAP connection object
        """
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email_address, self.password)
            logger.info(f"✅ Connected to {self.email_address}")
            return mail
        except Exception as e:
            logger.error(f"❌ Failed to connect to email: {str(e)}")
            raise

    def get_user_by_email(self, sender_email: str, db: Session) -> Optional[User]:
        """
        Get user from database by email address

        Args:
            sender_email: Sender's email address
            db: Database session

        Returns:
            User object or None
        """
        user = db.query(User).filter(User.email == sender_email).first()
        return user

    def extract_sender_email(self, from_header: str) -> str:
        """
        Extract email address from 'From' header

        Args:
            from_header: Raw 'From' header (e.g., "John Doe <john@example.com>")

        Returns:
            Email address
        """
        import re
        match = re.search(r'<(.+?)>', from_header)
        if match:
            return match.group(1)
        return from_header

    def process_email_attachments(self, msg, user_id: int, db: Session) -> int:
        """
        Process image attachments from email

        Args:
            msg: Email message object
            user_id: User ID
            db: Database session

        Returns:
            Number of items added
        """
        items_added = 0

        for part in msg.walk():
            # Check if attachment is an image
            content_type = part.get_content_type()
            if content_type in ['image/jpeg', 'image/png', 'image/jpg']:
                filename = part.get_filename()

                if filename:
                    # Save image temporarily
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    temp_path = f"./temp_receipts/{user_id}_{timestamp}_{filename}"

                    # Create temp directory if not exists
                    os.makedirs("./temp_receipts", exist_ok=True)

                    # Save attachment
                    with open(temp_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    logger.info(f"📸 Saved receipt image: {temp_path}")

                    try:
                        # Process with OCR
                        items = self.ocr_service.process_receipt_image(temp_path)

                        # Save items to database
                        for item_data in items:
                            # Get shelf life info
                            shelf_life_days = self.get_shelf_life(
                                item_data['name'],
                                item_data['category'],
                                db
                            )

                            # Calculate expiration date
                            purchase_date = datetime.now()
                            expiration_date = purchase_date + timedelta(days=shelf_life_days)

                            # Create food item
                            food_item = FoodItem(
                                user_id=user_id,
                                food_name=item_data['name'],
                                category=item_data['category'],
                                purchase_date=purchase_date,
                                expiration_date=expiration_date,
                                quantity=item_data['quantity'],
                                price=item_data['total_price']
                            )

                            db.add(food_item)
                            items_added += 1

                        db.commit()
                        logger.info(f"✅ Added {len(items)} items to database")

                    except Exception as e:
                        logger.error(f"❌ Error processing receipt: {str(e)}")
                        db.rollback()

                    finally:
                        # Clean up temp file
                        if os.path.exists(temp_path):
                            os.remove(temp_path)

        return items_added

    def get_shelf_life(self, food_name: str, category: str, db: Session) -> int:
        """
        Get shelf life for a food item from database

        Args:
            food_name: Name of food item
            category: Food category
            db: Database session

        Returns:
            Shelf life in days (defaults to 7 if not found)
        """
        # Try to find exact match
        shelf_life = db.query(FoodShelfLife).filter(
            FoodShelfLife.food_name_cn.ilike(f"%{food_name}%")
        ).first()

        if shelf_life and shelf_life.refrigerator_max:
            return shelf_life.refrigerator_max

        # Default shelf life by category
        default_shelf_life = {
            '乳制品': 7,      # 1 week
            '蔬菜': 5,        # 5 days
            '水果': 7,        # 1 week
            '肉类': 3,        # 3 days
            '蛋类': 21,       # 3 weeks
            '调味品': 180,    # 6 months
            '其他': 7         # 1 week default
        }

        return default_shelf_life.get(category, 7)

    def check_new_emails(self):
        """
        Check for new unread emails and process them
        This method is called periodically by the scheduler
        """
        logger.info("🔍 Checking for new receipt emails...")

        db = SessionLocal()

        try:
            mail = self.connect_to_mailbox()
            mail.select("inbox")

            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')

            if status != "OK":
                logger.warning("Failed to search emails")
                return

            email_ids = messages[0].split()

            if not email_ids:
                logger.info("No new emails found")
                return

            logger.info(f"📧 Found {len(email_ids)} new email(s)")

            for email_id in email_ids:
                try:
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    msg = email.message_from_bytes(msg_data[0][1])

                    # Get sender
                    from_header = msg.get('From', '')
                    sender_email = self.extract_sender_email(from_header)

                    logger.info(f"📨 Processing email from: {sender_email}")

                    # Find or create user
                    user = self.get_user_by_email(sender_email, db)

                    if not user:
                        # Auto-register new user
                        user = User(email=sender_email)
                        db.add(user)
                        db.commit()
                        db.refresh(user)
                        logger.info(f"👤 Created new user: {sender_email}")

                    # Process attachments
                    items_added = self.process_email_attachments(msg, user.id, db)

                    if items_added > 0:
                        logger.info(f"✅ Added {items_added} items for user {user.email}")
                        # TODO: Send push notification to user
                        # send_notification(user.id, f"已添加 {items_added} 件食材")

                except Exception as e:
                    logger.error(f"❌ Error processing email {email_id}: {str(e)}")
                    continue

            mail.logout()

        except Exception as e:
            logger.error(f"❌ Error in check_new_emails: {str(e)}")

        finally:
            db.close()

    def start_monitoring(self, interval_minutes: int = 5):
        """
        Start background monitoring of email inbox

        Args:
            interval_minutes: Check interval in minutes (default: 5)
        """
        logger.info(f"🚀 Starting email monitor (checking every {interval_minutes} minutes)")

        # Schedule periodic checks
        self.scheduler.add_job(
            self.check_new_emails,
            'interval',
            minutes=interval_minutes,
            id='email_check_job'
        )

        # Run initial check
        self.check_new_emails()

        # Start scheduler
        self.scheduler.start()

        logger.info("✅ Email monitoring started successfully!")

    def stop_monitoring(self):
        """Stop email monitoring"""
        self.scheduler.shutdown()
        logger.info("⏹️  Email monitoring stopped")


# Example usage
if __name__ == "__main__":
    # Load credentials from environment variables
    import os
    from dotenv import load_dotenv

    load_dotenv()

    EMAIL_ADDRESS = os.getenv("RECEIPT_EMAIL_ADDRESS", "receipt@freshtrack.app")
    EMAIL_PASSWORD = os.getenv("RECEIPT_EMAIL_PASSWORD", "")

    if not EMAIL_PASSWORD:
        print("❌ Please set RECEIPT_EMAIL_PASSWORD environment variable")
        exit(1)

    # Create and start monitor
    monitor = EmailMonitorService(EMAIL_ADDRESS, EMAIL_PASSWORD)
    monitor.start_monitoring(interval_minutes=5)

    # Keep running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        monitor.stop_monitoring()
        print("\n👋 Email monitor stopped")
