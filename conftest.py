import pytest

# This fixture configures the browser context arguments.
# scope="session" means this fixture is created once per test session.
@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        # Inherit existing arguments.
        **browser_context_args,
        # Set no_viewport to True to disable the default viewport size.
        # This is necessary to allow the browser to be maximized fully.
        "no_viewport": True,
    }

# This fixture configures the browser launch arguments.
@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        # Inherit existing arguments.
        **browser_type_launch_args,
        # Add the '--start-maximized' argument to the browser launch command.
        # This tells the browser to start in maximized mode.
        "args": ["--start-maximized", *browser_type_launch_args.get("args", [])],
    }

# You can also add other fixtures here, such as for authentication or data setup.
