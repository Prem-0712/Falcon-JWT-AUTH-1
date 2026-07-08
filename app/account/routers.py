from .schemas import UserRegisterReq, UserRegisterRes, UserLoginReq, UserProfileRes


class RegisterRouter:

    def __init__(self, service):
        self.service = service

    async def on_post(self, req, resp):

        body = await req.get_media()

        data = UserRegisterReq.model_validate(body)

        await self.service.register_user(data)

        response = UserRegisterRes(msg="Registration is successfully done !")

        resp.media = response.model_dump()


class LoginRouter:

    def __init__(self, service):

        self.service = service

    async def on_post(self, req, resp):
        body = await req.get_media()

        data = UserLoginReq.model_validate(body)

        response = await self.service.authenticate_user(data)

        resp.media = response.model_dump()


class ProfileRouter:

    def __init__(self, service):
        self.service = service

    async def on_get(self, req, resp):
        current_user = req.context.user

        response = UserProfileRes.model_validate(current_user)

        resp.media = response.model_dump(mode="json")
