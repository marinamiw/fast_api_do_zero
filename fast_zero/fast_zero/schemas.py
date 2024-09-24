from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str



class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)  # faz com que consiga ler os atributos da classe, em vez de ser um unico modelo do pydantic, assim conseguimos converter qualquer outro modelo como uma classe do database para esse modelo do schema sem problema


# iremos precisar disso no teste quando formos converter um modelo do sql para saida do teste em pydantic no arquivo test_app
class UserList(BaseModel):
    users: list[UserPublic]
