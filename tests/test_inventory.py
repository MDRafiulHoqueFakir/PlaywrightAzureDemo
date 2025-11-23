import os
import sys

# Add parent directory to sys.path to allow running this file directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
import allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from playwright.sync_api import Page, expect

@allure.feature("Inventory")
class TestInventory:

    # Test case for successful logout.
    @allure.story("Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, page: Page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        with allure.step("Login as standard user"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Perform logout"):
            # Logout from the application.
            inventory_page.logout()
            
        with allure.step("Verify redirection to login page"):
            # Assert that we are back on the login page.
            expect(page).to_have_url("https://www.saucedemo.com/")
            # Verify that the login button is visible.
            expect(login_page.login_button).to_be_visible()

    # Test case for sorting products by price (low to high).
    @allure.story("Sorting")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_low_to_high(self, page: Page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        with allure.step("Login as standard user"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Sort products by Price (low to high)"):
            # Select the 'lohi' option to sort by price low to high.
            inventory_page.sort_by("lohi")
            
        with allure.step("Verify sorting"):
            # Get all product prices.
            prices = page.locator(".inventory_item_price").all_inner_texts()
            # Convert price strings (e.g., "$29.99") to floats.
            price_values = [float(price.replace("$", "")) for price in prices]
            # Assert that the list of prices is sorted in ascending order.
            assert price_values == sorted(price_values), "Prices are not sorted low to high"

    # Test case for resetting the app state.
    @allure.story("App State")
    @allure.severity(allure.severity_level.NORMAL)
    def test_reset_app_state(self, page: Page):
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        
        with allure.step("Login as standard user"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Add item to cart"):
            # Add an item to the cart.
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            # Verify cart badge shows 1.
            expect(inventory_page.cart_badge).to_have_text("1")
            
        with allure.step("Reset App State"):
            # Reset the app state via the menu.
            inventory_page.reset_app_state()
            
        with allure.step("Verify cart is empty"):
            # Assert that the cart badge is no longer visible (cart is empty).
            expect(inventory_page.cart_badge).not_to_be_visible()

    # Advanced: Network Interception (Mocking)
    # This test intercepts network requests and aborts loading of images.
    # It verifies that the application handles missing assets gracefully (page still loads).
    @allure.story("Advanced: Network Interception")
    @allure.severity(allure.severity_level.NORMAL)
    def test_inventory_no_images(self, page: Page):
        # Define a route handler to abort image requests.
        def abort_images(route):
            if route.request.resource_type == "image":
                route.abort()
            else:
                route.continue_()

        # Apply the route handler to all requests matching the pattern.
        # This effectively blocks all images from loading.
        page.route("**/*", abort_images)

        login_page = LoginPage(page)
        
        with allure.step("Login with images blocked"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Verify page loads without images"):
            # Verify that the inventory list is still visible even without images.
            expect(page.locator(".inventory_list")).to_be_visible()
            # Verify that product names are present (proving page loaded).
            expect(page.locator(".inventory_item_name")).to_have_count(6)

if __name__ == "__main__":
    import subprocess
    script_path = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [sys.executable, "-m", "pytest", "--headed", script_path]
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=project_root)