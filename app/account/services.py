from sqlalchemy import select

from .schemas import *
from .models import User
from .utils import passwd, password_match, create_access_token, create_refresh_token
from sqlalchemy.ext.asyncio import AsyncSession
from falcon.http_error import HTTPError


class UserService:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def register_user(self, data: UserRegisterReq) -> User:

        async with self.session_factory() as session:
            session: AsyncSession

            stmt = select(User).where(User.email == data.email)

            user = await session.scalar(stmt)

            if user:
                raise HTTPError(
                    status=400, description="User with this email already exists"
                )

            password = password_match(data.password, data.password2)

            hashed_password = passwd.hash(password)

            new_user = User(
                name=data.name,
                email=data.email,
                hashed_password=hashed_password,
                is_active=False,
                is_customer=data.user_role == "customer",
                is_seller=data.user_role == "seller",
                is_superuser=False,
            )

            session.add(new_user)

            await session.commit()
            await session.refresh(new_user)

            return new_user

    async def authenticate_user(self, data: UserLoginReq):

        async with self.session_factory() as session:
            session: AsyncSession

            stmt = select(User).where(User.email == data.email)

            user = await session.scalar(stmt)

            if not user:
                raise HTTPError(status=400, description="user not found")

            authenticated = passwd.verify(data.password, user.hashed_password)

            if not authenticated:
                raise HTTPError(
                    status=400, description="Email or password is not valid"
                )

            access_token = create_access_token(data={"sub": str(user.id)})
            refresh_token = create_refresh_token(data={"sub": str(user.id)})

            return UserLoginRes(
                msg="Login is successfully done",
                user_role="seller" if user.is_seller else "customer",
                jwt_tokens=JWT_Token(
                    access_token=access_token, refresh_token=refresh_token
                ),
            )

    async def user_profile(self):
        return "PROFILE API SERVICE HIT"
