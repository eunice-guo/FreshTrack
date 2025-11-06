# 🧊 FreshTrack (鲜食追踪)

> **让冰箱里的每一样食材都物尽其用**
> Smart food inventory management to reduce waste

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com/)

## 📋 产品概述 (Product Overview)

**FreshTrack** is a smart food tracking application that helps you:

- ✅ **Track food inventory** automatically via receipt scanning
- ⏰ **Get expiration reminders** before food goes bad
- 🍳 **Discover recipes** based on available ingredients
- 🛒 **Manage shopping lists** intelligently
- 🌱 **Reduce food waste** and save money

### 🎯 Core Features

1. **📸 Receipt OCR** - Forward receipt photos via email, auto-extract food items
2. **🧊 Fridge Management** - Track all items with expiration dates
3. **🔔 Smart Reminders** - Get notified when food is about to expire
4. **👨‍🍳 Recipe Recommendations** - Match recipes to your available ingredients
5. **📝 Shopping List** - Auto-generate lists based on missing ingredients

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Tesseract OCR installed
- Gmail account (for receipt forwarding)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/FreshTrack.git
cd FreshTrack/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# macOS: brew install tesseract tesseract-lang
# Ubuntu: sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

# Set up environment variables
cp .env.example .env
# Edit .env with your email credentials

# Initialize database with sample data
python init_sample_data.py

# Run the API server
python main.py
```

The API will be available at `http://localhost:8000`

Visit `http://localhost:8000/docs` for interactive API documentation.

---

## 📁 Project Structure

```
FreshTrack/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Database models
│   ├── database.py             # Database configuration
│   ├── ocr_service.py          # Receipt OCR processing
│   ├── email_monitor.py        # Email monitoring service
│   ├── init_sample_data.py     # Sample data initialization
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example            # Environment variables template
│   └── data/
│       └── freshtrack.db       # SQLite database
├── mobile_app/                 # (Coming soon) Flutter mobile app
├── .gitignore
└── README.md
```

---

## 🔌 API Endpoints

### Users

- `POST /api/users/register` - Register new user
- `GET /api/users/{user_id}` - Get user by ID
- `GET /api/users/email/{email}` - Get user by email

### Food Items

- `GET /api/items/{user_id}` - Get all food items
- `GET /api/items/expiring/{user_id}?days=3` - Get items expiring soon
- `POST /api/items/{user_id}` - Manually add food item
- `PUT /api/items/consume/{item_id}` - Mark item as consumed
- `DELETE /api/items/{item_id}` - Delete item

### Recipes

- `GET /api/recipes/recommend/{user_id}?limit=5` - Get recipe recommendations

### Shopping List

- `GET /api/shopping/{user_id}` - Get shopping list
- `POST /api/shopping/{user_id}` - Add to shopping list
- `PUT /api/shopping/purchase/{item_id}` - Mark as purchased

### Statistics

- `GET /api/stats/{user_id}` - Get inventory statistics

---

## 💡 How It Works

### 1. Receipt Scanning Flow

```
📱 Take photo of receipt
    ↓
📧 Forward to receipt@freshtrack.app
    ↓
🤖 OCR extracts items
    ↓
🗄️  Items saved to database
    ↓
📲 Push notification: "Added 8 items"
```

### 2. Expiration Tracking

- Items are automatically assigned shelf life based on category
- Smart reminders sent:
  - 2 days before expiration
  - Day of expiration (morning)
  - Evening recipe suggestions

### 3. Recipe Matching

```python
# Match algorithm
match_rate = (available_ingredients / required_ingredients) × 100%

# Boost score for urgent items
if uses_expiring_food:
    score × 1.5
```

---

## 🛠️ Technology Stack

| Component | Technology | Why? |
|-----------|-----------|------|
| **Backend** | FastAPI | Fast, modern, async Python framework |
| **Database** | SQLite → PostgreSQL | Simple start, scalable later |
| **OCR** | Tesseract + OpenCV | Open-source, 85%+ accuracy |
| **Email** | IMAP | Standard email protocol |
| **Mobile** | Flutter (planned) | Cross-platform iOS/Android |

---

## 📊 Database Schema

### `users`
- id, email, username, created_at

### `food_items`
- id, user_id, food_name, category, purchase_date, expiration_date, quantity, is_consumed

### `food_shelf_life`
- id, food_name, food_name_cn, category, refrigerator_min/max, freezer_min/max, tips

### `recipes`
- id, name, name_cn, category, ingredients, instructions, prep_time, cook_time

### `shopping_list`
- id, user_id, item_name, quantity, is_purchased, reason

---

## 🔐 Configuration

Create a `.env` file based on `.env.example`:

```env
# Email for receiving receipts
RECEIPT_EMAIL_ADDRESS=receipt@freshtrack.app
RECEIPT_EMAIL_PASSWORD=your_app_password_here
IMAP_SERVER=imap.gmail.com

# Database
DATABASE_URL=sqlite:///./data/freshtrack.db

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True
```

### Setting up Gmail for Receipt Forwarding

1. Enable 2-Factor Authentication in Gmail
2. Generate App-Specific Password:
   - Go to Google Account → Security → App Passwords
   - Generate password for "Mail"
3. Use this password in `.env`

---

## 🧪 Testing

```bash
# Test OCR service
python ocr_service.py

# Test email monitoring
python email_monitor.py

# Run API server with auto-reload
uvicorn main:app --reload

# Access interactive API docs
open http://localhost:8000/docs
```

---

## 📱 Mobile App (Coming Soon)

The Flutter mobile app is planned with features:

- 📊 Dashboard with expiring items
- 🔔 Push notifications
- 📸 In-app receipt scanning
- 🍳 Recipe browsing
- 🛒 Shopping list management

---

## 🗺️ Roadmap

### MVP (v1.0) - Current
- [x] Receipt OCR
- [x] Food inventory tracking
- [x] Expiration reminders
- [x] Recipe recommendations
- [x] Shopping list

### Future (v2.0+)
- [ ] Mobile app (Flutter)
- [ ] Barcode scanning
- [ ] Nutrition tracking
- [ ] Meal planning
- [ ] Waste analytics
- [ ] Social features (share recipes)
- [ ] ML-powered OCR improvements

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [USDA FoodKeeper Data](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/foodkeeper-app) - Food shelf life database
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Open-source OCR engine
- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [TheMealDB](https://www.themealdb.com/) - Recipe API

---

## 📞 Contact

**Project Link:** [https://github.com/yourusername/FreshTrack](https://github.com/yourusername/FreshTrack)

**Email:** contact@freshtrack.app

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

Made with ❤️ to reduce food waste
