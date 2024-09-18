import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


# funçao de teste recebe esse parametro client,ele vai executar a funçao e vai passar o retorno dela para o teste
@pytest.fixture
def client():
    return TestClient(app)
