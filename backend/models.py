"""
Database models for FreshTrack application
"""
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    """User model for storing user information"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with food items
    food_items = relationship("FoodItem", back_populates="owner")
    shopping_items = relationship("ShoppingListItem", back_populates="owner")


class FoodItem(Base):
    """Food item model for tracking items in user's fridge"""
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_name = Column(String(200), nullable=False)
    food_name_cn = Column(String(200))  # Chinese name
    category = Column(String(50))  # 蔬菜/水果/肉类/乳制品等
    purchase_date = Column(DateTime, default=datetime.utcnow)
    expiration_date = Column(DateTime, nullable=False)
    quantity = Column(Integer, default=1)
    quantity_unit = Column(String(20), default="个")  # 个/斤/瓶等
    price = Column(Float)
    storage_location = Column(String(50), default="refrigerator")  # pantry/refrigerator/freezer
    is_consumed = Column(Integer, default=0)  # 0=未吃完, 1=已吃完
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with user
    owner = relationship("User", back_populates="food_items")

    @property
    def days_left(self):
        """Calculate days left until expiration"""
        if self.expiration_date:
            delta = self.expiration_date - datetime.utcnow()
            return delta.days
        return None

    @property
    def urgency_level(self):
        """Get urgency level: expired/urgent/warning/fresh"""
        days = self.days_left
        if days is None:
            return "unknown"
        if days < 0:
            return "expired"
        elif days == 0:
            return "today"
        elif days <= 3:
            return "urgent"
        elif days <= 7:
            return "warning"
        else:
            return "fresh"


class FoodShelfLife(Base):
    """Database for standard food shelf life information"""
    __tablename__ = "food_shelf_life"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String(100), index=True)  # English name
    food_name_cn = Column(String(100), index=True)  # Chinese name
    category = Column(String(50))

    # Shelf life in days for different storage methods
    pantry_min = Column(Integer)
    pantry_max = Column(Integer)
    refrigerator_min = Column(Integer)
    refrigerator_max = Column(Integer)
    freezer_min = Column(Integer)
    freezer_max = Column(Integer)

    tips = Column(Text)  # Storage tips
    created_at = Column(DateTime, default=datetime.utcnow)


class Recipe(Base):
    """Recipe model for storing recipe information"""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    name_cn = Column(String(200))
    category = Column(String(50))
    ingredients = Column(Text)  # JSON string of ingredients list
    instructions = Column(Text)
    prep_time = Column(Integer)  # minutes
    cook_time = Column(Integer)  # minutes
    servings = Column(Integer)
    image_url = Column(String(500))
    source_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)


class ShoppingListItem(Base):
    """Shopping list model"""
    __tablename__ = "shopping_list"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_name = Column(String(200), nullable=False)
    quantity = Column(Integer, default=1)
    quantity_unit = Column(String(20))
    is_purchased = Column(Integer, default=0)  # 0=待购买, 1=已购买
    reason = Column(String(200))  # e.g., "番茄炒蛋需要"
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with user
    owner = relationship("User", back_populates="shopping_items")
