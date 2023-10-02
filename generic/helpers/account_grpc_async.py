from apis.dm_api_account_grpc_async import RegisterAccountRequest, LoginRequest
from apis.dm_api_account_grpc_async.dm_api_account_grpc_async import DmApiAccountGrpcAsync


class AccountGrpcAsync:
    def __init__(self, host, port):
        self.grpc_account = DmApiAccountGrpcAsync(host=host, port=port)

    async def create_new_user(self, login: str, email: str, password: str):
        response = await self.grpc_account.register_account(
            request=RegisterAccountRequest(
                login=login,
                email=email,
                password=password
            )
        )
        return response

    async def login_as_user(self, login: str, password: str, remember_me: bool = True):
        response = await self.grpc_account.login(
            request=LoginRequest(
                login=login,
                password=password,
                remember_me=remember_me
            )
        )
        return response

    def close(self):
        self.grpc_account.close()
