import json
import time
from requests import Response
from restclient.restclient import Restclient


class MailhogApi:
    def __init__(self, host='http://5.63.153.31:5025'):
        self.host = host
        self.client = Restclient(host=host, log_enabled=False)

    def get_api_v2_messages(self, limit: int = 50) -> Response:
        """"
        Get messages by limit
        :param limit:
        :return:
        """
        time.sleep(2)
        response = self.client.get(
            path="/api/v2/messages",
            params={
                'limit': limit
            }
        )

        return response

    def get_token_from_last_email(self) -> str:
        """"
        Get user activation token from last email
        :return:
        """
        emails = self.get_api_v2_messages(limit=1).json()
        token_url = json.loads(emails['items'][0]['Content']['Body']).get('ConfirmationLinkUrl')
        token = token_url.split("/")[-1]
        return token

    def get_token_by_login(self, login: str, token_type: str = 'registration', attempt=5):
        if attempt == 0:
            raise AssertionError(f'E-Mail with login {login} can not be found')
        emails = self.get_api_v2_messages(limit=50).json().get('items')
        token_key = "ConfirmationLinkUrl" if token_type == 'registration' else "ConfirmationLinkUri"
        for email in emails:
            user_data = json.loads(email['Content']['Body'])
            if login == user_data.get('Login'):
                token = user_data.get(token_key).split("/")[-1]
                return token
        time.sleep(2)
        return self.get_token_by_login(login=login, token_type=token_type, attempt=attempt - 1)

    def delete_all_messages(self):
        response = self.client.delete(path='/api/v1/messages')
        return response
