from collections import namedtuple
import pytest
import structlog
from generic.assertions.assertions import Assertions
from generic.helpers.data_generator import DataGeneratorHelper
from generic.helpers.mailhog import MailhogApi
from generic.helpers.orm_db import OrmDatabase
from services.dm_api_account import Facade

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


@pytest.fixture
def mailhog():
    return MailhogApi(host='http://5.63.153.31:5025')


@pytest.fixture
def dm_api_facade(mailhog):
    return Facade(host="http://5.63.153.31:5051", mailhog=mailhog)


@pytest.fixture
def orm_db():
    db = OrmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')
    return db


@pytest.fixture
def data_helper():
    return DataGeneratorHelper()


@pytest.fixture()
def assertions(orm_db):
    return Assertions(orm_db)


@pytest.fixture
def prepare_user(dm_api_facade, orm_db, data_helper):
    login = data_helper.generate_login()
    password = data_helper.generate_password()
    email = data_helper.generate_email_with_login()
    user = namedtuple('User', 'login, email, password')
    User = user(login=login, email=email, password=password)

    yield User

    orm_db.delete_user_by_login(login=User.login)
    get_user_from_db = orm_db.get_user_by_login(login=User.login)
    assert len(get_user_from_db) == 0, f'User with {User.login} is not deleted'
    dm_api_facade.mailhog.delete_all_messages()


@pytest.fixture()
def cleanup_user_and_emails(dm_api_facade, orm_db, login):
    orm_db.delete_user_by_login(login=login)
    dm_api_facade.mailhog.delete_all_messages()
