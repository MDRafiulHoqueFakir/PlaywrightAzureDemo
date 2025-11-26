import pytest
from playwright.sync_api import Page, expect
from utils.smart_locator import SmartLocator

def test_generated_page_structure(page: Page):
    # Generated test for https://www.saucedemo.com/
    page.goto('https://www.saucedemo.com/')
    smart = SmartLocator(page)

    # Interaction for input (Type: text)
    element_0 = smart.get_locator('#user-name', fallbacks=['[name="user-name"]', '.input_error.form_input', '[placeholder="Username"]'])
    expect(element_0).to_be_visible()

    # Interaction for input (Type: password)
    element_1 = smart.get_locator('#password', fallbacks=['[name="password"]', '.input_error.form_input', '[placeholder="Password"]'])
    expect(element_1).to_be_visible()

    # Interaction for input (Type: submit)
    element_2 = smart.get_locator('#login-button', fallbacks=['[name="login-button"]', '.submit-button.btn_action'])
    expect(element_2).to_be_visible()
