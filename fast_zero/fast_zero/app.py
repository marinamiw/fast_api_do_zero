from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserPublic, UserSchema

app = FastAPI()



@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):  # vai executar a função get session e o resultado vai ser passado como argumento session
     db_user = session.scalar(
          select(User).where(
               (User.username == user.username) | (User.email == user.email)
          )    # verifica se ja existe o username e email na base de dados
          )
     if db_user:  # caso ja exista alguem com esse username ou email
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
          # caso nao exista agora criamos o registro,passaremos tudo que nao eh init false
     db_user = User(
          username=user.username,
          email=user.email,
          password=user.password
          )

     session.add(db_user)
     session.commit()
     session.refresh(db_user)  # atualiza o id

     return db_user


@app.get('/users/', response_model=UserList)
def read_users(limit: int = 10, skip: int = 0, session: Session = Depends(get_session)):  # funçao depende q session seja executada
     user = session.scalars(
          select(User).limit(limit).offset(skip)
          )
     return {'users': user}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema, session: Session = Depends(get_session)):
     
     db_user = session.scalar(
          select(User).where(User.id == user_id)
     )

     if not db_user:
        raise HTTPException(
             status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
     db_user.email = user.email
     db_user.username = user.username
     db_user.password = user.password

     session.add(db_user)
     session.commit()
     session.refresh(db_user) #retorna esse usuario atualizado no teste

     return db_user

@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):

   db_user = session.scalar(
        select(User).where(User.id == user_id)
   )

   if not db_user:
        raise HTTPException(
             status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

   session.delete(db_user)
   session.commit()

   return {'message': 'User deleted'}


# Criar um endpoint GET para pegar um único recurso como users/{id} e fazer os testes(BUSCAR ALGO)

@app.get('/users/{user_id}', response_model=UserPublic)
def search_user(user_id: int, session: Session = Depends(get_session)):

     db_user = session.scalar(
          select(User).where(User.id == user_id)
     )

     if not db_user:
          raise HTTPException(
               status_code=HTTPStatus.NOT_FOUND, detail='User not found'
          )
     
     
     session.commit()
     
     return db_user
     
