from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from account.utils import decode_token
from falcon.http_error import HTTPError
from account.models import User

PUBLIC_ROUTES = ["/account/register", "/account/login"]


class JWTMiddleware:

    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def process_request(self, req, resp):

        async with self.session_factory() as session:
            session: AsyncSession

            if req.path in PUBLIC_ROUTES:
                return

            token = req.get_header("Authorization")

            if not token:
                raise HTTPError(status=403, description="Authentication Required")

            if str(token).startswith("Bearer"):
                payload = decode_token(str(token).removeprefix("Bearer "))
            else:
                payload = decode_token(token)

            if not payload or payload is None:
                raise HTTPError(status=400, description="Token payload is invalid")

            token_type = payload.get("type")
            if token_type != "access":
                raise HTTPError(status=400, description="Invalid token type")

            user_id = payload.get("sub")

            stmt = select(User).where(User.id == (user_id))

            user = await session.scalar(stmt)

            if not user:
                raise HTTPError(status=404, description="User not found")

            req.context.user = user
