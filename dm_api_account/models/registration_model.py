from faker import Faker

fake = Faker()

login = "Sasha" + str(fake.random_int(min=1, max=9999))

registration_model = {
    "login": login,
    "email": f"{login}@example.com",
    "password": "NewPass1234!"
}


def prepare_registration_data():
    return registration_model
