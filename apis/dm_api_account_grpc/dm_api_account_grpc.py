import uuid
import grpc
import structlog
from google.protobuf.json_format import MessageToDict
from apis.dm_api_account_grpc.account_pb2 import RegisterAccountRequest, LoginRequest
from apis.dm_api_account_grpc.account_pb2_grpc import AccountServiceStub

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(indent=4, sort_keys=True, ensure_ascii=False)
    ]
)


def step(
        before_message: str = '',
        after_message: str = '',
        log_it=True
):
    def wrapper(function):
        def _wrap(*args, **kwargs):
            dynamic_before_message = before_message.format(**kwargs)
            dynamic_after_message = after_message.format(**kwargs)
            if log_it:
                print(f"\n{dynamic_before_message}")
            result = function(*args, **kwargs)
            if log_it:
                print(f"\n{dynamic_after_message}")
            return result

        return _wrap

    return wrapper


def grpc_logging(func):
    def wrapper(self, request, *args, **kwargs):
        log = self.log.bind(event_id=str(uuid.uuid4()))
        method = func.__name__
        if self.log_enabled:
            log.msg(
                event='request',
                method=method,
                channel=self.target,
                request=MessageToDict(request)
            )
            try:
                response = func(self, request, *args, **kwargs)
                log.msg(
                    event='response',
                    response=MessageToDict(response)
                )
                return response
            except Exception as e:
                print(f'Error {e}')
                raise

    return wrapper


class DmApiAccountGrpc:
    def __init__(self, target, log_enabled=True):
        self.target = target
        self.channel = grpc.insecure_channel(target=self.target)
        self.client = AccountServiceStub(channel=self.channel)
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='grpc api')
        self.log_enabled = log_enabled

    @grpc_logging
    def register_account(self, request: RegisterAccountRequest):
        response = self.client.RegisterAccount(
            request=request
        )
        return response

    @grpc_logging
    def login(self, request: LoginRequest):
        response = self.client.Login(
            request=request
        )
        return response

    def close(self):
        self.channel.close()
