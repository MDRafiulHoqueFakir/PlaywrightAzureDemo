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

@allure.feature("E2E Checkout")
class TestE2E:
    """
    End-to-End (E2E) test suite.
    Covers the complete user journey from login to purchase completion.
    """

    @allure.story("Purchase Flow")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_purchase_flow(self, page: Page):
        """
        Execute a complete purchase flow:
        Login -> Add Item -> Cart -> Checkout -> Finish -> Verify
        """
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)

        # 1. Login Step
        with allure.step("Login as standard user"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")

        # 2. Add Item Step
        item_name = "Sauce Labs Backpack"
        item_price = "$29.99"
        
        with allure.step(f"Add {item_name} to cart"):
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            expect(inventory_page.cart_badge).to_have_text("1")

        # 3. Go to Cart Step
        with allure.step("Navigate to cart"):
            inventory_page.go_to_cart()

        # 4. Verify Item in Cart Step
        with allure.step("Verify item name and price in cart"):
            assert cart_page.get_item_name() == item_name, f"Expected {item_name}, but got {cart_page.get_item_name()}"
            assert cart_page.get_item_price() == item_price, f"Expected {item_price}, but got {cart_page.get_item_price()}"

        # 5. Checkout Step
        with allure.step("Proceed to checkout"):
            cart_page.checkout("John", "Doe", "12345")

        # 6. Finish Step
        with allure.step("Finish checkout"):
            cart_page.finish_checkout()
            
        with allure.step("Verify order completion"):
            expect(cart_page.complete_header).to_have_text("Thank you for your order!")

if __name__ == "__main__":
    import subprocess
    script_path = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [sys.executable, "-m", "pytest", "--headed", script_path]
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=project_root)