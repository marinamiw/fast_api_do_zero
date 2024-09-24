from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):  # fixture feita para facilitar
    user = User(username='marina', email='marinamiw@test.com', password='secret')

    session.add(user)
    session.commit()

    result = session.scalar(
        select(User).where(User.email == 'marinamiw@test.com')
        )

    assert result.username == 'marina'
