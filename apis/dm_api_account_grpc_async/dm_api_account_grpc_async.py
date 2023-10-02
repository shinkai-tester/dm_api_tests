import uuid
from functools import wraps
import structlog
from grpclib.client import Channel

from apis.dm_api_account_grpc_async import LoginRequest, RegisterAccountRequest, AccountServiceStub

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def grpc_logging(func):
    @wraps(func)
    async def wrapper(self, request, *args, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        method = func.__name__
        log.msg(
            event='request',
            method=method,
            channel=f"{self.host}:{self.port}",
            request=request.to_dict()
        )
        try:
            response = await func(self, request, *args, **kwargs)
            log.msg(
                event='response',
                response=response.to_dict()
            )
            return response
        except Exception as e:
            log.msg(
                event='error',
                error=str(e)
            )
            raise

    return wrapper


class DmApiAccountGrpcAsync:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.channel = Channel(host=host, port=port)
        self.client = AccountServiceStub(channel=self.channel)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='grpc api async')

    @grpc_logging
    async def register_account(self, request: RegisterAccountRequest):
        response = await self.client.register_account(
            register_account_request=request
        )
        return response

    @grpc_logging
    async def login(self, request: LoginRequest):  # Made this async for consistency
        response = await self.client.login(
            login_request=request
        )
        return response

    def close(self):
        self.channel.close()
