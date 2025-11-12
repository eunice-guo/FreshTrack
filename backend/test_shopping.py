"""
Tests for shopping list endpoints
"""
import pytest


class TestShoppingListEndpoints:
    """Test shopping list API endpoints"""

    def test_get_shopping_list(self, client, test_user, test_shopping_items):
        """Test getting shopping list items"""
        response = client.get(f"/api/shopping/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all("item_name" in item for item in data)
        assert all("id" in item for item in data)

    def test_get_shopping_list_user_not_found(self, client):
        """Test getting shopping list for non-existent user"""
        response = client.get("/api/shopping/99999")

        # API returns empty list for non-existent users
        assert response.status_code == 200
        assert response.json() == []

    def test_get_shopping_list_empty(self, client, test_user):
        """Test getting empty shopping list"""
        response = client.get(f"/api/shopping/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0

    def test_add_shopping_item(self, client, test_user):
        """Test adding item to shopping list"""
        response = client.post(
            f"/api/shopping/{test_user.id}",
            json={
                "item_name": "Onion",
                "quantity": 2,
                "quantity_unit": "个",
                "reason": "做饭需要"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["item_name"] == "Onion"
        assert data["quantity"] == 2
        assert data["quantity_unit"] == "个"
        assert data["reason"] == "做饭需要"
        assert data["is_purchased"] == 0

    def test_add_shopping_item_minimal_data(self, client, test_user):
        """Test adding shopping item with minimal data"""
        response = client.post(
            f"/api/shopping/{test_user.id}",
            json={
                "item_name": "Garlic"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["item_name"] == "Garlic"
        assert data["quantity"] == 1  # Default value
        assert data["is_purchased"] == 0

    def test_add_shopping_item_user_not_found(self, client):
        """Test adding shopping item for non-existent user"""
        response = client.post(
            "/api/shopping/99999",
            json={
                "item_name": "Test Item"
            }
        )

        # API creates items for non-existent users
        assert response.status_code == 201

    def test_mark_item_as_purchased(self, client, test_shopping_items):
        """Test marking shopping item as purchased"""
        item_id = test_shopping_items[0].id

        response = client.put(f"/api/shopping/purchase/{item_id}")

        assert response.status_code == 200
        data = response.json()
        assert "marked as purchased" in data["message"]

    def test_mark_item_as_purchased_not_found(self, client):
        """Test marking non-existent item as purchased"""
        response = client.put("/api/shopping/purchase/99999")

        assert response.status_code == 404
        assert "Shopping item not found" in response.json()["detail"]

    def test_shopping_list_workflow(self, client, test_user):
        """Test complete shopping list workflow"""
        # 1. Add item to shopping list
        add_response = client.post(
            f"/api/shopping/{test_user.id}",
            json={
                "item_name": "Carrot",
                "quantity": 5,
                "quantity_unit": "根"
            }
        )
        assert add_response.status_code == 201
        item_id = add_response.json()["id"]

        # 2. Get shopping list and verify item is there
        list_response = client.get(f"/api/shopping/{test_user.id}")
        assert list_response.status_code == 200
        items = list_response.json()
        assert any(item["id"] == item_id for item in items)

        # 3. Mark as purchased
        purchase_response = client.put(f"/api/shopping/purchase/{item_id}")
        assert purchase_response.status_code == 200
        assert "marked as purchased" in purchase_response.json()["message"]

        # 4. Verify it's marked as purchased in list
        final_response = client.get(f"/api/shopping/{test_user.id}")
        assert final_response.status_code == 200
        updated_items = final_response.json()
        purchased_item = next(item for item in updated_items if item["id"] == item_id)
        assert purchased_item["is_purchased"] == 1
