# OpenCart UI Test Suite

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green)
![Pytest](https://img.shields.io/badge/Pytest-7.x-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

This is a demo UI test automation framework for OpenCart, built to showcase modern test automation practices. It's designed for my GitHub profile as a portfolio piece, demonstrating skills in Selenium, Pytest, containerized testing with Selenoid, and CI/CD integration. The framework focuses on key features like parallel execution, robust logging, and failure reporting, without extensive test cases (as it's a demo).

## Features
- **Page Object Model (POM):** Modular page classes for maintainability (e.g., `LoginPage`, `ProductPage`).
- **Multi-Environment Support:** Configurable for QA, UAT, and Prod via `config.yaml`.
- **Selenoid Integration:** Containerized remote browser testing with multiple versions (Chrome, Firefox, Edge) and VNC support.
- **Parallel Execution:** Supports `pytest-xdist` for running tests in parallel.
- **Logging:** Configurable logging for sequential and parallel runs, with dynamic file generation.
- **Reporting:** HTML reports with screenshots on failure (via `pytest-html` and optional Allure integration).
- **Data-Driven Testing:** Parameterized tests using CSV and constants.
- **Retry Mechanisms:** Handled via Pytest command-line args (e.g., `--last-failed`, `--reruns`).
- **CI/CD:** Jenkins freestyle job integrated; pipeline is a work-in-progress.
- **Utilities:** Custom helpers for elements, JavaScript, waits, and exceptions.

## Tech Stack
- **Language:** Python 3.8+
- **Testing Framework:** Pytest
- **Automation Library:** Selenium WebDriver
- **Containerization:** Docker (for Selenoid)
- **Reporting:** pytest-html, Allure (optional)
- **Other Libraries:** assertpy, PyYAML, pytest-xdist

## Prerequisites
- Python 3.8+ installed.
- Docker installed (for Selenoid).
- Optional: Jenkins for CI/CD.

## Setup
1. **Clone the Repository:**
   ```
   git clone https://github.com/yourusername/opencart-ui-test-suite.git
   cd opencart-ui-test-suite
   ```

2. **Install Dependencies:**
   Create a virtual environment and install requirements:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt  # Create this file with: selenium, pytest, pytest-html, pytest-xdist, assertpy, pyyaml, allure-pytest
   ```

3. **Set Up Selenoid:**
   - Navigate to `selenoid/` and start the containers:
     ```
     docker-compose up -d
     ```
   - Access Selenoid UI at `http://localhost:8080`.
   - Update `configs/config.yaml` to enable remote mode if needed:
     ```
     remote:
       enabled: true
       remote_url: "http://localhost:4444/wd/hub"
     ```

4. **Configure Environment:**
   - Set the `TEST_ENV` environment variable (default: `qa`):
     ```
     export TEST_ENV=qa  # On Windows: set TEST_ENV=qa
     ```
   - Customize `configs/config.yaml` for browsers, URLs, credentials, etc.

## Running Tests
- **Sequential Run:**
  ```
  pytest tests/
  ```

- **Parallel Run:**
  ```
  pytest tests/ -n auto --dist loadscope
  ```

- **With Retries:**
  ```
  pytest tests/ --reruns 3 --reruns-delay 2  # Requires pytest-rerunfailures plugin
  ```

- **Specific Tests:**
  ```
  pytest tests/test_login_page.py
  ```

- **Generate HTML Report:**
  ```
  pytest tests/ --html=reports/report.html --self-contained-html
  ```
  Reports are saved in `reports/` with timestamps; check `latest.html` for the most recent.

- **View Logs:**
  Logs are generated in `logs/` with timestamps (e.g., `test_YYYYMMDD_HHMMSS.log`). In parallel mode, each worker gets its own file.

## Project Structure
```
opencart_ui_test_suite/
├── configs/              # Configuration files (YAML)
├── constants/            # App constants and test data
├── logs/                 # Generated log files
├── pages/                # Page Object Model classes
├── reports/              # Test reports and assets (screenshots)
├── selenoid/             # Selenoid Docker setup
├── test_data/            # CSV data for tests
├── tests/                # Pytest tests and conftest.py
├── utils/                # Utility modules (driver factory, elements, etc.)
├── pytest.ini            # Pytest configuration
└── README.md             # This file
```

## Jenkins Integration
- A freestyle job is set up for basic CI/CD (e.g., triggering tests on commits).
- Pipeline integration is WIP—feel free to contribute!

## Contributing
This is a demo project, but contributions are welcome! Fork the repo, create a branch, and submit a pull request.

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Built by [Your Name/Username]. Check out my GitHub for more projects!
