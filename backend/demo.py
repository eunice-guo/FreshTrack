"""
Demo script to populate database with test user and sample food items
This creates a working demo you can use immediately!
"""
import sys
import io
from datetime import datetime, timedelta

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from database import SessionLocal, init_db
from models import User, FoodItem, FoodShelfLife, Recipe, ShoppingListItem
import json

def create_demo_user(db):
    """Create a demo user account"""

    # Check if demo user already exists
    demo_user = db.query(User).filter(User.email == "demo@freshtrack.app").first()

    if demo_user:
        print("⚠️  Demo user already exists. Using existing user.")
        return demo_user

    # Create new demo user
    demo_user = User(
        email="demo@freshtrack.app",
        username="Demo User"
    )
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)

    print(f"✅ Created demo user: {demo_user.email} (ID: {demo_user.id})")
    return demo_user


def add_sample_food_items(db, user_id):
    """Add sample food items to user's fridge"""

    # Clear existing items for demo user
    db.query(FoodItem).filter(FoodItem.user_id == user_id).delete()

    sample_items = [
        # Items expiring today
        {
            "food_name": "牛奶",
            "category": "乳制品",
            "quantity": 1,
            "quantity_unit": "瓶",
            "days_until_expiry": 0,
            "price": 15.90
        },
        {
            "food_name": "酸奶",
            "category": "乳制品",
            "quantity": 2,
            "quantity_unit": "杯",
            "days_until_expiry": 1,
            "price": 8.50
        },

        # Items expiring soon (within 3 days)
        {
            "food_name": "西兰花",
            "category": "蔬菜",
            "quantity": 1,
            "quantity_unit": "颗",
            "days_until_expiry": 2,
            "price": 12.00
        },
        {
            "food_name": "番茄",
            "category": "蔬菜",
            "quantity": 3,
            "quantity_unit": "个",
            "days_until_expiry": 3,
            "price": 9.60
        },
        {
            "food_name": "鸡蛋",
            "category": "蛋类",
            "quantity": 10,
            "quantity_unit": "个",
            "days_until_expiry": 3,
            "price": 18.00
        },

        # Fresh items
        {
            "food_name": "鸡肉",
            "category": "肉类",
            "quantity": 1,
            "quantity_unit": "斤",
            "days_until_expiry": 5,
            "price": 25.80
        },
        {
            "food_name": "土豆",
            "category": "蔬菜",
            "quantity": 5,
            "quantity_unit": "个",
            "days_until_expiry": 14,
            "price": 8.50
        },
        {
            "food_name": "大米",
            "category": "主食",
            "quantity": 1,
            "quantity_unit": "袋",
            "days_until_expiry": 60,
            "price": 45.00
        },
        {
            "food_name": "酱油",
            "category": "调味品",
            "quantity": 1,
            "quantity_unit": "瓶",
            "days_until_expiry": 180,
            "price": 12.50
        },
        {
            "food_name": "苹果",
            "category": "水果",
            "quantity": 6,
            "quantity_unit": "个",
            "days_until_expiry": 10,
            "price": 24.00
        },
    ]

    print("\n📦 Adding sample food items to fridge...")

    for item_data in sample_items:
        purchase_date = datetime.now()
        expiration_date = purchase_date + timedelta(days=item_data['days_until_expiry'])

        food_item = FoodItem(
            user_id=user_id,
            food_name=item_data['food_name'],
            category=item_data['category'],
            quantity=item_data['quantity'],
            quantity_unit=item_data['quantity_unit'],
            purchase_date=purchase_date,
            expiration_date=expiration_date,
            price=item_data['price']
        )

        db.add(food_item)

        # Show urgency level
        urgency_emoji = {
            'expired': '❌',
            'today': '⚠️',
            'urgent': '🟡',
            'warning': '🟢',
            'fresh': '✅'
        }

        emoji = urgency_emoji.get(food_item.urgency_level, '📦')
        print(f"  {emoji} {item_data['food_name']} - {item_data['quantity']}{item_data['quantity_unit']} - {item_data['days_until_expiry']} days left")

    db.commit()
    print(f"\n✅ Added {len(sample_items)} items to your fridge!")


def add_sample_recipes(db):
    """Add sample Chinese recipes"""

    # Check if recipes already exist
    recipe_count = db.query(Recipe).count()
    if recipe_count > 0:
        print(f"⚠️  {recipe_count} recipes already exist. Skipping recipe creation.")
        return

    print("\n👨‍🍳 Adding sample recipes...")

    sample_recipes = [
        {
            "name": "Tomato Scrambled Eggs",
            "name_cn": "番茄炒蛋",
            "category": "中式家常菜",
            "ingredients": ["番茄", "鸡蛋", "盐", "糖", "油"],
            "instructions": "1. 番茄切块 2. 鸡蛋打散 3. 先炒蛋,盛出 4. 炒番茄,加调料 5. 放入炒好的蛋,翻炒均匀",
            "prep_time": 5,
            "cook_time": 10
        },
        {
            "name": "Stir-fried Broccoli",
            "name_cn": "清炒西兰花",
            "category": "中式家常菜",
            "ingredients": ["西兰花", "蒜", "盐", "油"],
            "instructions": "1. 西兰花焯水 2. 蒜切片 3. 热油爆香蒜 4. 放入西兰花翻炒 5. 加盐调味",
            "prep_time": 5,
            "cook_time": 8
        },
        {
            "name": "Kung Pao Chicken",
            "name_cn": "宫保鸡丁",
            "category": "中式家常菜",
            "ingredients": ["鸡肉", "花生", "干辣椒", "酱油", "醋", "糖"],
            "instructions": "1. 鸡肉切丁腌制 2. 准备宫保汁 3. 热油炒鸡丁 4. 加入干辣椒、花生 5. 倒入宫保汁翻炒",
            "prep_time": 15,
            "cook_time": 10
        },
        {
            "name": "Potato Stir-fry",
            "name_cn": "炒土豆丝",
            "category": "中式家常菜",
            "ingredients": ["土豆", "醋", "盐", "油"],
            "instructions": "1. 土豆切丝泡水 2. 热油下土豆丝 3. 快速翻炒 4. 加醋、盐调味",
            "prep_time": 10,
            "cook_time": 5
        },
        {
            "name": "Apple Yogurt Bowl",
            "name_cn": "苹果酸奶碗",
            "category": "健康早餐",
            "ingredients": ["酸奶", "苹果", "蜂蜜"],
            "instructions": "1. 苹果切块 2. 倒入酸奶 3. 淋上蜂蜜",
            "prep_time": 3,
            "cook_time": 0
        }
    ]

    for recipe_data in sample_recipes:
        recipe = Recipe(
            name=recipe_data['name'],
            name_cn=recipe_data['name_cn'],
            category=recipe_data['category'],
            ingredients=json.dumps(recipe_data['ingredients'], ensure_ascii=False),
            instructions=recipe_data['instructions'],
            prep_time=recipe_data['prep_time'],
            cook_time=recipe_data['cook_time']
        )
        db.add(recipe)
        print(f"  📖 {recipe_data['name_cn']} ({recipe_data['name']})")

    db.commit()
    print(f"\n✅ Added {len(sample_recipes)} recipes!")


