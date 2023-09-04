from hamcrest import assert_that, has_properties, has_length
from services.dm_api_account import DmApiAccount
from services.mailhog import MailhogApi
from dm_api_account.models.registration_model import Registration
from faker import Faker


def test_post_v1_account():
    fake = Faker()
    mailhog = MailhogApi(host='http://5.63.153.31:5025')
    api = DmApiAccount(host="http://5.63.153.31:5051")
    login = "Sasha" + str(fake.random_int(min=1, max=9999))
    json = Registration(
        login=login,
        email=login + "@example.com",
        password="NewPass1234!"
    )
    api.account.post_v1_account(json=json)

    token = mailhog.get_token_from_last_email()
    response_activate = api.account.put_v1_account_token(token=token)
    assert_that(response_activate.resource, has_properties(
        {
            "login": login,
            "roles": has_length(2),
            "rating": has_properties({
                "enabled": True,
                "quality": 0,
                "quantity": 0
            })
        }
    ))
