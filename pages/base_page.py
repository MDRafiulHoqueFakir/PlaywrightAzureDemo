from playwright.sync_api import Page, Locator

class BasePage:
    """
    BasePage serves as the parent class for all page objects.
    It provides common methods and initializes the Playwright Page object.
    """

    def __init__(self, page: Page):
        """Initialize the BasePage with a Playwright Page instance."""
        self.page = page

    def navigate(self, url: str):
        """Navigate to the specified URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Return the current page title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current page URL."""
        return self.page.url

    def smart_find(self, selector: str, fallbacks: list[str] = None) -> Locator:
        """
        Find an element using SmartLocator with self-healing capabilities.
        """
        from utils.smart_locator import SmartLocator
        finder = SmartLocator(self.page)
        return finder.get_locator(selector, fallbacks)