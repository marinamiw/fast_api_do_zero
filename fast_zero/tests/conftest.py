import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.database import get_session
from fast_zero.models import table_registry,User

# funçao de teste recebe esse parametro client,ele vai executar a funçao e vai passar o retorno dela para o teste
@pytest.fixture
def client(session):

    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client
    app.dependency_overrides.clear()

@pytest.fixture()
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread':False},
        poolclass=StaticPool, #nao ira validar se estao rodando em threads diferentes, vai usar tbm a mesma coisa para validar
    )
    table_registry.metadata.create_all(engine)

    #gerenciamento de contexto
    with Session(engine) as session:
        yield session #delimita o setup (rodar antes do teste) e depois do yield (tear down) desfaz a operação que fez

        #quando pegar o objeto session, vai rodar ate essa linha e ai vai parar até esse objeto q foi dado yield, é o que vai cair dentro do parametro do teste la no test_db

    table_registry.metadata.drop_all(engine)


@pytest.fixture() #fixture para registrar um usuario na base de dados para testar
def user(session):
    user = User(
        username='teste', email='teste@test.com', password='testtest'
        )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user