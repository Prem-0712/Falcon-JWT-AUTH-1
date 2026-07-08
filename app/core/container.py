from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Object, Factory
from db.config import SessionLocal
from account.services import UserService
from account.routers import RegisterRouter, LoginRouter, ProfileRouter
from core.middleware import JWTMiddleware


class Container(DeclarativeContainer):

    session_factory = Object(SessionLocal)

    user_service = Factory(UserService, session_factory=session_factory)

    register_router = Factory(RegisterRouter, service=user_service)

    login_router = Factory(LoginRouter, service=user_service)

    profile_router = Factory(ProfileRouter, service=user_service)

    jwt_middleware = Factory(JWTMiddleware, session_factory = session_factory)
