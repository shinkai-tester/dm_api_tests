from faker import Faker

fake = Faker()

change_email_model = {
    "login": "<string>",
    "password": "<string>",
    "email": "<string>"
}


def get_new_email():
    return fake.company_email()
