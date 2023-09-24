# dm_api_tests

This testing framework is designed for DM.API Account, responsible for account management. It includes separate repositories for client libraries:

- [dm_api_account 📦](https://github.com/shinkai-tester/dm_api_account): Client for DM.API Account service.
- [orm_client 📦](https://github.com/shinkai-tester/orm_client): ORM-based database interactions with Allure and Logger.
- [restclient 📦](https://github.com/shinkai-tester/restclient): Restclient with Allure and Logger.
- [db_client 📦](https://github.com/shinkai-tester/db_client): DB client with Logger.

The separation of client libraries into individual repositories offers benefits like better code organization, easier testing, reusability, simpler updates, and improved code quality. It also facilitates the management of responsibilities for each library.

## Project Libraries 📚

This project comprises several libraries, each serving a specific purpose. These libraries have been separated into individual repositories to enhance code management, testing, and reusability across projects.

### dm_api_account 🌐

**Description:** `dm_api_account` is a client library designed for interacting with the DM.API Account service, responsible for managing user accounts. It provides convenient methods for various account operations, including user registration, password reset, email changes, authentication, and more.

### restclient 🌐

**Description:** `restclient` is a client library for making HTTP requests. It provides convenient methods for sending POST, GET, PUT, and DELETE requests to remote servers. Additionally, it integrates with the Allure system for logging requests and responses, facilitating request and response tracking during test execution.

### orm_client 🌐

**Description:** `orm_client` is a client library for interacting with databases using Object Relational Mapping (ORM). It provides convenient methods for executing queries against a database and integrates with the Allure system for logging SQL queries and results.
