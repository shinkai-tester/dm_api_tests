from dm_api_account.models import Registration, ChangePassword, ResetPassword, ChangeEmail
from restclient.restclient import step


class Account:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers):
        """
        Update the session headers for the account API client.
        :param headers: Dictionary containing the headers to set.
        :return: None
        """
        self.facade.account_api.client.session.headers.update(headers)

    @step(
        before_message='Initializing new user registration for {login}...',
        after_message='New user registration completed for {login}.'
    )
    def register_new_user(self, login: str, email: str, password: str, status_code: int = 201):
        response = self.facade.account_api.post_v1_account(
            json=Registration(
                login=login,
                email=email,
                password=password
            ),
            expected_status_code=status_code
        )
        return response

    @step(
        before_message='Initializing activation for registered user...',
        after_message='Activation for registered user completed.'
    )
    def activate_registered_user(self, login: str):
        token = self.facade.mailhog.get_token_by_login(login=login)
        response = self.facade.account_api.put_v1_account_token(
            token=token
        )
        return response

    @step(
        before_message='Initiating request to get current user information...',
        after_message='Successfully retrieved current user information.'
    )
    def get_current_user_info(self, **kwargs):
        response = self.facade.account_api.get_v1_account(**kwargs)
        return response

    @step(
        before_message="Initiating password reset for registered user with login: {login} and email: {email}...",
        after_message="Password reset for registered user with login: {login} and email: {email} completed."
    )
    def reset_user_password(self, login: str, email: str):
        response = self.facade.account_api.post_v1_account_password(
            ResetPassword(
                login=login,
                email=email
            )
        )
        return response

    @step(
        before_message="Preparing to change the password for user with login: {login}.",
        after_message="Password for user with login: {login} has been successfully changed."
    )
    def change_user_password(self, login: str, old_password: str, new_password: str):
        token = self.facade.mailhog.get_token_by_login(login=login, token_type='reset')
        response = self.facade.account_api.put_v1_account_password(
            json=ChangePassword(
                login=login,
                token=token,
                old_password=old_password,
                new_password=new_password
            )
        )

        return response

    @step(
        before_message="Preparing to change for {login} email to {email}...",
        after_message="User email has been changed to {email}."
    )
    def change_user_email(self, login: str, password: str, email: str):
        response = self.facade.account_api.put_v1_account_email(
            json=ChangeEmail(
                login=login,
                password=password,
                email=email
            )
        )

        return response
