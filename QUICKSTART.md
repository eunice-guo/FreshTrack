# 🚀 FreshTrack Quick Start Guide

## You're All Set Up! 🎉

Your FreshTrack application is **fully configured and running** with demo data!

---

## ✅ What's Already Done

- ✅ Python virtual environment created
- ✅ All dependencies installed
- ✅ Database initialized with 24 food shelf-life standards
- ✅ Demo user created: `demo@freshtrack.app` (ID: 1)
- ✅ 10 sample food items in your fridge
- ✅ 5 sample recipes added
- ✅ API server running on http://localhost:8000

---

## 🎯 How to Use FreshTrack

### 1. **Access the Interactive API Documentation**

The FastAPI server is currently running in the background.

Open your browser and visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

---

### 2. **Try the API Endpoints**

Your demo user ID is: **1**

#### Get All Items in Fridge
```
GET http://localhost:8000/api/items/1
```

#### Get Items Expiring Soon
```
GET http://localhost:8000/api/items/expiring/1?days=3
```

#### Get Recipe Recommendations
```
GET http://localhost:8000/api/recipes/recommend/1?limit=5
```

#### Get Statistics
```
GET http://localhost:8000/api/stats/1
```

#### Add New Food Item
```
POST http://localhost:8000/api/items/1
Content-Type: application/json

{
  "food_name": "香蕉",
  "category": "水果",
  "quantity": 5,
  "quantity_unit": "根",
  "expiration_date": "2025-11-13T00:00:00"
}
```

---

### 3. **Run the Test Script**

We've created a comprehensive test script that demonstrates all features:

```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/python test_api.py
```

This will:
- Check all API endpoints
- Display your fridge inventory
- Show recipe recommendations
- Add a sample item (草莓 - strawberry)
- Add item to shopping list

---

### 4. **View Your Current Fridge Status**

Run the demo script again to see a summary:

```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/python demo.py
```

This shows:
- Items expiring today or soon
- Recipe recommendations based on available ingredients
- Statistics by category

---

## 🎮 Current Demo Data

### Your Demo User
- **Email**: demo@freshtrack.app
- **User ID**: 1

### Your Fridge Contains
1. 🥛 牛奶 (Milk) - **EXPIRED** ❌
2. 🧈 酸奶 (Yogurt) - Expiring TODAY ⚠️
3. 🥦 西兰花 (Broccoli) - 1 day left 🟡
4. 🍅 番茄 (Tomato) - 2 days left 🟡
5. 🥚 鸡蛋 (Eggs) - 2 days left 🟡
6. 🍗 鸡肉 (Chicken) - 4 days left 🟢
7. 🍎 苹果 (Apple) - 9 days left ✅
8. 🥔 土豆 (Potato) - 13 days left ✅
9. 🍚 大米 (Rice) - 59 days left ✅
10. 🍾 酱油 (Soy Sauce) - 179 days left ✅

### Available Recipes
1. 番茄炒蛋 (Tomato Scrambled Eggs)
2. 清炒西兰花 (Stir-fried Broccoli)
3. 宫保鸡丁 (Kung Pao Chicken)
4. 炒土豆丝 (Potato Stir-fry)
5. 苹果酸奶碗 (Apple Yogurt Bowl)

---

## 🛠️ Server Management

### Start the Server
```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/python main.py
```

### Stop the Server
Press `Ctrl+C` in the terminal where the server is running.

### Check if Server is Running
```bash
curl http://localhost:8000/
```

Or open http://localhost:8000/ in your browser.

---

## 📱 Next Steps

### Option 1: Use the API Directly
You can now build a mobile app, web frontend, or any client that connects to:
```
http://localhost:8000
```

All endpoints are documented at http://localhost:8000/docs

### Option 2: Add More Data

#### Add More Food Items
```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/python -c "
from database import SessionLocal
from models import FoodItem
from datetime import datetime, timedelta

db = SessionLocal()
item = FoodItem(
    user_id=1,
    food_name='香蕉',
    category='水果',
    quantity=5,
    quantity_unit='根',
    purchase_date=datetime.now(),
    expiration_date=datetime.now() + timedelta(days=5)
)
db.add(item)
db.commit()
print('✅ Added 香蕉 to fridge!')
"
```

#### Add More Recipes
Edit `backend/demo.py` and add recipes to the `sample_recipes` list.

### Option 3: Set Up Email Receipt Scanning

1. Create a Gmail app-specific password:
   - Enable 2-Factor Authentication
   - Go to: https://myaccount.google.com/apppasswords
   - Generate password for "Mail"

2. Create `.env` file:
```bash
cd ~/Documents/FreshTrack/backend
cp .env.example .env
```

3. Edit `.env` and add:
```env
RECEIPT_EMAIL_ADDRESS=your-email@gmail.com
RECEIPT_EMAIL_PASSWORD=your_app_password_here
IMAP_SERVER=imap.gmail.com
```

4. Run email monitor:
```bash
venv/Scripts/python email_monitor.py
```

Now you can forward receipt photos to your email, and they'll be automatically processed!

---

## 📚 Learn More

- **Full README**: See `README.md` for complete documentation
- **API Docs**: http://localhost:8000/docs
- **Code Structure**: Explore the `backend/` folder
- **Database**: Located at `backend/data/freshtrack.db`

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Kill the process if needed
taskkill /PID <process_id> /F

# Restart server
cd ~/Documents/FreshTrack/backend
venv/Scripts/python main.py
```

### Database errors
```bash
# Reset database
cd ~/Documents/FreshTrack/backend
rm data/freshtrack.db
venv/Scripts/python init_sample_data.py
venv/Scripts/python demo.py
```

### Missing dependencies
```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/pip install -r requirements.txt
```

---

## 🎉 You're Ready to Go!

FreshTrack is now running on your system with:
- ✅ Working API server
- ✅ Sample data
- ✅ Test scripts
- ✅ Full documentation

**Start exploring at**: http://localhost:8000/docs

Happy food tracking! 🧊🍎🥗
