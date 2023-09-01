from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from dm_api_account.models.registration_model import RegistrationModel
from faker import Faker


def test_post_v1_account():
    fake = Faker()
    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host="http://5.63.153.31:5051")
    login = "Sasha" + str(fake.random_int(min=1, max=9999))
    json = RegistrationModel(
        login=login,
        email=login + "@example.com",
        password="NewPass1234!"
    )
    response_user_create = api.account.post_v1_account(json=json)

    assert response_user_create.status_code == 201, (f"Unexpected status code! Expected: 201. Actual: "
                                                     f"{response_user_create.status_code}")

    token = mailhog.get_token_from_last_email()
    response_activate = api.account.put_v1_account_token(token=token)
    assert response_activate.json()["resource"]["login"] == json.login
