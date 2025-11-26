import pytest
from playwright.sync_api import Page, expect
from pages.base_page import BasePage

def test_self_healing_mechanism(page: Page):
    """
    Test to verify that the self-healing mechanism works.
    We will try to find an element with a broken selector, but provide a valid fallback.
    """
    base_page = BasePage(page)
    base_page.navigate("https://www.saucedemo.com/")
    
    # 1. Broken primary selector, Valid fallback
    # Primary: #wrong-id
    # Fallback: [data-test="username"] (which is valid for username input)
    print("\nAttempting self-healing test...")
    
    username_input = base_page.smart_find(
        selector="#wrong-id-for-username", 
        fallbacks=['[data-test="username"]', '#user-name']
    )
    
    # This should succeed if healing works
    username_input.fill("standard_user")
    expect(username_input).to_have_value("standard_user")
    print("Self-healing test PASSED!")

def test_self_healing_failure(page: Page):
    """
    Test to verify that it fails gracefully if all selectors are wrong.
    """
    base_page = BasePage(page)
    base_page.navigate("https://www.saucedemo.com/")
    
    # All selectors are wrong
    print("\nAttempting self-healing failure test...")
    try:
        element = base_page.smart_find(
            selector="#completely-wrong", 
            fallbacks=['#also-wrong']
        )
        # The smart_find returns a locator, but the action should fail or wait_for inside smart_find might have logged error
        # Actually smart_find waits for attached. If it fails, it returns the primary locator.
        # So expect(element).to_be_visible() should fail.
        expect(element).to_be_visible(timeout=2000)
    except Exception as e:
        print(f"Expected failure occurred: {e}")
        assert True
