from fastapi import APIRouter, status,  HTTPException, Request, Depends, Response
from services.JWTBearer import JWTBearer
from fastapi.responses import JSONResponse

import grpc
from proto.auth import auth_pb2
from routers.schemas import RegistrationRequest, LoginRequest, ChangePasswordRequest, ForgotPasswordRequest
from services.utils import get_auth_grpc_stub


class AuthRouter():
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Authentication"])

        @self.router.post("/register", status_code=status.HTTP_201_CREATED)
        async def register(
            request: RegistrationRequest,
            auth_stub=Depends(get_auth_grpc_stub),
        ) -> JSONResponse:
            """
            Register new

            Parameters:
            - `request`: `RegistrationRequest` object containing client data.

            Returns:
            - none
            """

            response: auth_pb2.RegistrationResponse = await auth_stub.Registration(
                auth_pb2.RegistrationRequest(**request.model_dump())
            )

            res = Response(status_code=status.HTTP_201_CREATED)
            res.set_cookie(key="JWToken", value=response.token, httponly=True,)

            return res

        @self.router.post("/login")
        async def login(
            request: LoginRequest,
            auth_stub=Depends(get_auth_grpc_stub),
        ) -> dict:
            """
            Login

            Parameters:
            - `request`: `LoginRequest` object containing client data.

            Returns:
            - none
            """
            response: auth_pb2.RegistrationResponse = await auth_stub.Login(
                auth_pb2.LoginRequest(**request.model_dump())
            )

            res = Response()
            res.set_cookie(key="JWToken", value=response.token, httponly=True)

            return res

        @self.router.post("/forgot-password")
        async def forgot_password(
            request: ForgotPasswordRequest,
            auth_stub=Depends(get_auth_grpc_stub),
        ) -> dict:
            """
            Forgot password

            Parameters:
            - `request`: `ForgotPasswordRequest` object containing client data.

            Returns:
            - 
            """
            response: auth_pb2.RegistrationResponse = await auth_stub.ForgotPassword(
                auth_pb2.ForgotPasswordRequest(**request.model_dump())
            )

        @self.router.post("/change-password", dependencies=[Depends(JWTBearer())])
        async def change_password(
            request: ChangePasswordRequest,
            auth_stub=Depends(get_auth_grpc_stub),
        ) -> str:
            """
            Change password

            Parameters:
            - `request`: `ChangePasswordRequest` object containing client data.

            Returns:
            - `JSONResponse` object containing token.
            """
            response = await auth_stub.ChangePassword(
                auth_pb2.ChangePasswordRequest(**request.model_dump())
            )

            return "Password changed"
