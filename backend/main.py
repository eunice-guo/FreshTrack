"""
FreshTrack Backend API
FastAPI application for managing food inventory and reducing waste
"""
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr
import os

from database import get_db, init_db, engine
from models import User, FoodItem, FoodShelfLife, Recipe, ShoppingListItem, Base


# Pydantic schemas for request/response
class UserCreate(BaseModel):
    email: EmailStr
    username: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    username: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class FoodItemResponse(BaseModel):
    id: int
    food_name: str
    category: str
    purchase_date: datetime
    expiration_date: datetime
    quantity: int
    quantity_unit: str
    days_left: Optional[int]
    urgency_level: str
    is_consumed: int

    class Config:
        from_attributes = True


class FoodItemCreate(BaseModel):
    food_name: str
    category: str
    quantity: int = 1
    quantity_unit: str = "个"
    expiration_date: datetime


class RecipeResponse(BaseModel):
    id: int
    name: str
    name_cn: Optional[str]
    category: str
    ingredients: str
    prep_time: Optional[int]
    cook_time: Optional[int]
    match_rate: Optional[float] = None
    missing_ingredients: Optional[List[str]] = None

    class Config:
        from_attributes = True


class ShoppingListItemCreate(BaseModel):
    item_name: str
    quantity: int = 1
    quantity_unit: Optional[str] = None
    reason: Optional[str] = None


class ShoppingListItemResponse(BaseModel):
    id: int
    item_name: str
    quantity: int
    quantity_unit: Optional[str]
    is_purchased: int
    reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


# Create FastAPI app
app = FastAPI(
    title="FreshTrack API",
    description="Smart food inventory management to reduce waste",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database tables on startup"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized!")


# Health check endpoint
@app.get("/")
async def root():
    """Root endpoint - health check"""
    return {
        "message": "FreshTrack API is running!",
        "version": "1.0.0",
        "status": "healthy"
    }


# ==================== USER ENDPOINTS ====================

