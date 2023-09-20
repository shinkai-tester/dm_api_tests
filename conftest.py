from collections import namedtuple
from pathlib import Path

import allure
import pytest
import structlog
from vyper import v
import os

from generic.assertions.assertions import Assertions
from generic.helpers.data_generator import DataGeneratorHelper
from generic.helpers.dm_db import DmDatabase
from generic.helpers.mailhog import MailhogApi
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

# Setting up the structlog configuration to render logs in JSON format.
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog():
    """Fixture to set up the Mailhog API connection."""
    return MailhogApi(host=v.get('service.mailhog'))


@pytest.fixture
def dm_api_facade(mailhog):
    """Fixture to set up the facade for dm_api_account service."""
    return Facade(
        host=v.get('service.dm_api_account'),
        mailhog=mailhog
    )


@pytest.fixture
def orm_db():
    """Fixture to set up the ORM database connection."""
    db = OrmDatabase(
        user=v.get('database.dm3_5.user'),
        password=v.get('database.dm3_5.password'),
        host=v.get('database.dm3_5.host'),
        database=v.get('database.dm3_5.database')
    )
    yield db
    db.db.close_connection()


connect = None


@pytest.fixture
def dm_db():
    global connect
    if connect is None:
        connect = DmDatabase(
            user=v.get('database.dm3_5.user'),
            password=v.get('database.dm3_5.password'),
            host=v.get('database.dm3_5.host'),
            database=v.get('database.dm3_5.database'))
    yield connect
    connect.db.db.close()


@pytest.fixture
def data_helper():
    """Fixture to set up the Data Generator Helper."""
    return DataGeneratorHelper()


@pytest.fixture()
def assertions(orm_db):
    """Fixture to set up assertions using ORM database."""
    return Assertions(orm_db)


@allure.step("Preparation of user data")
@pytest.fixture
def prepare_user(dm_api_facade, orm_db, data_helper):
    """Fixture to prepare a user for tests."""
    pattern = "Shurka%"
    orm_db.delete_users_by_login_pattern(pattern=pattern)
    get_users_from_db = orm_db.get_users_by_login_pattern(pattern=pattern)
    assert len(get_users_from_db) == 0, f'User(s) with pattern {pattern} exist in DB'
    dm_api_facade.mailhog.delete_all_messages()
    login = data_helper.generate_login()
    password = data_helper.generate_password()
    email = data_helper.generate_email_with_login()
    user = namedtuple('User', 'login, email, password')
    User = user(login=login, email=email, password=password)
    return User


@pytest.fixture()
def cleanup_user_and_emails(dm_api_facade, orm_db, login):
    """Fixture to clean up user and emails post tests."""
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()


# List of options that can be overridden from the command line.
options = (
    'service.dm_api_account',
    'service.mailhog',
    'database.dm3_5.host'
)


@pytest.fixture(autouse=True)
def set_config(request):
    """
    Auto-used fixture to set up the configuration.

    This fixture performs the following:
    - Sets up the path to the configuration file.
    - Reads the --env option from the command line or uses 'stg' as default.
      This sets the environment (e.g., staging, production) for which the configuration will be loaded.
    - Reads the corresponding configuration file based on the environment.
    - Overwrites specific options from the configuration using values provided from the command line if any.

    Command-line overwrites:
    1. The --env value is fetched using `request.config.getoption('--env')`.
       If not provided, the default value 'stg' is used.
    2. For each option in the `options` list, the fixture tries to fetch its value from the command line.
       If provided, it will overwrite the corresponding value in the configuration.
       Otherwise, the value from the config file remains unchanged.
    """
    config = Path(__file__).parent.joinpath('config')
    config_name = request.config.getoption('--env')
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(option, request.config.getoption(f'--{option}'))


def pytest_addoption(parser):
    """Function to add custom command line options.

    This adds:
    - --env option, with a default of 'stg'.
    - Specific options listed in 'options' variable to allow them to be overridden from the command line.
    """
    parser.addoption('--env', action='store', default='stg')
    for option in options:
        parser.addoption(f'--{option}', action='store', default=None)


@pytest.fixture(autouse=True)
def set_allure_environment(request, set_config):
    environment = request.config.getoption('--env')
    allure_dir = request.config.getoption('--alluredir')

    dm_api_account = v.get('service.dm_api_account')
    mailhog = v.get('service.mailhog')
    db_host = v.get('database.dm3_5.host')

    with open(os.path.join(allure_dir, 'environment.properties'), 'w') as f:
        f.write(f"Environment={environment}\n")
        f.write(f"DM_API_Account={dm_api_account}\n")
        f.write(f"Mailhog={mailhog}\n")
        f.write(f"DB_Host={db_host}\n")
