# 🌐 FreshTrack Web Interface

Beautiful, responsive web interface for FreshTrack food inventory management system.

## ✨ Features

### 📊 Dashboard
- Real-time statistics overview
- Quick glance at total items, expiring items, and fresh items
- Urgent items alerts
- Category breakdown visualization

### 🧊 My Fridge
- Complete inventory view with visual indicators
- Filter by urgency (All / Urgent / Fresh)
- Color-coded expiration status:
  - ❌ Red: Expired
  - ⚠️ Orange: Expiring today
  - 🟡 Yellow: Expiring soon (1-3 days)
  - 🟢 Green: Needs attention (4-7 days)
  - ✅ Blue: Fresh (7+ days)
- Mark items as consumed
- Delete items

### 🍳 Recipe Recommendations
- Smart recipe matching based on available ingredients
- Match percentage display
- Missing ingredients list
- Quick add missing items to shopping list
- Cooking time and category info

### 🛒 Shopping List
- Separate pending and purchased items
- Quick checkbox to mark as purchased
- Add items with reason/notes
- Track why you need each item

### ➕ Add Food Item
- Simple form to manually add items
- Category selection with emojis
- Automatic expiration date suggestions
- Support for various units (个/斤/瓶/袋/盒 etc.)

## 🚀 Quick Start

### 1. Make Sure API Server is Running

```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/python main.py
```

The API should be running on http://localhost:8000

### 2. Open the Web Interface

Simply open `index.html` in your browser:

```bash
cd ~/Documents/FreshTrack/web
start index.html
```

Or double-click `index.html` in File Explorer.

**Alternatively**, you can serve it with Python:

```bash
cd ~/Documents/FreshTrack/web
python -m http.server 8080
```

Then visit: http://localhost:8080

## 🎨 Design Features

- **Modern UI**: Clean, minimalist design with smooth animations
- **Responsive**: Works on desktop, tablet, and mobile
- **Color-coded**: Visual indicators for food freshness
- **Real-time**: Live updates when adding/removing items
- **Toast Notifications**: User-friendly feedback messages
- **Single Page App**: Fast navigation without page reloads

## 🔧 Configuration

The API endpoint is configured in `app.js`:

```javascript
const API_BASE_URL = 'http://localhost:8000';
const USER_ID = 1; // Demo user ID
```

To use a different user or API endpoint, modify these values.

## 📱 Usage Tips

### Dashboard
- Click "🔄 刷新" to reload all statistics
- Urgent items are automatically highlighted
- Category chart shows distribution of your food items

### My Fridge
- Use filter buttons to view specific items:
  - **全部** (All): Show everything
  - **紧急** (Urgent): Expired, today, or 1-3 days
  - **新鲜** (Fresh): 4+ days remaining
- Click "✅ 已吃完" when you finish an item
- Click "🗑️ 删除" to remove an item

### Recipe Recommendations
- Recipes are sorted by match percentage
- Green checkmark (✅) means all ingredients available
- Yellow warning (⚠️) shows missing ingredients
- Click "添加缺失食材到购物清单" to add all missing items at once

### Shopping List
- Click checkbox to mark item as purchased
- Items move to "已购买" section when checked
- Click "➕ 添加商品" to add new items

### Add Food Item
- Fill in all required fields (marked with *)
- Expiration date defaults to 7 days from now
- Price field is optional
- Submit form to add to your fridge

## 🌟 Features Overview

| Feature | Status |
|---------|--------|
| Dashboard Overview | ✅ |
| Statistics Cards | ✅ |
| Urgent Alerts | ✅ |
| Category Visualization | ✅ |
| Food Inventory List | ✅ |
| Filter by Urgency | ✅ |
| Mark as Consumed | ✅ |
| Delete Items | ✅ |
| Recipe Recommendations | ✅ |
| Match Percentage | ✅ |
| Missing Ingredients | ✅ |
| Shopping List Management | ✅ |
| Mark as Purchased | ✅ |
| Add Food Items | ✅ |
| Toast Notifications | ✅ |
| Responsive Design | ✅ |

## 🎯 Browser Compatibility

- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ✅ Mobile browsers

## 🐛 Troubleshooting

### API Connection Error

**Problem**: "加载数据失败" (Failed to load data)

**Solution**:
1. Make sure the API server is running:
   ```bash
   cd ~/Documents/FreshTrack/backend
   venv/Scripts/python main.py
   ```
2. Check that http://localhost:8000 is accessible
3. Open browser console (F12) to see detailed error messages

### CORS Error

**Problem**: Cross-Origin Request Blocked

**Solution**: The backend already has CORS enabled. If you still see errors:
1. Use the same domain for both frontend and backend
2. Or serve the web interface through Python:
   ```bash
   python -m http.server 8080
   ```

### No Data Showing

**Problem**: Empty fridge or no recipes

**Solution**: Run the demo setup script:
```bash
cd ~/Documents/FreshTrack/backend
venv/Scripts/python demo.py
```

This will create demo user and populate sample data.

## 📚 Technical Stack

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **Vanilla JavaScript**: No framework dependencies
- **Fetch API**: RESTful API communication
- **Google Fonts**: Inter font family

## 🔮 Future Enhancements

- [ ] Offline support with Service Workers
- [ ] Push notifications
- [ ] Barcode scanning via camera
- [ ] Meal planning calendar
- [ ] Export/Import data
- [ ] Dark mode
- [ ] Multi-language support
- [ ] Food waste analytics charts

## 📖 API Endpoints Used

```
GET  /api/stats/{user_id}               - Dashboard statistics
GET  /api/items/{user_id}                - All food items
GET  /api/items/expiring/{user_id}       - Expiring items
POST /api/items/{user_id}                - Add food item
PUT  /api/items/consume/{item_id}        - Mark as consumed
DELETE /api/items/{item_id}              - Delete item
GET  /api/recipes/recommend/{user_id}    - Recipe recommendations
GET  /api/shopping/{user_id}             - Shopping list
POST /api/shopping/{user_id}             - Add to shopping list
PUT  /api/shopping/purchase/{item_id}    - Mark as purchased
```

## 🎉 Enjoy!

Your FreshTrack web interface is ready to use! Start tracking your food and reducing waste today! 🧊🍎🥗
