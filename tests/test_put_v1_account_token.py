from services.dm_api_account import DmApiAccount


def test_put_v1_account_token():
    api = DmApiAccount(host="http://5.63.153.31:5051")
    response = api.account.put_v1_account_token(
        "06b7ddf8-eb1b-4310-924b-dff85a79ac4b"
    )

    assert response.json()["resource"]["login"] == "Sasha1598"
