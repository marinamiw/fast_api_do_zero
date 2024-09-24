from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)  # init=false(nao esta mais inicializando esse objeto, nao inclui essa coluna no construtor gerado automaticamente para a classe) e o primary key diz que a partir de agora, nao precisa mais preencher o campo id, ele ira preencher automaticamente quando esse user for para o BD
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
        )
