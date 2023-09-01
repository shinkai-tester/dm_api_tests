from faker import Faker

from dm_api_account.models.change_email_model import ChangeEmailModel
from dm_api_account.models.registration_model import RegistrationModel
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi


def test_put_v1_account_email():
    fake = Faker()
    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host="http://5.63.153.31:5051")
    # Create user
    login = "Sasha" + str(fake.random_int(min=1, max=9999))
    registration_data = RegistrationModel(
        login=login,
        email=login + "@example.com",
        password="NewPass1234!"
    )
    api.account.post_v1_account(json=registration_data)

    # Initial activation of user with token
    token = mailhog.get_token_from_last_email()
    api.account.put_v1_account_token(token=token)

    # Change user's email
    json = ChangeEmailModel(
        login=registration_data.login,
        password=registration_data.password,
        email=fake.company_email()
    )
    response_change_email = api.account.put_v1_account_email(json=json)
    assert response_change_email.status_code == 200, (f"Unexpected status code! Expected: 200. Actual: "
                                                      f"{response_change_email.status_code}")
    assert response_change_email.json()['resource']['login'] == registration_data.login

    # It is needed to activate user again after email changing
    upd_token = mailhog.get_token_from_last_email()
    response_activate_after_change = api.account.put_v1_account_token(token=upd_token)
    assert response_activate_after_change.status_code == 200, (f"Unexpected status code! Expected: 200. Actual: "
                                                               f"{response_change_email.status_code}")
    assert response_activate_after_change.json()['resource']['login'] == registration_data.login
