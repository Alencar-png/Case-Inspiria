from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import String, Boolean, Integer, ForeignKey

# revision identifiers, used by Alembic.
revision: str = '9541188de65f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Criação da tabela 'users'
    op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False),
    )

    # Inserir superusuário
    users_table = table('users',
        column('id', Integer),
        column('name', String),
        column('email', String),
        column('password', String),
        column('is_admin', Boolean)
    )

    op.bulk_insert(users_table, [
        {'id': 1, 'name': 'Admin', 'email': 'adm@example.com', 
         'password': '$2b$12$9P7uGuun1qwfwsUONOmq5uUzDYLkrNDY32jSDLnZcDH8dntrc8Nqm', 
         'is_admin': True}
    ])

    op.execute("SELECT setval('users_id_seq', (SELECT MAX(id) FROM users))")

def downgrade() -> None:
    op.drop_table('buttons')
    op.drop_table('users')
