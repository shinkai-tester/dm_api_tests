from dm_api_account.models import registration_model
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_post_v1_account_login():
    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host="http://5.63.153.31:5051")
    # Create user
    registration_data = registration_model.prepare_registration_data()
    api.account.post_v1_account(json=registration_data)

    # Initial activation of user with token
    token = mailhog.get_token_from_last_email()
    api.account.put_v1_account_token(token=token)

    # Login as user
    credentials = {
        "login": registration_data['login'],
        "password": registration_data['password'],
        "rememberMe": True
    }
    response_login = api.login.post_v1_account_login(json=credentials)
    assert response_login.json()['resource']['login'] == registration_data['login']
