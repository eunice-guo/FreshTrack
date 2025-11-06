# 🌐 FreshTrack Web Interface - Complete User Guide

Welcome to FreshTrack! This guide will help you get started with the web interface.

---

## 🚀 Getting Started (2 Steps)

### Step 1: Start the API Server

```bash
cd C:\Users\egeun\Documents\FreshTrack\backend
venv\Scripts\python main.py
```

**You should see:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

✅ Leave this window open! The API server must keep running.

### Step 2: Open the Web Interface

**Option A: Double-click**
1. Navigate to `C:\Users\egeun\Documents\FreshTrack\web`
2. Double-click `index.html`

**Option B: Command line**
```bash
cd C:\Users\egeun\Documents\FreshTrack\web
start index.html
```

The web interface will open in your default browser!

---

## 📊 Using the Dashboard

The Dashboard gives you a quick overview of your fridge status.

### What You'll See:

**Statistics Cards:**
- 📦 **Total Items** - All food in your fridge
- ⚠️ **Expiring Today** - Items that expire today
- 🟡 **Expiring Soon** - Items expiring within 3 days
- ✅ **Fresh Items** - Items with 7+ days remaining

**Urgent Alerts:**
If you have items expiring today or soon, you'll see an orange alert box listing them.

**Category Chart:**
Visual breakdown showing how many items you have in each category (蔬菜, 水果, 肉类, etc.)

### Actions:
- Click **🔄 刷新** to reload all data from the server

---

## 🧊 Managing Your Fridge

Click "🧊 我的冰箱" in the navigation to view all your food items.

### Understanding the Color Codes:

| Color | Status | Meaning |
|-------|--------|---------|
| ❌ Red | Expired | Already past expiration date |
| ⚠️ Orange | Today | Expires today - eat ASAP! |
| 🟡 Yellow | Urgent | 1-3 days left |
| 🟢 Green | Warning | 4-7 days left |
| ✅ Blue | Fresh | 7+ days remaining |

### Filter Your Items:

- **全部** (All) - Show everything
- **紧急** (Urgent) - Only expired, today, or 1-3 days
- **新鲜** (Fresh) - Only items with 4+ days

### Actions on Each Item:

**✅ 已吃完** (Mark as Consumed)
- Click when you've finished eating the item
- Item will be removed from your fridge
- Helps track consumption patterns

**🗑️ 删除** (Delete)
- Permanently removes the item
- Use if you threw it away or made a mistake

---

## 🍳 Recipe Recommendations

Click "🍳 食谱推荐" to see recipes you can make with your current ingredients!

### How It Works:

The system analyzes your fridge and recommends recipes based on:
1. **Match Percentage** - How many ingredients you already have
2. **Urgency** - Recipes using items about to expire get priority

### Recipe Card Information:

**Match Bar:**
- Green bar shows percentage of ingredients you have
- Higher percentage = easier to make now

**Status Indicators:**
- ✅ **All ingredients available** - You can make this right now!
- ⚠️ **Missing ingredients** - Shows what you need to buy

**Recipe Details:**
- ⏱️ **Cooking time** - Total prep + cook time
- 🍽️ **Category** - Type of dish (中式家常菜, 健康早餐, etc.)

### Quick Actions:

**🛒 Add Missing Ingredients to Shopping List**
- Click this button on any recipe
- All missing ingredients are added to your shopping list
- Each item notes which recipe needs it

---

## 🛒 Shopping List

Click "🛒 购物清单" to manage items you need to buy.

### Two Sections:

**待购买 (To Buy):**
- Items you still need to purchase
- Check the checkbox when bought
- Items automatically move to "已购买"

**已购买 (Purchased):**
- Items you've already bought
- Greyed out and crossed through
- Keeps a record of your shopping

### Adding Items:

1. Click **➕ 添加商品** button
2. Fill in the form:
   - **商品名称** - What to buy (e.g., 蜂蜜)
   - **数量** - How many (e.g., 1)
   - **单位** - Unit (e.g., 瓶)
   - **原因** - Why you need it (optional, e.g., "做苹果酸奶碗需要")
3. Click **添加** to save

### Tips:

- The "原因" (reason) field helps you remember why you added each item
- Items added from recipes automatically include the recipe name as the reason
- Check items off as you shop to track what's left

---

## ➕ Adding Food Items

Click "➕ 添加食材" to manually add items to your fridge.

### Form Fields:

**食材名称 (Food Name)** *Required*
- What you bought (e.g., 西红柿, 鸡蛋, 牛奶)

**分类 (Category)** *Required*
- Choose from dropdown:
  - 🥬 蔬菜 (Vegetables)
  - 🍎 水果 (Fruits)
  - 🍗 肉类 (Meat)
  - 🥛 乳制品 (Dairy)
  - 🥚 蛋类 (Eggs)
  - 🍚 主食 (Staples)
  - 🧂 调味品 (Condiments)
  - 🥢 豆制品 (Tofu products)
  - 📦 其他 (Other)

