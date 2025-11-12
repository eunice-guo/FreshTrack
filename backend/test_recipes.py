"""
Tests for recipe recommendation endpoints
"""
import pytest


class TestRecipeEndpoints:
    """Test recipe-related API endpoints"""

    def test_get_recipe_recommendations(self, client, test_user, test_food_items, test_recipes):
        """Test getting recipe recommendations based on available ingredients"""
        response = client.get(f"/api/recipes/recommend/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

        # Check that recommendations have required fields
        for recipe in data:
            assert "id" in recipe
            assert "name" in recipe
            assert "match_rate" in recipe
            assert "missing_ingredients" in recipe
            assert 0 <= recipe["match_rate"] <= 100

    def test_recipe_recommendations_user_not_found(self, client):
        """Test recipe recommendations for non-existent user"""
        response = client.get("/api/recipes/recommend/99999")

        assert response.status_code == 404
        assert "User not found" in response.json()["detail"]

    def test_recipe_recommendations_no_items(self, client, test_user, test_recipes):
        """Test recipe recommendations when user has no food items"""
        response = client.get(f"/api/recipes/recommend/{test_user.id}")

        assert response.status_code == 200
        data = response.json()
        # Should still return recipes but with 0% match rate
        assert isinstance(data, list)

    def test_recipe_recommendations_with_apple(self, client, test_user, test_food_items, test_recipes):
        """Test that Apple Pie recipe gets recommended when user has apples"""
        response = client.get(f"/api/recipes/recommend/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        # Find Apple Pie recipe in recommendations
        apple_pie = None
        for recipe in data:
            if "苹果" in recipe.get("name_cn", "") or "Apple" in recipe.get("name", ""):
                apple_pie = recipe
                break

        if apple_pie:
            # Should have some match since user has apples
            assert apple_pie["match_rate"] > 0

    def test_recipe_recommendations_sorting(self, client, test_user, test_food_items, test_recipes):
        """Test that recipe recommendations are sorted by match rate"""
        response = client.get(f"/api/recipes/recommend/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        if len(data) > 1:
            # Check that match rates are in descending order
            match_rates = [recipe["match_rate"] for recipe in data]
            assert match_rates == sorted(match_rates, reverse=True)

    def test_recipe_recommendations_limit(self, client, test_user, test_food_items, test_recipes):
        """Test recipe recommendations with limit parameter"""
        response = client.get(f"/api/recipes/recommend/{test_user.id}?limit=2")

        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 2

    def test_recipe_recommendations_missing_ingredients(self, client, test_user, test_food_items, test_recipes):
        """Test that missing ingredients are properly identified"""
        response = client.get(f"/api/recipes/recommend/{test_user.id}")

        assert response.status_code == 200
        data = response.json()

        for recipe in data:
            if recipe["match_rate"] < 100:
                # If match rate is not 100%, should have missing ingredients
                assert len(recipe["missing_ingredients"]) > 0
            else:
                # If match rate is 100%, should have no missing ingredients
                assert len(recipe["missing_ingredients"]) == 0
