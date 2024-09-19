import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient

from fast_zero.app import app
from fast_zero.models import table_registry

# funçao de teste recebe esse parametro client,ele vai executar a funçao e vai passar o retorno dela para o teste
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture()
def session():
    engine = create_engine('sqlite:///:memory:')
    table_registry.metadata.create_all(engine)

    #gerenciamento de contexto
    with Session(engine) as engine:
        yield session #delimita o setup (rodar antes do teste) e depois do yield (tear down) desfaz a operação que fez

        #quando pegar o objeto session, vai rodar ate essa linha e ai vai parar até esse objeto q foi dado yield, é o que vai cair dentro do parametro do teste la no test_db

    table_registry.metadata.drop_all(engine)