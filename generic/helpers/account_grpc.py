from apis.dm_api_account_grpc.account_pb2 import RegisterAccountRequest, LoginRequest
from apis.dm_api_account_grpc.dm_api_account_grpc import DmApiAccountGrpc, step


class AccountGrpc:
    """
    AccountGrpc class to handle user registration and login using gRPC.
    """

    def __init__(self, target):
        """
        Initialize the AccountGrpc instance.

        :param target: The target gRPC server.
        """
        self.grpc_account = DmApiAccountGrpc(target=target)

    @step(
        before_message='Initializing new user registration for {login}...',
        after_message='New user registration completed for {login}.'
    )
    def create_new_user(self, login: str, email: str, password: str):
        """
        Registers a new user account.

        :param login: User login name.
        :param email: User email address.
        :param password: User password.
        :return: Response from the gRPC service.
        """
        response = self.grpc_account.register_account(
            request=RegisterAccountRequest(
                login=login,
                email=email,
                password=password
            )
        )
        return response

    @step(
        before_message='Starting user login process for {login}...',
        after_message='User login process completed for {login}.'
    )
    def login_as_user(self, login: str, password: str, remember_me: bool = True):
        """
        Logs in a user.

        :param login: User login name.
        :param password: User password.
        :param remember_me: Flag to remember the user. Defaults to True.
        :return: Response from the gRPC service.
        """
        response = self.grpc_account.login(
            request=LoginRequest(
                login=login,
                password=password,
                remember_me=remember_me
            )
        )
        return response

    def close(self):
        self.grpc_account.close()
