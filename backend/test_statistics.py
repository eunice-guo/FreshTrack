"""
Tests for statistics endpoints
"""
import pytest
from datetime import datetime, timedelta


class TestStatisticsEndpoints:
    """Test statistics API endpoints"""

    def test_get_user_statistics(self, client, test_user, test_food_items):
        """Test getting user statistics"""
        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # Check all required fields are present
        assert "total_items" in data
        assert "expiring_today" in data
        assert "expiring_within_3_days" in data
        assert "fresh_items" in data
        assert "category_breakdown" in data

        # Verify data types
        assert isinstance(data["total_items"], int)
        assert isinstance(data["expiring_today"], int)
        assert isinstance(data["expiring_within_3_days"], int)
        assert isinstance(data["fresh_items"], int)
        assert isinstance(data["category_breakdown"], dict)

    def test_statistics_counts(self, client, test_user, test_food_items):
        """Test that statistics counts are accurate"""
        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # We have 4 items total, but 1 is expired so only 3 are not consumed
        assert data["total_items"] == 3

        # Should have items expiring soon (milk expires in 2 days)
        assert data["expiring_within_3_days"] >= 1

        # Should have fresh items (apple expires in 10 days, rice in 365 days)
        assert data["fresh_items"] >= 1

    def test_statistics_category_breakdown(self, client, test_user, test_food_items):
        """Test category breakdown in statistics"""
        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        category_breakdown = data["category_breakdown"]

        # Should have multiple categories
        assert len(category_breakdown) > 0

        # Each category should have a positive count
        for category, count in category_breakdown.items():
            assert count > 0

    def test_statistics_empty_inventory(self, client, test_user):
        """Test statistics when user has no items"""
        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # All counts should be 0
        assert data["total_items"] == 0
        assert data["expiring_today"] == 0
        assert data["expiring_within_3_days"] == 0
        assert data["fresh_items"] == 0
        assert len(data["category_breakdown"]) == 0

    def test_statistics_with_consumed_items(self, client, test_user, test_food_items):
        """Test that consumed items are not counted in statistics"""
        # Mark one item as consumed
        item_id = test_food_items[0].id
        client.put(f"/api/items/consume/{item_id}")

        # Get statistics
        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # Total items should be reduced by 1
        assert data["total_items"] == 2

    def test_statistics_expiring_today_accuracy(self, client, test_user, test_db):
        """Test expiring_today count with specific test data"""
        from models import FoodItem

        # Add an item expiring today
        now = datetime.utcnow()
        today_item = FoodItem(
            user_id=test_user.id,
            food_name="Expires Today",
            expiration_date=now.replace(hour=12, minute=0, second=0, microsecond=0)
        )
        test_db.add(today_item)
        test_db.commit()

        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # Should count the item expiring today
        assert data["expiring_today"] >= 1

    def test_statistics_fresh_items_threshold(self, client, test_user, test_db):
        """Test that fresh items are correctly identified (>7 days)"""
        from models import FoodItem

        # Add items with different expiration dates
        now = datetime.utcnow()

        # Fresh item (expires in 10 days)
        fresh_item = FoodItem(
            user_id=test_user.id,
            food_name="Very Fresh",
            expiration_date=now + timedelta(days=10)
        )

        # Not fresh item (expires in 5 days)
        not_fresh_item = FoodItem(
            user_id=test_user.id,
            food_name="Not Fresh",
            expiration_date=now + timedelta(days=5)
        )

        test_db.add(fresh_item)
        test_db.add(not_fresh_item)
        test_db.commit()

        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # Should have at least 1 fresh item
        assert data["fresh_items"] >= 1

    def test_statistics_complete_workflow(self, client, test_user, test_db):
        """Test statistics through a complete workflow"""
        from models import FoodItem

        now = datetime.utcnow()

        # Add various items
        items = [
            FoodItem(
                user_id=test_user.id,
                food_name="Fresh Item 1",
                category="水果",
                expiration_date=now + timedelta(days=15)
            ),
            FoodItem(
                user_id=test_user.id,
                food_name="Fresh Item 2",
                category="水果",
                expiration_date=now + timedelta(days=20)
            ),
            FoodItem(
                user_id=test_user.id,
                food_name="Urgent Item",
                category="蔬菜",
                expiration_date=now + timedelta(days=2)
            )
        ]

        for item in items:
            test_db.add(item)
        test_db.commit()

        # Get statistics
        response = client.get(f"/api/stats/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # Should have 3 items
        assert data["total_items"] == 3

        # Should have 2 fresh items (>7 days)
        assert data["fresh_items"] == 2

        # Should have 1 item expiring within 3 days
        assert data["expiring_within_3_days"] == 1

        # Category breakdown should show 2 fruits and 1 vegetable
        assert data["category_breakdown"]["水果"] == 2
        assert data["category_breakdown"]["蔬菜"] == 1
