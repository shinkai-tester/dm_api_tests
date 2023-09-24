# `dm_api_tests` Framework Documentation 🛠️

## 🌐 Overview
`dm_api_tests` is a testing framework specifically tailored for DM.API Account, a component responsible for account management. This framework uses a range of libraries, tools, and architectural decisions to streamline and facilitate the testing process.

## 📜 Table of Contents
- [🔗 Swagger Documentation](#swagger-documentation)
- [🚀 Installation & Setup](#installation--setup)
- [🧰 Technologies and Libraries](#technologies-and-libraries)
- [📂 Project Structure](#project-structure)
- [🏛️ Architectural Highlights](#architectural-highlights)
- [🛠️ Configuration](#configuration)
- [📊 Generating Allure Reports](#generating-allure-reports)

## 🔗 Swagger Documentation
For a detailed breakdown of the API endpoints, refer to the [Swagger documentation](http://5.63.153.31:5051/index.html?urls.primaryName=Account).

## 🚀 Installation & Setup
Clone, setup, and launch with:

```bash
git clone https://github.com/shinkai-tester/dm_api_tests.git
pip install -r requirements.txt
```

## 🧰 Technologies and Libraries
- **Pytest**: The backbone for all testing needs.
- **Allure**: Provides enhanced reporting capabilities integrated throughout the project.
- **SQLAlchemy**: Used for ORM-based database interactions.
- **Requests**: Handles HTTP requests.
- **JSON**: Manages data in JSON format.
- **MailHog API**: Retrieves email data for tests.

## 📂 Project Structure

Explore the well-organized and intuitive structure of the project:

- **`apis/`**: This directory houses all APIs that interact within this framework.

- **`common_libs/`**: Here, you'll find universal libraries, including logging clients, designed for reuse across various modules.

- **`config/`**: This is the home for environment configuration files that tailor the test execution environment.

- **`data/`**: Within this directory, you'll discover data generation utilities, including Faker, ensuring dynamic data for your tests.

- **`services/`**: These are the entry points or facades for various APIs, especially useful for seamless integration when dealing with multiple APIs.

- **`tests/`**: A vast collection of tests, meticulously categorized by individual controllers.

- **`generic/`**: This directory contains common helper classes and verifications.

  - **`assertions/`**: A dedicated space for validations, encompassing checks from generic to test-specific.

  - **`helpers/`**: This package is enriched with helper classes, ensuring smooth test executions and auxiliary operations.


## 🏛️ Architectural Highlights
- **Modular Design**: Encapsulates different components within specific directories and classes.
- **ORM (Object Relational Mapping)**: The `orm_db.py` uses SQLAlchemy for database interactions. Functions like `get_all_users`, `delete_user_by_login`, etc., abstract the complexities of direct SQL queries.
- **API Models**: The `apis/` directory contains modules specific to endpoints. Classes such as `LoginApi` and `AccountApi` connect to the DM.API Account service for tasks like user login and account details retrieval.
- **Service Facade**: The `services/` directory uses a facade pattern. The `Facade` class in `dm_api_account.py` groups multiple services, streamlining the interaction among different components.
- **Data Models**: `generic/helpers/orm_models.py` provides structured representations of all database tables, enabling ORM interactions and ensuring type safety and structure. These models are generated using `sqlacodegen`.
- **Allure Integration**: Allure is integrated across the project. Functions in various files, including tests like `TestPostV1Account`, use `@allure.step` and other annotations for improved report clarity. Methods such as `allure_attach` are employed for attaching database queries, REST API requests and responses.

## 🛠️ Configuration
Configurations pertaining to environments and primary connections are managed in a config file, making modifications straightforward without altering core code.

## 📊 Generating Allure Reports
To visualize test results (`test_post_v1_account.py` showcased here):

```bash
pytest tests/tests_account/test_post_v1_account.py --alluredir=./allure-results
allure generate -c ./allure-results -o ./allure-report 
allure serve
```