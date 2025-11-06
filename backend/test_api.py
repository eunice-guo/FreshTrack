"""
Simple test script to interact with FreshTrack API
Run this after starting the API server (python main.py)
"""
import sys
import io
import requests
import json
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_URL = "http://localhost:8000"
USER_ID = 1  # Demo user ID


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_health_check():
    """Test if API is running"""
    print_section("🏥 API Health Check")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        return True
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API server!")
        print("   Make sure the server is running: venv\\Scripts\\python main.py")
        return False


def test_get_user():
    """Get user information"""
    print_section("👤 Get User Information")
    response = requests.get(f"{BASE_URL}/api/users/{USER_ID}")

    if response.status_code == 200:
        user = response.json()
        print(f"✅ User found:")
        print(f"   Email: {user['email']}")
        print(f"   Username: {user['username']}")
        print(f"   Created: {user['created_at']}")
    else:
        print(f"❌ Error: {response.status_code}")


def test_get_all_items():
    """Get all food items"""
    print_section("🧊 Get All Fridge Items")
    response = requests.get(f"{BASE_URL}/api/items/{USER_ID}")

    if response.status_code == 200:
        items = response.json()
        print(f"✅ Found {len(items)} items in fridge:\n")

        for item in items:
            urgency_emoji = {
                'expired': '❌',
                'today': '⚠️',
                'urgent': '🟡',
                'warning': '🟢',
                'fresh': '✅'
            }
            emoji = urgency_emoji.get(item['urgency_level'], '📦')

            days_text = f"{item['days_left']} days left" if item['days_left'] > 0 else "EXPIRED" if item['days_left'] < 0 else "TODAY"
            print(f"   {emoji} {item['food_name']} ({item['quantity']}{item['quantity_unit']}) - {days_text}")
    else:
        print(f"❌ Error: {response.status_code}")


def test_get_expiring_items():
    """Get items expiring soon"""
    print_section("⏰ Get Items Expiring Soon (Within 3 Days)")
    response = requests.get(f"{BASE_URL}/api/items/expiring/{USER_ID}?days=3")

    if response.status_code == 200:
        items = response.json()
        print(f"✅ Found {len(items)} items expiring soon:\n")

        for item in items:
            days_text = "TODAY!" if item['days_left'] == 0 else f"{item['days_left']} days left"
            print(f"   🔔 {item['food_name']} - {days_text}")

        if not items:
            print("   🎉 No items expiring soon!")
    else:
        print(f"❌ Error: {response.status_code}")


def test_get_recipe_recommendations():
    """Get recipe recommendations"""
    print_section("🍳 Get Recipe Recommendations")
    response = requests.get(f"{BASE_URL}/api/recipes/recommend/{USER_ID}?limit=5")

    if response.status_code == 200:
        recipes = response.json()
        print(f"✅ Found {len(recipes)} recommended recipes:\n")

        for i, recipe in enumerate(recipes, 1):
            match_rate = recipe.get('match_rate', 0)
            missing = recipe.get('missing_ingredients', [])

            print(f"   {i}. {recipe['name_cn']} ({recipe['name']})")
            print(f"      Match: {match_rate}%")

            if missing:
                print(f"      Missing: {', '.join(missing)}")
            else:
                print(f"      ✅ All ingredients available!")

            total_time = recipe.get('prep_time', 0) + recipe.get('cook_time', 0)
            print(f"      Time: {total_time} minutes\n")

        if not recipes:
            print("   📝 No recipes found. Add more ingredients or recipes!")
    else:
        print(f"❌ Error: {response.status_code}")


def test_get_statistics():
    """Get user statistics"""
    print_section("📊 Get Inventory Statistics")
    response = requests.get(f"{BASE_URL}/api/stats/{USER_ID}")

    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Inventory Statistics:\n")
        print(f"   📦 Total Items: {stats['total_items']}")
        print(f"   ❌ Expiring Today: {stats['expiring_today']}")
        print(f"   🟡 Expiring Within 3 Days: {stats['expiring_within_3_days']}")
        print(f"   ✅ Fresh Items: {stats['fresh_items']}")

        if stats.get('category_breakdown'):
            print(f"\n   📋 By Category:")
            for category, count in stats['category_breakdown'].items():
                print(f"      • {category}: {count}")
    else:
        print(f"❌ Error: {response.status_code}")


def test_add_item():
    """Test adding a new food item"""
    print_section("➕ Add New Food Item")

    new_item = {
        "food_name": "草莓",
        "category": "水果",
        "quantity": 10,
        "quantity_unit": "个",
        "expiration_date": (datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                           .replace(day=datetime.now().day + 4)
                           .isoformat())
    }

    print(f"Adding: {new_item['food_name']} ({new_item['quantity']}{new_item['quantity_unit']})")

    response = requests.post(f"{BASE_URL}/api/items/{USER_ID}", json=new_item)

    if response.status_code == 201:
        item = response.json()
        print(f"✅ Successfully added!")
        print(f"   ID: {item['id']}")
        print(f"   Name: {item['food_name']}")
        print(f"   Days left: {item['days_left']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"   {response.text}")


def test_add_to_shopping_list():
    """Test adding item to shopping list"""
    print_section("🛒 Add to Shopping List")

    shopping_item = {
        "item_name": "蜂蜜",
        "quantity": 1,
        "quantity_unit": "瓶",
        "reason": "苹果酸奶碗需要"
    }

    print(f"Adding to shopping list: {shopping_item['item_name']}")

    response = requests.post(f"{BASE_URL}/api/shopping/{USER_ID}", json=shopping_item)

    if response.status_code == 201:
        print(f"✅ Successfully added to shopping list!")
    else:
        print(f"❌ Error: {response.status_code}")


def test_get_shopping_list():
    """Get shopping list"""
    print_section("📝 Get Shopping List")
    response = requests.get(f"{BASE_URL}/api/shopping/{USER_ID}")

    if response.status_code == 200:
        items = response.json()
        print(f"✅ Found {len(items)} items in shopping list:\n")

        for item in items:
            status = "☑️" if item['is_purchased'] else "☐"
            reason_text = f" ({item['reason']})" if item.get('reason') else ""
            print(f"   {status} {item['item_name']} - {item['quantity']}{item.get('quantity_unit', '')}{reason_text}")

        if not items:
            print("   📝 Shopping list is empty!")
    else:
        print(f"❌ Error: {response.status_code}")


def main():
    """Run all API tests"""
    print("="*60)
    print("🧪 FreshTrack API Testing")
    print("="*60)
    print("\nThis script will test all major API endpoints")
    print("Make sure the API server is running first!\n")

    # Test health check first
    if not test_health_check():
        return

    # Run all tests
    try:
        test_get_user()
        test_get_all_items()
        test_get_expiring_items()
        test_get_recipe_recommendations()
        test_get_statistics()
        test_add_item()
        test_add_to_shopping_list()
        test_get_shopping_list()

        print("\n" + "="*60)
        print("✅ All API tests completed!")
        print("="*60)
        print("\n🌐 Visit http://localhost:8000/docs for interactive API docs")
        print()

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")


if __name__ == "__main__":
    main()
