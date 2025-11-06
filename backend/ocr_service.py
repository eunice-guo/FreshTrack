"""
OCR Service for processing receipt images
Uses Tesseract OCR + OpenCV for image preprocessing
"""
import cv2
import pytesseract
import re
from typing import List, Dict
from datetime import datetime
import numpy as np


class ReceiptOCRService:
    """Service for processing receipt images and extracting food items"""

    def __init__(self):
        # Configure Tesseract path if needed (Windows)
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pass

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess receipt image for better OCR accuracy

        Args:
            image_path: Path to the receipt image

        Returns:
            Preprocessed image as numpy array
        """
        # Read image
        img = cv2.imread(image_path)

        if img is None:
            raise ValueError(f"Could not read image from {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)

        # Apply thresholding (binary)
        thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Dilation and erosion to remove noise
        kernel = np.ones((1, 1), np.uint8)
        processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

        return processed

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from receipt image using OCR

        Args:
            image_path: Path to the receipt image

        Returns:
            Extracted text as string
        """
        # Preprocess image
        processed_img = self.preprocess_image(image_path)

        # Configure OCR (PSM 6 = single uniform block of text)
        custom_config = r'--oem 3 --psm 6'

        # Perform OCR with Chinese and English support
        text = pytesseract.image_to_string(
            processed_img,
            lang='chi_sim+eng',
            config=custom_config
        )

        return text

    def parse_receipt_text(self, text: str) -> List[Dict]:
        """
        Parse OCR text and extract structured food items

        Args:
            text: Raw OCR text from receipt

        Returns:
            List of dictionaries containing item information
        """
        items = []
        lines = text.split('\n')

        # Regex patterns for common receipt formats
        # Pattern 1: Item name followed by price (e.g., "牛奶 15.90")
        pattern1 = r'([^0-9\n]+?)\s+(\d+\.?\d*)'

        # Pattern 2: Quantity x Item name x Unit price = Total (e.g., "2 x 牛奶 x 7.95 = 15.90")
        pattern2 = r'(\d+)\s*[xX×]\s*([^x×\d]+?)\s*[xX×]\s*(\d+\.?\d*)\s*=\s*(\d+\.?\d*)'

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Try pattern 2 first (more specific)
            match2 = re.search(pattern2, line)
            if match2:
                quantity = int(match2.group(1))
                name = match2.group(2).strip()
                unit_price = float(match2.group(3))
                total_price = float(match2.group(4))

                items.append({
                    'name': name,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total_price': total_price,
                    'category': self._classify_item(name)
                })
                continue

            # Try pattern 1
            match1 = re.search(pattern1, line)
            if match1:
                name = match1.group(1).strip()
                price = float(match1.group(2))

                # Filter out common non-item entries
                if self._is_likely_food_item(name):
                    items.append({
                        'name': name,
                        'quantity': 1,
                        'unit_price': price,
                        'total_price': price,
                        'category': self._classify_item(name)
                    })

        return items

    def _is_likely_food_item(self, text: str) -> bool:
        """
        Filter out non-food items (like "total", "cash", etc.)
        """
        # Exclude common receipt keywords
        exclude_keywords = [
            'total', 'subtotal', 'tax', 'cash', 'change', 'receipt',
            '小计', '总计', '合计', '现金', '找零', '***', '---',
            'thank', 'welcome', '欢迎', '谢谢'
        ]

        text_lower = text.lower()
        for keyword in exclude_keywords:
            if keyword in text_lower:
                return False

        # Must have at least 2 characters
        if len(text.strip()) < 2:
            return False

        return True

    def _classify_item(self, name: str) -> str:
        """
        Simple keyword-based classification of food items
        This is a basic implementation - can be enhanced with ML later
        """
        name_lower = name.lower()

        # Dairy products
        if any(kw in name_lower for kw in ['牛奶', 'milk', '酸奶', 'yogurt', '奶酪', 'cheese', '黄油', 'butter']):
            return '乳制品'

        # Vegetables
        if any(kw in name_lower for kw in ['菜', '白菜', '西兰花', '番茄', '土豆', '萝卜', 'vegetable', 'lettuce', 'tomato']):
            return '蔬菜'

        # Fruits
        if any(kw in name_lower for kw in ['苹果', '香蕉', '橙', '梨', '葡萄', 'apple', 'banana', 'orange', 'grape']):
            return '水果'

        # Meat
        if any(kw in name_lower for kw in ['肉', '鸡', '猪', '牛', '鱼', 'meat', 'chicken', 'pork', 'beef', 'fish']):
            return '肉类'

        # Eggs
        if any(kw in name_lower for kw in ['蛋', 'egg']):
            return '蛋类'

        # Condiments
        if any(kw in name_lower for kw in ['酱油', '盐', '糖', '醋', '油', 'sauce', 'salt', 'sugar', 'oil']):
            return '调味品'

        # Default category
        return '其他'

    def process_receipt_image(self, image_path: str) -> List[Dict]:
        """
        Main method to process a receipt image and extract items

        Args:
            image_path: Path to the receipt image file

        Returns:
            List of extracted food items with structured data
        """
        try:
            # Extract text
            text = self.extract_text_from_image(image_path)

            print(f"📄 Extracted text from receipt:")
            print(text)
            print("\n" + "="*50 + "\n")

            # Parse items
            items = self.parse_receipt_text(text)

            print(f"✅ Found {len(items)} items:")
            for item in items:
                print(f"  - {item['name']} | {item['category']} | ¥{item['total_price']}")

            return items

        except Exception as e:
            print(f"❌ Error processing receipt: {str(e)}")
            raise


# Example usage
if __name__ == "__main__":
    service = ReceiptOCRService()

    # Test with a sample receipt image
    # items = service.process_receipt_image("sample_receipt.jpg")
    # print(f"Processed {len(items)} items")
