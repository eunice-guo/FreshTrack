"""
Initialize database with sample food shelf life data
Based on common Chinese and international foods
"""
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from models import FoodShelfLife

# Sample shelf life data (in days)
SAMPLE_FOOD_DATA = [
    # 乳制品 (Dairy)
    {
        "food_name": "milk",
        "food_name_cn": "牛奶",
        "category": "乳制品",
        "pantry_min": 0,
        "pantry_max": 0,
        "refrigerator_min": 5,
        "refrigerator_max": 7,
        "freezer_min": 90,
        "freezer_max": 180,
        "tips": "开封后需冷藏，3-5天内饮用完毕"
    },
    {
        "food_name": "yogurt",
        "food_name_cn": "酸奶",
        "category": "乳制品",
        "refrigerator_min": 7,
        "refrigerator_max": 14,
        "tips": "注意查看生产日期，开封后尽快食用"
    },
    {
        "food_name": "cheese",
        "food_name_cn": "奶酪",
        "category": "乳制品",
        "refrigerator_min": 14,
        "refrigerator_max": 30,
        "freezer_min": 180,
        "freezer_max": 365,
        "tips": "硬质奶酪保存时间更长"
    },

    # 蔬菜 (Vegetables)
    {
        "food_name": "lettuce",
        "food_name_cn": "生菜",
        "category": "蔬菜",
        "refrigerator_min": 3,
        "refrigerator_max": 7,
        "tips": "用纸巾包裹可延长保鲜"
    },
    {
        "food_name": "broccoli",
        "food_name_cn": "西兰花",
        "category": "蔬菜",
        "refrigerator_min": 5,
        "refrigerator_max": 7,
        "freezer_min": 180,
        "freezer_max": 365,
        "tips": "焯水后冷冻可保存更久"
    },
    {
        "food_name": "tomato",
        "food_name_cn": "番茄",
        "category": "蔬菜",
        "pantry_min": 3,
        "pantry_max": 5,
        "refrigerator_min": 7,
        "refrigerator_max": 14,
        "tips": "室温保存口感更好，成熟后冷藏"
    },
    {
        "food_name": "potato",
        "food_name_cn": "土豆",
        "category": "蔬菜",
        "pantry_min": 30,
        "pantry_max": 90,
        "refrigerator_min": 60,
        "refrigerator_max": 90,
        "tips": "避光干燥处保存，发芽后不可食用"
    },
    {
        "food_name": "cabbage",
        "food_name_cn": "白菜",
        "category": "蔬菜",
        "refrigerator_min": 7,
        "refrigerator_max": 14,
        "tips": "整颗白菜可保存2周左右"
    },
    {
        "food_name": "carrot",
        "food_name_cn": "胡萝卜",
        "category": "蔬菜",
        "pantry_min": 7,
        "pantry_max": 14,
        "refrigerator_min": 21,
        "refrigerator_max": 30,
        "tips": "去掉叶子后冷藏保存更久"
    },

    # 水果 (Fruits)
    {
        "food_name": "apple",
        "food_name_cn": "苹果",
        "category": "水果",
        "pantry_min": 7,
        "pantry_max": 14,
        "refrigerator_min": 30,
        "refrigerator_max": 60,
        "tips": "与其他水果分开存放，避免催熟"
    },
    {
        "food_name": "banana",
        "food_name_cn": "香蕉",
        "category": "水果",
        "pantry_min": 3,
        "pantry_max": 7,
        "tips": "室温保存，变黑后仍可食用"
    },
    {
        "food_name": "orange",
        "food_name_cn": "橙子",
        "category": "水果",
        "pantry_min": 7,
        "pantry_max": 14,
        "refrigerator_min": 14,
        "refrigerator_max": 21,
        "tips": "柑橘类水果常温即可"
    },
    {
        "food_name": "strawberry",
        "food_name_cn": "草莓",
        "category": "水果",
        "refrigerator_min": 3,
        "refrigerator_max": 7,
        "tips": "食用前清洗，避免提前洗"
    },

    # 肉类 (Meat)
    {
        "food_name": "chicken",
        "food_name_cn": "鸡肉",
        "category": "肉类",
        "refrigerator_min": 1,
        "refrigerator_max": 2,
        "freezer_min": 180,
        "freezer_max": 365,
        "tips": "生鸡肉冷藏1-2天，冷冻可保存数月"
    },
    {
        "food_name": "pork",
        "food_name_cn": "猪肉",
        "category": "肉类",
        "refrigerator_min": 2,
        "refrigerator_max": 3,
        "freezer_min": 180,
        "freezer_max": 270,
        "tips": "分装后冷冻更方便"
    },
    {
        "food_name": "beef",
        "food_name_cn": "牛肉",
        "category": "肉类",
        "refrigerator_min": 2,
        "refrigerator_max": 3,
        "freezer_min": 180,
        "freezer_max": 365,
        "tips": "牛肉可冷冻保存6-12个月"
    },
    {
        "food_name": "fish",
        "food_name_cn": "鱼",
        "category": "肉类",
        "refrigerator_min": 1,
        "refrigerator_max": 2,
        "freezer_min": 90,
        "freezer_max": 180,
        "tips": "鲜鱼应尽快烹饪"
    },

    # 蛋类 (Eggs)
    {
        "food_name": "eggs",
        "food_name_cn": "鸡蛋",
        "category": "蛋类",
        "pantry_min": 7,
        "pantry_max": 14,
        "refrigerator_min": 21,
        "refrigerator_max": 35,
        "tips": "尖头向下存放，不要清洗"
    },

    # 调味品 (Condiments)
    {
        "food_name": "soy_sauce",
        "food_name_cn": "酱油",
        "category": "调味品",
        "pantry_min": 180,
        "pantry_max": 365,
        "refrigerator_min": 365,
        "refrigerator_max": 730,
        "tips": "开封后冷藏保存"
    },
    {
        "food_name": "cooking_oil",
        "food_name_cn": "食用油",
        "category": "调味品",
        "pantry_min": 180,
        "pantry_max": 365,
        "tips": "避光密封保存"
    },
    {
        "food_name": "salt",
        "food_name_cn": "盐",
        "category": "调味品",
        "pantry_min": 1825,
        "pantry_max": 3650,
        "tips": "干燥保存，几乎不会过期"
    },

    # 豆制品 (Tofu products)
    {
        "food_name": "tofu",
        "food_name_cn": "豆腐",
        "category": "豆制品",
        "refrigerator_min": 3,
        "refrigerator_max": 5,
        "freezer_min": 90,
        "freezer_max": 180,
        "tips": "开封后泡在水中冷藏"
    },

    # 主食 (Staples)
    {
        "food_name": "rice",
        "food_name_cn": "大米",
        "category": "主食",
        "pantry_min": 180,
        "pantry_max": 365,
        "tips": "密封防潮，避免生虫"
    },
    {
        "food_name": "bread",
        "food_name_cn": "面包",
        "category": "主食",
        "pantry_min": 3,
        "pantry_max": 7,
        "freezer_min": 30,
        "freezer_max": 90,
        "tips": "常温3-7天，冷冻可延长"
    }
]


