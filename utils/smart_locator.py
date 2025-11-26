from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartLocator:
    """
    A utility to provide self-healing capabilities for Playwright locators.
    It attempts to find an element using a primary selector, and if that fails,
    it tries a list of fallback selectors.
    """
    def __init__(self, page: Page):
        self.page = page

    def get_locator(self, selector: str, fallbacks: list[str] = None, timeout: int = 4000) -> Locator:
        """
        Attempts to find an element using the primary selector.
        If it fails, tries the fallback selectors.
        Returns the first working locator found.
        
        Args:
            selector: The primary selector to try first.
            fallbacks: A list of alternative selectors to try if primary fails.
            timeout: Time in ms to wait for each selector to be attached.
        """
        if fallbacks is None:
            fallbacks = []

        # List of selectors to try: Primary first, then fallbacks
        # We process them sequentially.
        
        # 1. Try Primary
        try:
            loc = self.page.locator(selector)
            # Check if attached. If it's not attached within timeout, we assume it's broken/missing.
            # Note: 'visible' might be better, but 'attached' is safer for existence.
            loc.wait_for(state="attached", timeout=timeout)
            return loc
        except PlaywrightTimeoutError:
            logger.info(f"Primary selector '{selector}' failed/timed out. Attempting self-healing with fallbacks...")

        # 2. Try Fallbacks
        for fb in fallbacks:
            try:
                loc = self.page.locator(fb)
                loc.wait_for(state="attached", timeout=timeout)
                logger.warning(f"Self-Healing SUCCESS! Primary '{selector}' failed. Healed using fallback '{fb}'.")
                return loc
            except PlaywrightTimeoutError:
                continue
        
        # 3. If all fail, return the primary locator so the calling code raises the standard Playwright error
        # (or we could raise a custom error here)
        logger.error(f"Self-Healing FAILED. All selectors failed for target (Primary: '{selector}').")
        return self.page.locator(selector)
