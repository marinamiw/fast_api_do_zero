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

def test_update_user(client):
   response = client.put(
      '/users/1',
      json={
         'password': '123',
         'username': 'testusername2',
         'email': 'test@test.com',
         'id': 1
      }
      )
   assert response.json() == {
      'username': 'testusername2',
      'email': 'test@test.com',
      'id': 1
   }

def test_delete_user(client):
   response = client.delete('/users/1')

   assert response.json() == {'message':'User deleted'}

def test_search_user(client):
    response = client.get('/users/1')
    
    assert response.status_code == 200
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com'
    }

def test_search_user_not_found(client):
    response = client.get('/users/999')  # ID que não existe
    
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}