from http import HTTPStatus


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


def test_read_user(client):
   response = client.get('/users/')
   assert response.status_code == HTTPStatus.OK
   assert response.json() == {'users': [
   {
      'username': 'testusername',
      'email': 'test@test.com',
      'id': 1
   }
   ]}