@app.post("/api/users/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    Args:
        user: User registration data
        db: Database session

    Returns:
        Created user object
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # Create new user
    new_user = User(
        email=user.email,
        username=user.username
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/users/email/{email}", response_model=UserResponse)
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get user by email"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ==================== FOOD ITEM ENDPOINTS ====================

@app.get("/api/items/{user_id}", response_model=List[FoodItemResponse])
async def get_user_items(
    user_id: int,
    include_consumed: bool = False,
    db: Session = Depends(get_db)
):
    """
    Get all food items for a user

    Args:
        user_id: User ID
        include_consumed: Include consumed items (default: False)
        db: Database session

    Returns:
        List of food items
    """
    query = db.query(FoodItem).filter(FoodItem.user_id == user_id)

    if not include_consumed:
        query = query.filter(FoodItem.is_consumed == 0)

    items = query.order_by(FoodItem.expiration_date).all()
    return items


@app.get("/api/items/expiring/{user_id}", response_model=List[FoodItemResponse])
async def get_expiring_items(
    user_id: int,
    days: int = 3,
    db: Session = Depends(get_db)
):
    """
    Get items expiring soon

    Args:
        user_id: User ID
        days: Number of days threshold (default: 3)
        db: Database session

    Returns:
        List of items expiring within specified days
    """
    threshold_date = datetime.now() + timedelta(days=days)

    items = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0,
        FoodItem.expiration_date <= threshold_date
    ).order_by(FoodItem.expiration_date).all()

    return items


@app.post("/api/items/{user_id}", response_model=FoodItemResponse, status_code=status.HTTP_201_CREATED)
async def add_food_item(
    user_id: int,
    item: FoodItemCreate,
    db: Session = Depends(get_db)
):
    """
    Manually add a food item

    Args:
        user_id: User ID
        item: Food item data
        db: Database session

    Returns:
        Created food item
    """
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Create food item
    food_item = FoodItem(
        user_id=user_id,
        food_name=item.food_name,
        category=item.category,
        quantity=item.quantity,
        quantity_unit=item.quantity_unit,
        expiration_date=item.expiration_date
    )

    db.add(food_item)
    db.commit()
    db.refresh(food_item)

    return food_item


@app.put("/api/items/consume/{item_id}")
async def mark_item_consumed(item_id: int, db: Session = Depends(get_db)):
    """
    Mark an item as consumed

    Args:
        item_id: Food item ID
        db: Database session

    Returns:
        Success message
    """
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.is_consumed = 1
    db.commit()

    return {"message": f"Item '{item.food_name}' marked as consumed"}


@app.delete("/api/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    """Delete a food item"""
    item = db.query(FoodItem).filter(FoodItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()

    return {"message": "Item deleted successfully"}


# ==================== RECIPE ENDPOINTS ====================

@app.get("/api/recipes/recommend/{user_id}", response_model=List[RecipeResponse])
async def recommend_recipes(
    user_id: int,
    limit: int = 5,
    db: Session = Depends(get_db)
):
    """
    Recommend recipes based on user's available ingredients

    Args:
        user_id: User ID
        limit: Maximum number of recipes to return
        db: Database session

    Returns:
        List of recommended recipes with match rates
    """
    # Get user's available ingredients
    user_items = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0
    ).all()

    user_ingredients = [item.food_name for item in user_items]

    # Get items expiring soon (within 3 days)
    urgent_items = [
        item.food_name for item in user_items
        if item.days_left is not None and item.days_left <= 3
    ]

    # Get all recipes
    recipes = db.query(Recipe).all()

    # Calculate match rate for each recipe
    scored_recipes = []
    for recipe in recipes:
        import json
        recipe_ingredients = json.loads(recipe.ingredients) if recipe.ingredients else []

        # Calculate match
        matched = len(set(user_ingredients) & set(recipe_ingredients))
        total = len(recipe_ingredients)

        if total == 0:
            continue

        match_rate = matched / total

        # Boost score if recipe uses urgent ingredients
        uses_urgent = any(ing in urgent_items for ing in recipe_ingredients)
        score = match_rate * (1.5 if uses_urgent else 1.0)

        # Find missing ingredients
        missing = list(set(recipe_ingredients) - set(user_ingredients))

        recipe_dict = RecipeResponse(
            id=recipe.id,
            name=recipe.name,
            name_cn=recipe.name_cn,
            category=recipe.category,
            ingredients=recipe.ingredients,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            match_rate=round(match_rate * 100, 1),
            missing_ingredients=missing
        )

        scored_recipes.append((score, recipe_dict))

    # Sort by score and return top N
    scored_recipes.sort(key=lambda x: x[0], reverse=True)
    top_recipes = [recipe for score, recipe in scored_recipes[:limit]]

    return top_recipes


# ==================== SHOPPING LIST ENDPOINTS ====================

@app.get("/api/shopping/{user_id}", response_model=List[ShoppingListItemResponse])
async def get_shopping_list(
    user_id: int,
    include_purchased: bool = False,
    db: Session = Depends(get_db)
):
    """Get user's shopping list"""
    query = db.query(ShoppingListItem).filter(ShoppingListItem.user_id == user_id)

    if not include_purchased:
        query = query.filter(ShoppingListItem.is_purchased == 0)

    items = query.order_by(ShoppingListItem.created_at.desc()).all()
    return items


@app.post("/api/shopping/{user_id}", response_model=ShoppingListItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_shopping_list(
    user_id: int,
    item: ShoppingListItemCreate,
    db: Session = Depends(get_db)
):
    """Add item to shopping list"""
    shopping_item = ShoppingListItem(
        user_id=user_id,
        item_name=item.item_name,
        quantity=item.quantity,
        quantity_unit=item.quantity_unit,
        reason=item.reason
    )

    db.add(shopping_item)
    db.commit()
    db.refresh(shopping_item)

    return shopping_item


@app.put("/api/shopping/purchase/{item_id}")
async def mark_purchased(item_id: int, db: Session = Depends(get_db)):
    """Mark shopping item as purchased"""
    item = db.query(ShoppingListItem).filter(ShoppingListItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Shopping item not found")

    item.is_purchased = 1
    db.commit()

    return {"message": f"'{item.item_name}' marked as purchased"}


# ==================== STATS ENDPOINTS ====================

@app.get("/api/stats/{user_id}")
async def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """
    Get user statistics

    Returns:
        Statistics about user's food inventory
    """
    # Total items
    total_items = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0
    ).count()

    # Items expiring today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    expiring_today = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0,
        FoodItem.expiration_date >= today_start,
        FoodItem.expiration_date < today_end
    ).count()

    # Items expiring within 3 days
    three_days = datetime.now() + timedelta(days=3)
    expiring_soon = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0,
        FoodItem.expiration_date <= three_days
    ).count()

    # Fresh items (more than 7 days)
    seven_days = datetime.now() + timedelta(days=7)
    fresh_items = db.query(FoodItem).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0,
        FoodItem.expiration_date > seven_days
    ).count()

    # Category breakdown
    from sqlalchemy import func
    category_stats = db.query(
        FoodItem.category,
        func.count(FoodItem.id).label('count')
    ).filter(
        FoodItem.user_id == user_id,
        FoodItem.is_consumed == 0
    ).group_by(FoodItem.category).all()

    category_breakdown = {cat: count for cat, count in category_stats}

    return {
        "total_items": total_items,
        "expiring_today": expiring_today,
        "expiring_within_3_days": expiring_soon,
        "fresh_items": fresh_items,
        "category_breakdown": category_breakdown
    }


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
