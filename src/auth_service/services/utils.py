import grpc
from typing import Any

from database.Models.Models import User
from database.database import select, async_session

from services.converter import Converter

converter = Converter()


async def get_user_by_email(email, session):
    q = select(User).where(User.email == email)
    user = (await session.exec(q)).first()
    return user


def convert(to: Any):
    if to not in converter.mapper:
        raise ValueError(f"No such cls type in converter mapper: {to}")

    def decorator(func):
        async def wrapper(self, request, context):
            try:
                request = converter.convert_to(request, to)
                response = await func(self, request, context)
                return response

            except ValueError as e:
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(str(e))

        return wrapper

    return decorator


def session_decorator(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            return await func(*args, **kwargs, session=session)

    return wrapper


def user_or_none_decorator(func):
    async def wrapper(*args, **kwargs):
        self, request, context = args
        user = await get_user_by_email(request.email, kwargs["session"])
        res = await func(*args, **kwargs, user=user)
        return res

    return wrapper


def user_decorator(func):
    async def wrapper(*args, **kwargs):
        self, request, context = args
        user = await get_user_by_email(request.email, kwargs["session"])

        if user is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return

        res = await func(*args, **kwargs, user=user)
        return res

    return wrapper
