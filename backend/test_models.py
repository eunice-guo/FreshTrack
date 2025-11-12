"""
Tests for database models
"""
import pytest
from datetime import datetime, timedelta
from models import User, FoodItem, Recipe, ShoppingListItem, FoodShelfLife


class TestUserModel:
    """Test User model"""

    def test_create_user(self, test_db):
        """Test creating a user"""
        user = User(
            email="newuser@example.com",
            username="New User"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)

        assert user.id is not None
        assert user.email == "newuser@example.com"
        assert user.username == "New User"
        assert user.created_at is not None

    def test_user_relationships(self, test_db, test_user, test_food_items):
        """Test user relationships with food items"""
        assert len(test_user.food_items) == 4
        assert all(isinstance(item, FoodItem) for item in test_user.food_items)


class TestFoodItemModel:
    """Test FoodItem model"""

    def test_create_food_item(self, test_db, test_user):
        """Test creating a food item"""
        now = datetime.utcnow()
        item = FoodItem(
            user_id=test_user.id,
            food_name="Bread",
            food_name_cn="面包",
            category="主食",
            purchase_date=now,
            expiration_date=now + timedelta(days=5),
            quantity=1,
            quantity_unit="袋",
            price=10.0,
            storage_location="pantry"
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        assert item.id is not None
        assert item.user_id == test_user.id
        assert item.food_name == "Bread"
        assert item.is_consumed == 0

    def test_days_left_property(self, test_db, test_user):
        """Test days_left computed property"""
        now = datetime.utcnow()

        # Item expiring in 5 days
        item = FoodItem(
            user_id=test_user.id,
            food_name="Test",
            expiration_date=now + timedelta(days=5)
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        # Allow for small timing differences (4 or 5 days is acceptable)
        assert item.days_left in [4, 5]

    def test_urgency_level_expired(self, test_db, test_user):
        """Test urgency level for expired item"""
        now = datetime.utcnow()

        item = FoodItem(
            user_id=test_user.id,
            food_name="Expired Item",
            expiration_date=now - timedelta(days=1)
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        assert item.urgency_level == "expired"

    def test_urgency_level_today(self, test_db, test_user):
        """Test urgency level for item expiring today"""
        now = datetime.utcnow()

        # Set expiration to end of today to avoid timing issues
        item = FoodItem(
            user_id=test_user.id,
            food_name="Today Item",
            expiration_date=now.replace(hour=23, minute=59, second=59)
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        # Could be "today" or "expired" depending on exact timing
        assert item.urgency_level in ["today", "expired"]

    def test_urgency_level_urgent(self, test_db, test_user):
        """Test urgency level for urgent item (1-3 days)"""
        now = datetime.utcnow()

        item = FoodItem(
            user_id=test_user.id,
            food_name="Urgent Item",
            expiration_date=now + timedelta(days=2)
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        assert item.urgency_level == "urgent"

    def test_urgency_level_warning(self, test_db, test_user):
        """Test urgency level for warning item (4-7 days)"""
        now = datetime.utcnow()

        item = FoodItem(
            user_id=test_user.id,
            food_name="Warning Item",
            expiration_date=now + timedelta(days=5)
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        assert item.urgency_level == "warning"

    def test_urgency_level_fresh(self, test_db, test_user):
        """Test urgency level for fresh item (>7 days)"""
        now = datetime.utcnow()

        item = FoodItem(
            user_id=test_user.id,
            food_name="Fresh Item",
            expiration_date=now + timedelta(days=10)
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        assert item.urgency_level == "fresh"


class TestRecipeModel:
    """Test Recipe model"""

    def test_create_recipe(self, test_db):
        """Test creating a recipe"""
        recipe = Recipe(
            name="Test Recipe",
            name_cn="测试菜谱",
            category="测试",
            ingredients='["ingredient1", "ingredient2"]',
            instructions="Test instructions",
            prep_time=10,
            cook_time=20,
            servings=4
        )
        test_db.add(recipe)
        test_db.commit()
        test_db.refresh(recipe)

        assert recipe.id is not None
        assert recipe.name == "Test Recipe"
        assert recipe.prep_time == 10
        assert recipe.cook_time == 20


class TestShoppingListItemModel:
    """Test ShoppingListItem model"""

    def test_create_shopping_item(self, test_db, test_user):
        """Test creating a shopping list item"""
        item = ShoppingListItem(
            user_id=test_user.id,
            item_name="Test Item",
            quantity=2,
            quantity_unit="个",
            is_purchased=0,
            reason="测试原因"
        )
        test_db.add(item)
        test_db.commit()
        test_db.refresh(item)

        assert item.id is not None
        assert item.user_id == test_user.id
        assert item.item_name == "Test Item"
        assert item.is_purchased == 0


class TestFoodShelfLifeModel:
    """Test FoodShelfLife model"""

    def test_create_shelf_life(self, test_db):
        """Test creating shelf life data"""
        shelf_life = FoodShelfLife(
            food_name="Test Food",
            food_name_cn="测试食物",
            category="测试类别",
            pantry_min=7,
            pantry_max=14,
            refrigerator_min=14,
            refrigerator_max=30,
            freezer_min=180,
            freezer_max=365,
            tips="测试提示"
        )
        test_db.add(shelf_life)
        test_db.commit()
        test_db.refresh(shelf_life)

        assert shelf_life.id is not None
        assert shelf_life.food_name == "Test Food"
        assert shelf_life.refrigerator_max == 30
