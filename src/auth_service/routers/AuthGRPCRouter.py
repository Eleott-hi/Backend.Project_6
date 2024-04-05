import grpc
import proto.auth.auth_pb2 as auth_pb2
import proto.auth.auth_pb2_grpc as auth_pb2_grpc

from database.database import AsyncSession
from database.Models.Models import User

from services.JWT import JWT
from services.utils import convert,  session_decorator, user_decorator, user_or_none_decorator
from services.pwd_context import PWDContext
import services.schemas as schemas


class AuthenticationServicer(auth_pb2_grpc.AuthenticationServicer):
    def __init__(self) -> None:
        super().__init__()
        self.pwd_context = PWDContext()
        self.jwt = JWT()

    @convert(to=schemas.RegistrationRequest)
    @session_decorator
    @user_or_none_decorator
    async def Registration(
        self,
        request: schemas.RegistrationRequest,
        context,
        session: AsyncSession | None = None,
        user: User | None = None,
    ):
        if user:
            context.set_code(grpc.StatusCode.ALREADY_EXISTS)
            context.set_details(
                "A user with such email already exists")
            return auth_pb2.RegistrationResponse()

        user = User(
            name=request.name,
            surname=request.surname,
            email=request.email,
            phone_number=request.phone_number,
            password_token=self.pwd_context.hash(request.password),
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)
        return auth_pb2.RegistrationResponse(token=self.jwt.get_token())

    @convert(to=schemas.LoginRequest)
    @session_decorator
    @user_decorator
    async def Login(
        self,
        request: schemas.LoginRequest,
        context,
        session: AsyncSession | None = None,
        user: User | None = None,
    ):
        verified = self.pwd_context.verify(
            request.password, user.password_token)

        if not verified:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid password")
            return auth_pb2.LoginResponse()

        return auth_pb2.LoginResponse(token=self.jwt.get_token())

    @convert(to=schemas.ForgotPasswordRequest)
    @session_decorator
    @user_decorator
    async def ForgotPassword(
        self,
        request: schemas.ForgotPasswordRequest,
        context,
        session: AsyncSession | None = None,
        user: User | None = None,
    ):
        password = self.pwd_context.gen_password()
        user.password_token = self.pwd_context.hash(password)
        session.add(user)
        await session.commit()
        await session.refresh(user)

        print(f"New user passwod send to email: {password}", flush=True)

        return auth_pb2.EmptyResponse()

    @convert(to=schemas.ChangePasswordRequest)
    @session_decorator
    @user_decorator
    async def ChangePassword(
        self,
        request: schemas.ChangePasswordRequest,
        context,
        session: AsyncSession | None = None,
        user: User | None = None
    ):
        if not self.pwd_context.verify(request.old_password, user.password_token):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Invalid password")
            return auth_pb2.EmptyResponse()

        user.password_token = self.pwd_context.hash(
            request.new_password
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return auth_pb2.EmptyResponse()

    async def VerifyJWT(self, request, context):
        self.jwt.verify_token(request.token)
        return auth_pb2.EmptyResponse()
