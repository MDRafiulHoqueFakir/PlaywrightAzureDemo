from playwright.sync_api import Page
from .base_page import BasePage

class InventoryPage(BasePage):
    """
    Represents the Inventory (Product Listing) Page.
    Contains methods to interact with products, the cart, and the main menu.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        # Locators
        self.cart_badge = page.locator(".shopping_cart_badge")
        self.cart_link = page.locator(".shopping_cart_link")
        self.sort_container = page.locator(".product_sort_container")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.locator("#logout_sidebar_link")
        self.reset_link = page.locator("#reset_sidebar_link")
        self.close_menu_button = page.locator("#react-burger-cross-btn")

    def add_item_to_cart(self, item_name_kebab_case):
        """
        Add a specific item to the cart using its kebab-case name.
        Example: 'sauce-labs-backpack'
        """
        self.page.locator(f"[data-test='add-to-cart-{item_name_kebab_case}']").click()

    def get_cart_count(self):
        """Return the number of items currently in the cart."""
        return int(self.cart_badge.inner_text())

    def go_to_cart(self):
        """Navigate to the Cart page."""
        self.cart_link.click()

    def sort_by(self, option_value):
        """
        Sort the inventory items by the given option value.
        Options: 'az', 'za', 'lohi', 'hilo'
        """
        self.sort_container.select_option(option_value)

    def open_menu(self):
        """Open the side menu."""
        self.menu_button.click()

    def logout(self):
        """Perform the logout action via the side menu."""
        self.open_menu()
        self.logout_link.click()

    def reset_app_state(self):
        """Reset the application state (e.g., clear cart) via the side menu."""
        self.open_menu()
        self.reset_link.click()
        self.close_menu_button.click()