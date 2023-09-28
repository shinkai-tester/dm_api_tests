from dm_api_account.models import *
from restclient.restclient import step


class Login:
    def __init__(self, facade):
        from services.dm_api_account import Facade
        self.facade: Facade = facade

    def set_headers(self, headers):
        """
        Update the session headers for the login API client.
        :param headers: Dictionary containing the headers to set.
        :return: None
        """
        self.facade.login_api.client.session.headers.update(headers)

    @step(
        before_message='Starting user login process for {login}...',
        after_message='User login process completed for {login}.'
    )
    def login_user(self, login: str, password: str, remember_me: bool = True):
        response = self.facade.login_api.v1_account_login_post(
            _return_http_data_only=False,
            login_credentials=LoginCredentials(
                login=login,
                password=password,
                remember_me=remember_me
            )
        )
        return response

    def get_auth_token(self, login: str, password: str, remember_me: bool = True):
        response = self.login_user(
            login=login,
            password=password,
            remember_me=remember_me
        )
        token = response[2]['X-Dm-Auth-Token']
        return token

    @step(
        before_message="Initiating user logout process...",
        after_message="User logout process completed."
    )
    def logout_user(self, x_dm_auth_token: str, **kwargs):
        response = self.facade.login_api.v1_account_login_delete(
            x_dm_auth_token=x_dm_auth_token,
            **kwargs
        )
        return response

    @step(
        before_message="Initiating logout from all devices...",
        after_message="Logout from all devices completed."
    )
    def logout_user_from_all_devices(self, x_dm_auth_token: str, **kwargs):
        response = self.facade.login_api.v1_account_login_all_delete(
            x_dm_auth_token=x_dm_auth_token,
            **kwargs
        )
        return response
