from http import HTTPStatus
from sqlalchemy import select

from fastapi import FastAPI, HTTPException, Depends
from fast_zero.models import User
from fast_zero.schemas import UserDB, UserList, UserPublic, UserSchema, Message
from fast_zero.settings import Settings
from fast_zero.database import get_session

app = FastAPI()

database = []

@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session = Depends(get_session)): #vai executar a função get session e o resultado vai ser passado como argumento session
     db_user = session.scalar(
          select(User).where(
               (User.username == user.username) | (User.email == user.email)
          )    #verifica se ja existe o username e email na base de dados
          )
     if db_user: #caso ja exista alguem com esse username ou email
          if db_user.username == user.username:
               raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Username already exists',
               )
          elif db_user.email == user.email:
               raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail='Email already exists',
               )
          #caso nao exista agora criamos o registro,passaremos tudo que nao eh init false
     db_user = User(
          username = user.username, 
          email = user.email, 
          password = user.password
          )
          
     session.add(db_user)
     session.commit()
     session.refresh(db_user) #atualiza o id
     
     return db_user


@app.get('/users/', response_model=UserList)
def read_users(session = Depends(get_session)): #funçao depende q session seja executada
     return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
#caso o id seja invalido e nao exista
     if user_id < 1 or user_id > len(database): 
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND, detail='User not found'
          )

     user_with_id = UserDB(id=user_id, **user.model_dump()) #criaçao de um novo id
     
     database[user_id - 1] = user_with_id # vai acessar o bd pela posição do id e substituir ele pelos novos valores
     
     return user_with_id

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
     if user_id < 1 or user_id > len(database): 
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND, detail='User not found'
          )
     user_with_id = database[user_id - 1]
     del database[user_id - 1]
     return {'message': 'User deleted'}

#Criar um endpoint GET para pegar um único recurso como users/{id} e fazer os testes(BUSCAR ALGO)

@app.get('/users/{user_id}', response_model=UserPublic)
def search_user(user_id: int):
     if user_id < 1 or user_id > len(database):
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND, detail='User not found'
          )
     user = database[user_id - 1] 
     return user
