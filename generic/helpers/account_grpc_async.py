from apis.dm_api_account_grpc_async import RegisterAccountRequest, LoginRequest
from apis.dm_api_account_grpc_async.dm_api_account_grpc_async import DmApiAccountGrpcAsync


class AccountGrpcAsync:
    """
    AccountGrpcAsync class to handle user registration and login using asynchronous gRPC.
    """

    def __init__(self, host, port):
        """
        Initialize the AccountGrpcAsync instance.

        :param host: The target gRPC server host.
        :param port: The target gRPC server port.
        """
        self.grpc_account = DmApiAccountGrpcAsync(host=host, port=port)

    async def create_new_user(self, login: str, email: str, password: str):
        """
        Asynchronously registers a new user account.

        :param login: User login name.
        :param email: User email address.
        :param password: User password.
        :return: Response from the asynchronous gRPC service.
        """
        response = await self.grpc_account.register_account(
            request=RegisterAccountRequest(
                login=login,
                email=email,
                password=password
            )
        )
        return response

    async def login_as_user(self, login: str, password: str, remember_me: bool = True):
        """
        Asynchronously logs in a user.

        :param login: User login name.
        :param password: User password.
        :param remember_me: Flag to remember the user. Defaults to True.
        :return: Response from the asynchronous gRPC service.
        """
        response = await self.grpc_account.login(
            request=LoginRequest(
                login=login,
                password=password,
                remember_me=remember_me
            )
        )
        return response

    def close(self):
        """
        Closes the gRPC channel.
        """
        self.grpc_account.close()
