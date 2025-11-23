# Playwright Azure DevOps Automation

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-Latest-green)
![Azure DevOps](https://img.shields.io/badge/Azure%20DevOps-CI%2FCD-0078D7)

A professional-grade test automation framework built with **Python** and **Playwright**, using the **Page Object Model (POM)** design pattern. This project demonstrates automated testing of an e-commerce application (SauceDemo) with integration into **Azure DevOps** for CI/CD and **Allure** for reporting.

## 🚀 Features

*   **Page Object Model (POM)**: Modular and maintainable code structure.
*   **Cross-Browser Testing**: Supports Chromium, Firefox, and WebKit.
*   **CI/CD Integration**: Azure Pipelines configuration for automated execution.
*   **Allure Reporting**: Rich, interactive test reports with step-by-step logging.
*   **Parallel Execution**: Fast test runs using `pytest-xdist`.
*   **Visual Execution**: Option to run tests in headed mode for debugging.
*   **Comprehensive Scenarios**: Covers Login, Inventory, Cart, Checkout, and Negative testing.

## 📂 Project Structure

```
PlaywrightAzureDemo/
├── pages/                  # Page Object Classes
│   ├── base_page.py        # Base class with common methods
│   ├── login_page.py       # Login page interactions
│   ├── inventory_page.py   # Product listing page interactions
│   └── cart_page.py        # Cart and Checkout page interactions
├── tests/                  # Test Scripts
│   ├── test_login.py       # Login scenarios (Positive & Negative)
│   ├── test_inventory.py   # Inventory scenarios (Sorting, Logout)
│   ├── test_cart.py        # Cart scenarios (Add/Remove, Continue Shopping)
│   ├── test_checkout.py    # Checkout scenarios (E2E, Validation)
│   └── test_e2e.py         # Complete End-to-End Purchase Flow
├── azure-pipelines.yml     # Azure DevOps Pipeline configuration
├── conftest.py             # Pytest fixtures (Browser config)
├── pytest.ini              # Pytest configuration
├── requirements.txt        # Project dependencies
└── README.md               # Project documentation
```

## 🛠️ Setup & Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd PlaywrightAzureDemo
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Install Playwright browsers:**
    ```bash
    playwright install
    ```

## 🏃‍♂️ Running Tests

### Run all tests (Headless)
Standard mode for CI/CD.
```bash
pytest
```

### Run all tests (Headed / Visual)
Opens the browser window to see the execution.
```bash
pytest --headed
```

### Run specific test file
```bash
python tests/test_login.py
```

### Generate Allure Report
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 🤖 CI/CD (Azure DevOps)

The `azure-pipelines.yml` file is configured to:
1.  Set up Python.
2.  Install dependencies.
3.  Install Playwright browsers.
4.  Run tests and generate Allure results.
5.  Publish test artifacts.

## 🧪 Test Scenarios Covered

*   **Login**: Valid login, Locked out user, Invalid credentials, Empty fields.
*   **Inventory**: Sorting (Low to High), Logout, Reset App State.
*   **Cart**: Add to cart, Remove from cart, Verify items, Continue shopping.
*   **Checkout**: Complete purchase flow, Form field validations (required fields).

---
*Created for Portfolio Demonstration*
