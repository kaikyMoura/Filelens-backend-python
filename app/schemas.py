from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    username: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    password: str


class UserUpdate(UserCreate):
    id: str
    name: str
    username: str
    email: str


class UserRequest(UserBase):
    pass


class UserResponse(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)
