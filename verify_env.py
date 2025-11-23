import sys
try:
    import playwright
    import os
    import sys
    print(f"SYS.PATH: {sys.path}")
    if hasattr(playwright, '__path__'):
        print(f"Playwright PATH: {playwright.__path__}")
    else:
        print(f"Playwright FILE: {playwright.__file__}")
    
    from playwright.sync_api import PageAssertions
    print("Successfully imported PageAssertions")
    
    if hasattr(PageAssertions, 'to_have_screenshot'):
        print("PageAssertions has 'to_have_screenshot'")
    else:
        print("PageAssertions DOES NOT have 'to_have_screenshot'")
        
except ImportError:
    print("Could not import PageAssertions from playwright.sync_api")
except Exception as e:
    print(f"Error: {e}")
