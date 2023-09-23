from faker import Faker


class DataGeneratorHelper:
    def __init__(self):
        self.faker = Faker()

    def generate_email_with_login(self):
        email = self.generate_login() + "@example.com"
        return email

    def generate_email(self):
        return self.faker.company_email()

    def generate_password(self):
        return self.faker.password()

    def generate_login(self):
        login = "Shurka" + str(self.faker.random_int(min=1, max=9999))
        return login