def show_summary(db, user_id):
    """Show a summary of the user's fridge status"""

    print("\n" + "="*60)
    print("📊 YOUR FRIDGE SUMMARY")
    print("="*60)

    # Get all items
    all_items = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0
    ).all()

    # Categorize by urgency
    expired_items = [item for item in all_items if item.urgency_level == 'expired']
    today_items = [item for item in all_items if item.urgency_level == 'today']
    urgent_items = [item for item in all_items if item.urgency_level == 'urgent']
    warning_items = [item for item in all_items if item.urgency_level == 'warning']
    fresh_items = [item for item in all_items if item.urgency_level == 'fresh']

    print(f"\n📦 Total Items: {len(all_items)}")
    print(f"❌ Expired: {len(expired_items)}")
    print(f"⚠️  Expiring Today: {len(today_items)}")
    print(f"🟡 Expiring Soon (1-3 days): {len(urgent_items)}")
    print(f"🟢 Need Attention (4-7 days): {len(warning_items)}")
    print(f"✅ Fresh (7+ days): {len(fresh_items)}")

    if today_items or urgent_items:
        print("\n" + "="*60)
        print("⚡ URGENT: Items to use TODAY or SOON!")
        print("="*60)

        for item in today_items + urgent_items:
            days_text = "TODAY!" if item.days_left == 0 else f"{item.days_left} days left"
            print(f"  🔔 {item.food_name} ({item.quantity}{item.quantity_unit}) - {days_text}")

    print("\n" + "="*60)
    print("🍳 RECIPE RECOMMENDATIONS")
    print("="*60)
    print("Based on your available ingredients, you can make:")

    # Get user ingredients
    user_ingredients = [item.food_name for item in all_items]

    # Get recipes and calculate match
    recipes = db.query(Recipe).all()

    scored_recipes = []
    for recipe in recipes:
        recipe_ingredients = json.loads(recipe.ingredients)
        matched = len(set(user_ingredients) & set(recipe_ingredients))
        total = len(recipe_ingredients)

        if matched > 0:
            match_rate = (matched / total) * 100
            missing = list(set(recipe_ingredients) - set(user_ingredients))
            scored_recipes.append((match_rate, recipe, matched, total, missing))

    scored_recipes.sort(key=lambda x: x[0], reverse=True)

    for match_rate, recipe, matched, total, missing in scored_recipes[:3]:
        status = "✅ All ingredients available!" if match_rate == 100 else f"⚠️  Missing: {', '.join(missing)}"
        print(f"\n  🍽️  {recipe.name_cn} ({recipe.name})")
        print(f"      Match: {match_rate:.0f}% ({matched}/{total} ingredients)")
        print(f"      {status}")
        print(f"      Time: {recipe.prep_time + recipe.cook_time} minutes total")

    print("\n" + "="*60)


def main():
    """Main demo setup function"""

    print("="*60)
    print("🧊 FreshTrack Demo Setup")
    print("="*60)
    print("\nThis will set up a working demo with:")
    print("  • Demo user account")
    print("  • 10 sample food items in your fridge")
    print("  • 5 sample recipes")
    print()

    # Initialize database
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Create demo user
        demo_user = create_demo_user(db)

        # Add sample food items
        add_sample_food_items(db, demo_user.id)

        # Add sample recipes
        add_sample_recipes(db)

        # Show summary
        show_summary(db, demo_user.id)

        print("\n" + "="*60)
        print("✅ DEMO SETUP COMPLETE!")
        print("="*60)
        print("\n🚀 Next steps:")
        print(f"   1. Start the API server: venv\\Scripts\\python main.py")
        print(f"   2. Visit: http://localhost:8000/docs")
        print(f"   3. Try API endpoints with user_id: {demo_user.id}")
        print(f"   4. Email: {demo_user.email}")
        print("\n📖 Key endpoints to try:")
        print(f"   • GET /api/items/{demo_user.id} - View all items")
        print(f"   • GET /api/items/expiring/{demo_user.id}?days=3 - Urgent items")
        print(f"   • GET /api/recipes/recommend/{demo_user.id} - Get recipes")
        print(f"   • GET /api/stats/{demo_user.id} - View statistics")
        print()

    except Exception as e:
        print(f"\n❌ Error during demo setup: {str(e)}")
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
