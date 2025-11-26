import os
import sys
import random
import string
import pytest
import allure
from playwright.sync_api import Page, expect

# Add parent directory to sys.path to allow running this file directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

@allure.feature("Checkout")
class TestCheckout:
    """
    Test suite for Checkout functionality.
    Includes dynamic data input and negative form validation.
    """

    @allure.story("Advanced: Dynamic Data")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_dynamic_data(self, page: Page):
        """
        Verify checkout with randomly generated user data.
        Ensures application handles variable input correctly.
        """
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        # Helper functions for random data
        def random_string(length=8):
            return ''.join(random.choices(string.ascii_letters, k=length))
            
        def random_digits(length=5):
            return ''.join(random.choices(string.digits, k=length))

        first_name = random_string()
        last_name = random_string()
        zip_code = random_digits()
        
        with allure.step("Login and go to checkout"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            inventory_page.go_to_cart()
            
        with allure.step(f"Checkout with dynamic data: {first_name} {last_name}, {zip_code}"):
            cart_page.checkout(first_name, last_name, zip_code)
            
        with allure.step("Verify checkout overview"):
            expect(cart_page.finish_button).to_be_visible()

    @allure.story("Negative Checkout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_empty_firstname(self, page: Page):
        """Verify error message when First Name is empty."""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        with allure.step("Login and go to checkout"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            inventory_page.go_to_cart()
            cart_page.checkout_button.click()
            
        with allure.step("Try to continue with empty first name"):
            cart_page.last_name_input.fill("Doe")
            cart_page.postal_code_input.fill("12345")
            cart_page.continue_button.click()
            
        with allure.step("Verify error message"):
            expect(page.locator("[data-test='error']")).to_contain_text("Error: First Name is required")

    @allure.story("Negative Checkout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_empty_lastname(self, page: Page):
        """Verify error message when Last Name is empty."""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        with allure.step("Login and go to checkout"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            inventory_page.go_to_cart()
            cart_page.checkout_button.click()
            
        with allure.step("Try to continue with empty last name"):
            cart_page.first_name_input.fill("John")
            cart_page.postal_code_input.fill("12345")
            cart_page.continue_button.click()
            
        with allure.step("Verify error message"):
            expect(page.locator("[data-test='error']")).to_contain_text("Error: Last Name is required")

    @allure.story("Negative Checkout")
    @allure.severity(allure.severity_level.NORMAL)
    def test_checkout_empty_zip(self, page: Page):
        """Verify error message when Postal Code is empty."""
        login_page = LoginPage(page)
        inventory_page = InventoryPage(page)
        cart_page = CartPage(page)
        
        with allure.step("Login and go to checkout"):
            login_page.load()
            login_page.login("standard_user", "secret_sauce")
            inventory_page.add_item_to_cart("sauce-labs-backpack")
            inventory_page.go_to_cart()
            cart_page.checkout_button.click()
            
        with allure.step("Try to continue with empty zip code"):
            cart_page.first_name_input.fill("John")
            cart_page.last_name_input.fill("Doe")
            cart_page.continue_button.click()
            
        with allure.step("Verify error message"):
            expect(page.locator("[data-test='error']")).to_contain_text("Error: Postal Code is required")

if __name__ == "__main__":
    import subprocess
    script_path = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [sys.executable, "-m", "pytest", "--headed", script_path]
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=project_root)