**数量 (Quantity)** *Required*
- How many you have (e.g., 3)

**单位 (Unit)** *Required*
- Choose from dropdown: 个, 斤, 瓶, 袋, 盒, 根, 颗

**到期日期 (Expiration Date)** *Required*
- When the item expires
- Defaults to 7 days from today
- Click to open date picker

**价格 (Price)** Optional
- How much you paid (e.g., 15.90)
- Used for future analytics

### After Submitting:

- You'll see a success message: "食材已添加！"
- Form resets for easy multiple entries
- If you're on the Dashboard or Fridge page, it automatically refreshes

---

## 💡 Tips & Best Practices

### Daily Routine:

**Morning:**
1. Check Dashboard for items expiring today
2. Plan meals around urgent items
3. Check Recipe Recommendations

**After Shopping:**
1. Add new items via "➕ 添加食材"
2. Update quantities if you bought more of existing items

**When Cooking:**
1. Check Recipes for what you can make
2. Mark ingredients as consumed after cooking

**Weekly:**
1. Review what's expiring in next 7 days
2. Add missing ingredients to shopping list
3. Plan weekly meals

### Keyboard Shortcuts:

While there are no built-in keyboard shortcuts, you can:
- Use **Tab** to navigate between form fields
- Press **Enter** to submit forms
- Use your browser's refresh (F5) if something doesn't load

### Troubleshooting:

**"加载数据失败" (Failed to load data)**
- Check that the API server is running
- Visit http://localhost:8000 to verify
- Restart the server if needed

**Items not showing up**
- Click the refresh button (🔄)
- Check your browser's console (F12) for errors
- Make sure you're on the correct user (demo@freshtrack.app)

**Page looks broken**
- Clear your browser cache (Ctrl+Shift+Delete)
- Try a different browser (Chrome recommended)
- Make sure all files (index.html, styles.css, app.js) are in the same folder

---

## 🎨 Interface Features

### Navigation Bar:

**Top Left:**
- 🧊 **FreshTrack** logo - Click to go home

**Center:**
- Navigation links with icons
- Active page is highlighted in blue

**Top Right:**
- Current user email (demo@freshtrack.app)

### Color Theme:

- **Primary Blue** (#4F46E5) - Main actions and active states
- **Green** (#10B981) - Success, fresh items
- **Orange** (#F59E0B) - Warnings, urgent items
- **Red** (#EF4444) - Danger, expired items

### Responsive Design:

The interface automatically adjusts to your screen size:
- **Desktop** - Full layout with grid displays
- **Tablet** - Adjusted columns for medium screens
- **Mobile** - Single column, touch-friendly buttons

---

## 📱 Mobile Usage

While the web interface works on mobile browsers, for the best mobile experience:

1. Open in Chrome or Safari on your phone
2. Add to home screen for quick access:
   - **iPhone**: Tap Share → Add to Home Screen
   - **Android**: Tap Menu (⋮) → Add to Home screen

The interface will work like a native app!

---

## 🔐 Privacy & Data

### Your Data:

- All data is stored locally in `backend/data/freshtrack.db`
- No data is sent to external servers
- Demo user is: demo@freshtrack.app (User ID: 1)

### Changing Users:

To use a different user account:

1. Open `web/app.js` in a text editor
2. Find line 2: `const USER_ID = 1;`
3. Change `1` to your user ID
4. Save and refresh the page

---

## 🆘 Getting Help

### Quick Links:

- **API Documentation**: http://localhost:8000/docs
- **Test API**: Run `venv\Scripts\python test_api.py`
- **Reset Demo**: Run `venv\Scripts\python demo.py`

### Common Issues:

**Issue: Can't connect to API**
```bash
# Check if server is running
curl http://localhost:8000

# If not, start it
cd backend
venv\Scripts\python main.py
```

**Issue: No data showing**
```bash
# Reset with demo data
cd backend
venv\Scripts\python demo.py
```

**Issue: Page won't load**
- Check file path: `C:\Users\egeun\Documents\FreshTrack\web\index.html`
- Make sure all files are in the `web` folder
- Try opening directly: `file:///C:/Users/egeun/Documents/FreshTrack/web/index.html`

---

## 🎉 You're All Set!

**Your FreshTrack web interface is ready to use!**

**Quick Start Checklist:**
- ✅ API server running (http://localhost:8000)
- ✅ Web interface open in browser
- ✅ Demo data loaded
- ✅ You know how to navigate

**Start managing your food and reducing waste today!** 🧊🍎🥗

---

## 📚 Additional Resources

- **Main README**: `README.md` - Complete project documentation
- **Quick Start**: `QUICKSTART.md` - Fast setup guide
- **Web README**: `web/README.md` - Technical web documentation
- **GitHub**: https://github.com/eunice-guo/FreshTrack

Happy food tracking! 🎊
