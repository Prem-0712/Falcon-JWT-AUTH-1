from falcon import asgi
from core.container import Container
from core.middleware import JWTMiddleware

container = Container()

app = asgi.App(middleware=[container.jwt_middleware()])

app.add_route("/account/register", container.register_router())
app.add_route("/account/login", container.login_router())
app.add_route("/account/profile", container.profile_router())
