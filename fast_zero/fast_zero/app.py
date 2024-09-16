from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import  UserSchema, UserPublic

app = FastAPI()

database = []


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    
     return user
