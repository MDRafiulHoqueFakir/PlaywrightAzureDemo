import os
import sys
import pytest
import allure
from playwright.sync_api import Page, expect

# Add parent directory to sys.path to allow running this file directly.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pages.login_page import LoginPage

@allure.feature("Login")
class TestLogin:
    """
    Test suite for Login functionality.
    Covers positive, negative, and data-driven scenarios.
    """

    @allure.story("Positive Login")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_valid_login(self, page: Page):
        """Verify that a valid user can login successfully."""
        login_page = LoginPage(page)
        
        with allure.step("Open Login Page"):
            login_page.load()
            
        with allure.step("Login with valid credentials"):
            login_page.login("standard_user", "secret_sauce")
            
        with allure.step("Verify redirection to inventory"):
            expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

    @allure.story("Negative Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_locked_out_user(self, page: Page):
        """Verify error message for locked-out user."""
        login_page = LoginPage(page)
        
        with allure.step("Open Login Page"):
            login_page.load()
            
        with allure.step("Login with locked out user"):
            login_page.login("locked_out_user", "secret_sauce")
            
        with allure.step("Verify error message"):
            expect(login_page.error_message).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

    @allure.story("Negative Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_credentials(self, page: Page):
        """Verify error message for invalid password."""
        login_page = LoginPage(page)
        
        with allure.step("Open Login Page"):
            login_page.load()
            
        with allure.step("Login with invalid password"):
            login_page.login("standard_user", "wrong_password")
            
        with allure.step("Verify error message"):
            expect(login_page.error_message).to_contain_text("Epic sadface: Username and password do not match any user in this service")

    @allure.story("Negative Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_username(self, page: Page):
        """Verify error message for empty username."""
        login_page = LoginPage(page)
        
        with allure.step("Open Login Page"):
            login_page.load()
            
        with allure.step("Login with empty username"):
            login_page.login("", "secret_sauce")
            
        with allure.step("Verify error message"):
            expect(login_page.error_message).to_contain_text("Epic sadface: Username is required")

    @allure.story("Negative Login")
    @allure.severity(allure.severity_level.NORMAL)
    def test_empty_password(self, page: Page):
        """Verify error message for empty password."""
        login_page = LoginPage(page)
        
        with allure.step("Open Login Page"):
            login_page.load()
            
        with allure.step("Login with empty password"):
            login_page.login("standard_user", "")
            
        with allure.step("Verify error message"):
            expect(login_page.error_message).to_contain_text("Epic sadface: Password is required")

    @allure.story("Advanced: Data-Driven Login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("username, password", [
        ("standard_user", "secret_sauce"),
        ("problem_user", "secret_sauce"),
        ("performance_glitch_user", "secret_sauce"),
        ("error_user", "secret_sauce"),
        ("visual_user", "secret_sauce")
    ])
    def test_login_parametrized(self, page: Page, username, password):
        """Verify login functionality with multiple valid user accounts."""
        login_page = LoginPage(page)
        
        with allure.step(f"Login with user: {username}"):
            login_page.load()
            login_page.login(username, password)
            
        with allure.step("Verify login success"):
            expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

if __name__ == "__main__":
    import subprocess
    script_path = os.path.abspath(__file__)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cmd = [sys.executable, "-m", "pytest", "--headed", script_path]
    print(f"Running command: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=project_root)
