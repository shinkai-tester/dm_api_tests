import time
from generic.helpers.data_generator import DataGeneratorHelper
from generic.helpers.dm_db import DmDatabase
from services.dm_api_account import Facade


def test_post_v1_account():
    """Test the registration and activation of a new user, and assert their initial properties."""

    # Initialize data helper, API client and database client
    data_helper = DataGeneratorHelper()
    api = Facade(host="http://5.63.153.31:5051")
    db = DmDatabase(user='postgres', password='admin', host='5.63.153.31', database='dm3.5')

    # Register new user
    login = data_helper.generate_login()
    password = data_helper.generate_password()
    email = data_helper.generate_email_with_login()

    api.account.register_new_user(
        login=login,
        email=email,
        password=password
    )

    dataset = db.get_user_by_login(login=login)
    for row in dataset:
        assert row['Login'] == login, f'User {login} is not registered'
        assert row['Activated'] is False, f'User {login} is already activated'

    # Activate registered user using DB
    db.set_activated_flag_by_login(login=login)
    activated_dataset = db.get_user_by_login(login=login)
    time.sleep(2)
    for row in activated_dataset:
        assert row['Activated'] is True, f'User {login} is not activated'

    # Login as user
    api.login.login_user(
        login=login,
        password=password
    )

    # Delete user, delete emails - cleanup data
    db.delete_user_by_login(login=login)
    get_user_from_db = db.get_user_by_login(login=login)
    assert len(get_user_from_db) == 0, f'User with {login} is not deleted'
    api.mailhog.delete_all_messages()
