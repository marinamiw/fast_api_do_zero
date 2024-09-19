from fast_zero.models import User, table_registry

from sqlalchemy.orm import Session
from sqlalchemy import create_engine


def test_create_user():
    engine = create_engine('sqlite:///database.db')

    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(username = 'test', email = 'test@test.com', password = 'secret')

    session.add(user)
    session.commit()
    session.refresh(user)

    assert user.id == 1