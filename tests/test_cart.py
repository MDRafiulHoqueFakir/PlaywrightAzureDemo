import os
import sys
import pytest
import allure
from playwright.sync_api import Page, expect

# Add parent directory to sys.path to allow running this file directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@allure.feature("Cart")
class TestCart:
    """
    Test suite for Cart functionality.
    Includes item removal, continuing shopping, and UI layout verification.
    """

    @allure.story("Cart Management")
    @allure.severity(allure.severity_level.NORMAL)
    def test_remove_item_from_cart(self, page: Page):
        """Verify that an item can be removed from the cart."""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        with allure.step("Login as standard user"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Add item to cart"):
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            
        with allure.step("Navigate to cart"):
            inventory_page.go_to_cart()
            
        with allure.step("Remove item from cart"):
            cart_page.remove_item("sauce-labs-backpack")
            
        with allure.step("Verify cart is empty"):
            expect(page.locator(".cart_item")).not_to_be_visible()

    @allure.story("Cart Management")
    @allure.severity(allure.severity_level.NORMAL)
    def test_continue_shopping(self, page: Page):
        """Verify that 'Continue Shopping' redirects back to inventory."""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        with allure.step("Login as standard user"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Navigate to cart"):
            inventory_page.go_to_cart()
            
        with allure.step("Click Continue Shopping"):
            cart_page.continue_shopping()
            
        with allure.step("Verify redirection to inventory"):
            expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    @allure.story("Advanced: UI Layout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_cart_layout(self, page: Page):
        """
        Verify the presence and text of key elements on the cart page.
        Ensures UI structure is correct (Title, Headers, Buttons).
        """
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        with allure.step("Login and go to cart"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            inventory_page.go_to_cart()
            
        with allure.step("Verify UI Layout"):
            # Verify page title
            expect(page.locator(".title")).to_have_text("Your Cart")
            # Verify column headers
            expect(page.locator(".cart_quantity_label")).to_have_text("QTY")
            expect(page.locator(".cart_desc_label")).to_have_text("Description")
            # Verify buttons exist
            expect(cart_page.continue_shopping_button).to_be_visible()
            expect(cart_page.checkout_button).to_be_visible()

if __name__ == "__main__":
    import subprocess
    script_path = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [sys.executable, "-m", "pytest", "--headed", script_path]
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=project_root)