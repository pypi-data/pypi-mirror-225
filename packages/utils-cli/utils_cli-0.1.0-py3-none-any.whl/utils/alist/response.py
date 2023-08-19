from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    message: str

    @property
    def ok(self) -> bool:
        return self.code == 200 and self.message == "success"


class AuthLoginResponse(BaseResponse):
    class Data(BaseModel):
        token: str

    data: Data


class FsListResponse(BaseResponse):
    pass


class FsPutResponse(BaseResponse):
    pass
