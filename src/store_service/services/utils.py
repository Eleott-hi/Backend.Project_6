import grpc
from config import AUTH_SERVICE
import proto.auth.auth_pb2_grpc as auth_pb2_grpc
from fastapi import status,  HTTPException


def handle_grpc_exceptions(e: grpc.RpcError):
    match e.code():
        case grpc.StatusCode.INVALID_ARGUMENT:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=e.details(),
            )
        case grpc.StatusCode.UNAUTHENTICATED:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=e.details(),
            )
        case grpc.StatusCode.PERMISSION_DENIED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=e.details(),
            )
        case grpc.StatusCode.NOT_FOUND:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.details(),
            )
        case  grpc.StatusCode.ALREADY_EXISTS:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=e.details(),
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.details(),
            )


async def get_auth_grpc_stub():
    try:
        async with grpc.aio.insecure_channel(AUTH_SERVICE) as channel:
            stub = auth_pb2_grpc.AuthenticationStub(channel)
            yield stub

    except grpc.RpcError as e:
        handle_grpc_exceptions(e)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e,
        )
