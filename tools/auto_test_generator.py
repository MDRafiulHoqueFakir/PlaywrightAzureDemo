import os
from playwright.sync_api import sync_playwright

def generate_test_case(url: str, output_path: str):
    """
    Analyzes the web page at 'url' and generates a Playwright test case
    with self-healing selectors.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to {url}...")
        page.goto(url)
        
        # Analyze page to find interactive elements
        # We look for inputs, buttons, and links
        elements_data = page.evaluate("""() => {
            const data = [];
            
            // Helper to get unique-ish selector
            function getSelectors(el) {
                const selectors = [];
                if (el.id) selectors.push(`#${el.id}`);
                if (el.name) selectors.push(`[name="${el.name}"]`);
                if (el.className) selectors.push(`.${el.className.split(' ').join('.')}`);
                if (el.tagName === 'BUTTON' || el.tagName === 'A') {
                    const text = el.innerText.trim();
                    if (text) selectors.push(`text="${text}"`);
                }
                if (el.placeholder) selectors.push(`[placeholder="${el.placeholder}"]`);
                return selectors;
            }

            const inputs = document.querySelectorAll('input:not([type="hidden"])');
            inputs.forEach(el => {
                data.push({
                    tag: 'input',
                    selectors: getSelectors(el),
                    type: el.type
                });
            });

            const buttons = document.querySelectorAll('button');
            buttons.forEach(el => {
                data.push({
                    tag: 'button',
                    selectors: getSelectors(el),
                    text: el.innerText.trim()
                });
            });

            return data;
        }""")
        
        browser.close()
        
        # Generate Python Test Code
        lines = []
        lines.append("import pytest")
        lines.append("from playwright.sync_api import Page, expect")
        lines.append("from utils.smart_locator import SmartLocator")
        lines.append("")
        lines.append(f"def test_generated_page_structure(page: Page):")
        lines.append(f"    # Generated test for {url}")
        lines.append(f"    page.goto('{url}')")
        lines.append(f"    smart = SmartLocator(page)")
        lines.append("")
        
        for i, el in enumerate(elements_data):
            selectors = el['selectors']
            if not selectors:
                continue
            
            primary = selectors[0]
            fallbacks = selectors[1:]
            
            var_name = f"element_{i}"
            lines.append(f"    # Interaction for {el['tag']} (Type: {el.get('type') or el.get('text')})")
            lines.append(f"    {var_name} = smart.get_locator('{primary}', fallbacks={fallbacks})")
            lines.append(f"    expect({var_name}).to_be_visible()")
            lines.append("")
            
        # Write to file
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            f.write("\n".join(lines))
        
        print(f"Test case generated at: {output_path}")

if __name__ == "__main__":
    # Example usage:
    # Generate a test for the inventory page (assuming login is handled or we test a public page)
    # For demo, we'll test a public site or the login page itself.
    target_url = "https://www.saucedemo.com/" 
    output_file = "tests/generated/test_saucedemo_generated.py"
    generate_test_case(target_url, output_file)
