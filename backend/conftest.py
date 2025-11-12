"""
Pytest configuration and fixtures for FreshTrack backend tests
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Import from the application
from database import Base, get_db
from models import User, FoodItem, Recipe, ShoppingListItem, FoodShelfLife

# Use in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test_freshtrack.db"

# Create test engine globally
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh test database for each test function
    """
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create session
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(test_db):
    """
    Create a test client with test database dependency override
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    # Import app here to avoid circular imports
    from main import app

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app, raise_server_exceptions=False) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    """Cleanup test database file after all tests"""
    yield
    # Remove test database file
    if os.path.exists("test_freshtrack.db"):
        os.remove("test_freshtrack.db")


@pytest.fixture(scope="function")
def test_user(test_db):
    """
    Create a test user in the database
    """
    user = User(
        email="test@example.com",
        username="Test User"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_food_items(test_db, test_user):
    """
    Create test food items in the database
    """
    now = datetime.utcnow()

    items = [
        FoodItem(
            user_id=test_user.id,
            food_name="Milk",
            food_name_cn="牛奶",
            category="乳制品",
            purchase_date=now,
            expiration_date=now + timedelta(days=2),  # Expiring soon
            quantity=1,
            quantity_unit="瓶",
            price=15.5,
            storage_location="refrigerator"
        ),
        FoodItem(
            user_id=test_user.id,
            food_name="Apple",
            food_name_cn="苹果",
            category="水果",
            purchase_date=now,
            expiration_date=now + timedelta(days=10),  # Fresh
            quantity=5,
            quantity_unit="个",
            price=12.0,
            storage_location="refrigerator"
        ),
        FoodItem(
            user_id=test_user.id,
            food_name="Expired Yogurt",
            food_name_cn="酸奶",
            category="乳制品",
            purchase_date=now - timedelta(days=5),
            expiration_date=now - timedelta(days=1),  # Expired
            quantity=1,
            quantity_unit="瓶",
            price=8.0,
            storage_location="refrigerator"
        ),
        FoodItem(
            user_id=test_user.id,
            food_name="Rice",
            food_name_cn="大米",
            category="主食",
            purchase_date=now,
            expiration_date=now + timedelta(days=365),  # Long shelf life
            quantity=1,
            quantity_unit="袋",
            price=50.0,
            storage_location="pantry"
        )
    ]

    for item in items:
        test_db.add(item)
    test_db.commit()

    for item in items:
        test_db.refresh(item)

    return items


@pytest.fixture(scope="function")
def test_recipes(test_db):
    """
    Create test recipes in the database
    """
    recipes = [
        Recipe(
            name="Tomato Scrambled Eggs",
            name_cn="番茄炒蛋",
            category="家常菜",
            ingredients='["番茄", "鸡蛋", "盐", "糖"]',
            instructions="1. 番茄切块 2. 鸡蛋打散 3. 先炒蛋后炒番茄",
            prep_time=5,
            cook_time=10,
            servings=2
        ),
        Recipe(
            name="Apple Pie",
            name_cn="苹果派",
            category="甜点",
            ingredients='["苹果", "面粉", "黄油", "糖"]',
            instructions="1. 准备派皮 2. 切苹果 3. 烤制",
            prep_time=20,
            cook_time=45,
            servings=6
        ),
        Recipe(
            name="Fried Rice",
            name_cn="炒饭",
            category="主食",
            ingredients='["米饭", "鸡蛋", "蔬菜", "酱油"]',
            instructions="1. 准备隔夜饭 2. 炒蛋 3. 加饭和配菜翻炒",
            prep_time=10,
            cook_time=10,
            servings=2
        )
    ]

    for recipe in recipes:
        test_db.add(recipe)
    test_db.commit()

    for recipe in recipes:
        test_db.refresh(recipe)

    return recipes


@pytest.fixture(scope="function")
def test_shopping_items(test_db, test_user):
    """
    Create test shopping list items in the database
    """
    items = [
        ShoppingListItem(
            user_id=test_user.id,
            item_name="番茄",
            quantity=3,
            quantity_unit="个",
            is_purchased=0,
            reason="番茄炒蛋需要"
        ),
        ShoppingListItem(
            user_id=test_user.id,
            item_name="鸡蛋",
            quantity=6,
            quantity_unit="个",
            is_purchased=1,
            reason="已购买"
        )
    ]

    for item in items:
        test_db.add(item)
    test_db.commit()

    for item in items:
        test_db.refresh(item)

    return items


@pytest.fixture(scope="function")
def test_shelf_life_data(test_db):
    """
    Create test shelf life data
    """
    shelf_life_items = [
        FoodShelfLife(
            food_name="Milk",
            food_name_cn="牛奶",
            category="乳制品",
            refrigerator_min=5,
            refrigerator_max=7,
            tips="开封后尽快饮用"
        ),
        FoodShelfLife(
            food_name="Apple",
            food_name_cn="苹果",
            category="水果",
            pantry_min=7,
            pantry_max=14,
            refrigerator_min=30,
            refrigerator_max=60,
            tips="放冰箱可保存更久"
        )
    ]

    for item in shelf_life_items:
        test_db.add(item)
    test_db.commit()

    return shelf_life_items