def init_sample_data():
    """Initialize database with sample food shelf life data"""
    print("🚀 Initializing database with sample food data...")

    # Initialize database tables
    init_db()

    # Create database session
    db = SessionLocal()

    try:
        # Check if data already exists
        existing_count = db.query(FoodShelfLife).count()
        if existing_count > 0:
            print(f"⚠️  Database already contains {existing_count} food items")
            response = input("Do you want to clear and re-import? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Import cancelled")
                return

            # Clear existing data
            db.query(FoodShelfLife).delete()
            db.commit()
            print("🗑️  Cleared existing data")

        # Insert sample data
        for food_data in SAMPLE_FOOD_DATA:
            food_item = FoodShelfLife(**food_data)
            db.add(food_item)

        db.commit()
        print(f"✅ Successfully imported {len(SAMPLE_FOOD_DATA)} food items!")

        # Display summary
        print("\n📊 Category Summary:")
        from sqlalchemy import func
        categories = db.query(
            FoodShelfLife.category,
            func.count(FoodShelfLife.id)
        ).group_by(FoodShelfLife.category).all()

        for category, count in categories:
            print(f"  - {category}: {count} items")

    except Exception as e:
        print(f"❌ Error importing data: {str(e)}")
        db.rollback()

    finally:
        db.close()


if __name__ == "__main__":
    init_sample_data()
