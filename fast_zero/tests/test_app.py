from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):

   response = client.post(  # UserSchema, testando a parte do envio
      '/users/',
      json={
      'username': 'testusername',
      'password': 'password',
      'email': 'test@test.com'
      }
   )
   # validar UserPublic, o recebimento dos dados.
   assert response.status_code == HTTPStatus.CREATED
   assert response.json() == {
      'username': 'testusername',
      'email': 'test@test.com',
      'id': 1
   }

def test_create_user_username_already_exists(client, user):

   response = client.post('/users/',
   json = {
      'username': user.username,
      'password': 'password',
      'email':'emailbacana@test.com'
   }
   )
   assert response.status_code == HTTPStatus.BAD_REQUEST
   assert response.json() == {'detail': "Username already exists"}

def test_create_user_email_already_exists(client, user):

   response = client.post('/users/',
   json = {
      'username': 'usernamelouco',
      'password': 'password',
      'email': user.email
   }
   )
   assert response.status_code == HTTPStatus.BAD_REQUEST
   assert response.json() == {'detail': "Email already exists"}



# se nao tiver ninguem no BD
def test_read_user(client):
   response = client.get('/users/')
   assert response.status_code == HTTPStatus.OK
   assert response.json() == {'users': []}


# se tiver
def test_read_user_with_user(client, user):  # user eh um objeto do sql alchemy feito no conftest que simula um cadatro de usuario (retorna os atributos publicos dele pelo formato da base de dados - é uma fixture), so que para realizar se a resposta do teste é esse modelo, precisamos converter ele em modelo do pydantic pois o teste retorna em pydantic e nao em sql alchemy. Portanto, precisamos do model validate para converter esse objeto em objeto de UserPublic(pydantic)
   user_schema = UserPublic.model_validate(user).model_dump()  # model validade pega os atributos do user, que é um modelo do sql alchemy,e ira converter eles em schema, modelo do pydantic
  # no caso model validate faz a conversão de um pbjeto qualquer para um modelo do pydantic
   response = client.get('/users/')

   assert response.status_code == HTTPStatus.OK
   assert response.json() == {'users': [user_schema]}  # UserPublic


def test_update_user(client, user):
   response = client.put(
      '/users/1',
      json={
         'password': '123',
         'username': 'testusername2',  # tem q mudar o username do q foi colocdao antes nesse id1 pois ele esta atualizando, poderia mudar qualquer outro campo
         'email': 'test@test.com',
         'id': 1
      }
      )
   assert response.json() == {
      'username': 'testusername2',
      'email': 'test@test.com',
      'id': 1
   }


def test_update_user_not_found(client):
   response = client.put(
      '/users/99',
      json={
         'password': '1234',
         'username': 'testusernamee',
         'email': 'test@test.com',
         'id': 99
      }
      )
   assert response.status_code == HTTPStatus.NOT_FOUND
   assert response.json() == {'detail': 'User not found'}


def test_search_user(client, user):
    response = client.get(f'/users/{user.id}')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
       'username': user.username,
       'email': user.email,
       'id': user.id
    }
   

def test_search_user_not_found(client):
    response = client.get('/users/999')  # ID que não existe

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
   response = client.delete('/users/1')  # o delete tem q vir depois de tudo pois ele estara removendo o id 1 na execuçao do teste

   assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
   response = client.delete('/users/99')
   assert response.status_code == HTTPStatus.NOT_FOUND
   assert response.json() == {'detail': 'User not found'}
