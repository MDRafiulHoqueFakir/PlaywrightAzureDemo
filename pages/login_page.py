from playwright.sync_api import Page
from .base_page import BasePage

class LoginPage(BasePage):
    """
    Represents the Login Page of the application.
    Contains locators and methods to interact with the login form.
    """
    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page):
        super().__init__(page)
        # Locators
        self.username_input = page.locator("[data-test='username']")
        self.password_input = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def load(self):
        """Navigate to the Login Page."""
        self.navigate(self.URL)

    def login(self, username, password):
        """Perform the login action with the given credentials."""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self):
        """Retrieve the text of the error message displayed on failure."""
        return self.error_message.inner_text()