from pydantic import BaseModel


class UserOut(BaseModel):
    id: str
    token: str
    username: str

    class Config:
        orm_mode = True


class CreateUser(BaseModel):
    id: str
    token: str
    username: str

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    id: str
    token: str
    username: str

    class Config:
        orm_mode = True
