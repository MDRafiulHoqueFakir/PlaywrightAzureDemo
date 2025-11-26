from playwright.sync_api import Page
from .base_page import BasePage

class CartPage(BasePage):
    """
    Represents the Cart and Checkout pages.
    Contains methods for cart management and the checkout process.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Locators
        self.checkout_button = page.locator("[data-test='checkout']")
        self.first_name_input = page.locator("[data-test='firstName']")
        self.last_name_input = page.locator("[data-test='lastName']")
        self.postal_code_input = page.locator("[data-test='postalCode']")
        self.continue_button = page.locator("[data-test='continue']")
        self.finish_button = page.locator("[data-test='finish']")
        self.continue_shopping_button = page.locator("[data-test='continue-shopping']")
        self.complete_header = page.locator(".complete-header")
        self.error_message = page.locator("[data-test='error']")

    def get_item_name(self):
        """Return the name of the first item in the cart."""
        return self.page.locator(".inventory_item_name").first.inner_text()

    def get_item_price(self):
        """Return the price of the first item in the cart."""
        return self.page.locator(".inventory_item_price").first.inner_text()

    def checkout(self, first_name, last_name, zip_code):
        """
        Perform the checkout flow:
        1. Click Checkout
        2. Fill user details
        3. Click Continue
        """
        self.checkout_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.postal_code_input.fill(zip_code)
        self.continue_button.click()

    def finish_checkout(self):
        """Complete the order by clicking the Finish button."""
        self.finish_button.click()

    def get_complete_header(self):
        """Return the success message header after checkout."""
        return self.complete_header.inner_text()

    def remove_item(self, item_name_kebab_case):
        """Remove a specific item from the cart."""
        self.page.locator(f"[data-test='remove-{item_name_kebab_case}']").click()

    def continue_shopping(self):
        """Navigate back to the inventory to continue shopping."""
        self.continue_shopping_button.click()

    def get_checkout_error(self):
        """Return the error message displayed on the checkout page."""
        return self.error_message.inner_text()