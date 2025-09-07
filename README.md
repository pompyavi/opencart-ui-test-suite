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
- **CI/CD:** Jenkins pipeline integrated via `Jenkinsfile` (multi-env, browser/version params, optional remote via Selenoid, parallel execution, and report publishing).
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
     docker-compose up -d  # or: docker compose up -d
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

- **Remote (Selenoid):**
  ```
  pytest tests --remote --browser chrome --browser_version latest -n auto --dist loadscope
  ```

- **With Retries:**
  ```
  pytest tests --reruns 3 --reruns-delay 2  # Requires pytest-rerunfailures plugin
  ```

- **Specific Tests:**
  ```
  pytest tests/test_login_page.py
  ```

- **Generate HTML Report:**
  ```
  pytest tests --html=reports/report.html --self-contained-html
  ```
  Reports are saved in `reports/` with timestamps; check `latest.html` for the most recent.

- **View Logs:**
  Logs are generated in `logs/` with timestamps (e.g., `test_YYYYMMDD_HHMMSS.log`). In parallel mode, each worker gets its own file.

## Project Structure

```text
opencart_ui_test_suite/
├── configs/              # Configuration files (YAML)
│   ├── config.yaml
│   └── logger_config.yaml
├── constants/            # App constants and test data
│   ├── app_constants.py
│   └── test_data.py
├── logs/                 # Generated log files (timestamped)
├── pages/                # Page Object Model classes
│   ├── account_page.py
│   ├── common_components.py
│   ├── login_page.py
│   ├── product_page.py
│   ├── search_result_page.py
│   └── user_registration_page.py
├── reports/              # Test reports and assets (generated)
│   ├── assets/
│   ├── latest.html
│   └── report_*.html
├── selenoid/             # Selenoid Docker setup
│   ├── docker-compose.yml
│   └── browsers.json
├── test_data/
│   └── user_registration_data.csv
├── tests/                # Pytest tests and configuration
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_account_page.py
│   ├── test_login_page.py
│   ├── test_product_page.py
│   ├── test_search_result_page.py
│   └── test_user_registration_page.py
├── utils/                # Utility modules
│   ├── config_reader.py
│   ├── csv_reader.py
│   ├── element_util.py
│   ├── framework_exception.py
│   ├── javascript_util.py
│   └── driver_factory/
│       ├── browser_options_manager.py
│       └── driver_manager.py
├── Jenkinsfile
├── pytest.ini
├── requirements.txt
└── README.md
```

## Jenkins Integration
- Declarative pipeline integrated via `Jenkinsfile`.
- Triggers on GitHub push (requires webhook to `/github-webhook/`).
- Publishes JUnit, Allure, and HTML reports and archives all artifacts.
- Runs on a Windows agent (uses `bat` and `docker desktop start`).

**Pipeline parameters:**
- `TEST_ENV`: qa | uat | prod (sets configuration and URLs).
- `browser`: chrome | firefox.
- `browser_version`: e.g., `latest`, `126`.
- `REMOTE`: true/false (start Selenoid and run remotely).
- `MARK`: optional pytest `-m` expression.

**Required Jenkins plugins:**
- Pipeline
- Git / GitHub Integration
- Allure Jenkins Plugin (for Allure results)
- HTML Publisher

**How to run:**
1. Create a Pipeline job -> Pipeline script from SCM -> point to this repo and branch.
2. Ensure it runs on a node labeled `windows` with Docker Desktop installed and logged in.
3. (Optional) Configure a GitHub webhook to trigger on push.
4. Build with parameters; view 'Pytest HTML Report', Allure, and JUnit trend on the job page.

> Note: To use a Linux agent, adapt the `Jenkinsfile` (replace `agent { label 'windows' }`, convert `bat` to `sh`, and remove `docker desktop start`).

## Contributing
This is a demo project, but contributions are welcome! Fork the repo, create a branch, and submit a pull request.



