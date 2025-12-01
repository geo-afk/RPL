from pydantic import BaseModel, EmailStr


class UserDetailsSaveRequest(BaseModel):
    first_name: str
    username: str
    last_name: str
    password: str
    email: EmailStr



class UserOut(BaseModel):
    id: int
    username: str
    email: str | None = None
    role: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserOut