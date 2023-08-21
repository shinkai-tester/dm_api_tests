from faker import Faker

from services.dm_api_account import DmApiAccount


def test_post_v1_account():
    api = DmApiAccount(host="http://5.63.153.31:5051")
    fake = Faker()
    login = "Sasha" + str(fake.random_int(min=1, max=9999))
    json = {
        "login": login,
        "email": f"{login}@example.com",
        "password": "NewPass1234!"
    }
    response = api.account.post_v1_account(
        json=json
    )

    assert response.status_code == 201, f"Unexpected status code! Expected: 201. Actual: {response.status_code}"
