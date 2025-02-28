"""scheduling_migration

Revision ID: 64f70068a9a6
Revises: 0e35895be866
Create Date: 2025-02-26 05:54:03.654498
"""
from alembic import op
import sqlalchemy as sa
import uuid

# revision identifiers, used by Alembic.
revision = '64f70068a9a6'
down_revision = '0e35895be866'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Cria a tabela de agendamentos
    op.create_table('schedulings',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('scheduling_date', sa.String(), nullable=False),
        sa.Column('scheduling_time', sa.String(), nullable=False),
        sa.Column('scheduling_type', sa.String(), nullable=False),
        sa.Column('doctor_id', sa.Integer(), nullable=True),
        sa.Column('patient_id', sa.Integer(), nullable=True),
        sa.Column('rescheduled', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['doctor_id'], ['doctors.id']),
        sa.ForeignKeyConstraint(['patient_id'], ['patients.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Prepara a tabela para inserção dos dados
    schedulings_table = sa.table('schedulings',
        sa.column('id', sa.String),
        sa.column('scheduling_date', sa.String),
        sa.column('scheduling_time', sa.String),
        sa.column('scheduling_type', sa.String),
        sa.column('doctor_id', sa.Integer),
        sa.column('patient_id', sa.Integer),
        sa.column('rescheduled', sa.Boolean)
    )
    
    # Insere os registros de agendamento
    op.bulk_insert(
        schedulings_table,
        [
            {
                "id": str(uuid.uuid4()),
                "scheduling_date": "01/03/2025",
                "scheduling_time": "09:00",
                "scheduling_type": "CONSULTATION",
                "doctor_id": 1,
                "patient_id": 1,
                "rescheduled": False
            },
            {
                "id": str(uuid.uuid4()),
                "scheduling_date": "01/03/2025",
                "scheduling_time": "10:00",
                "scheduling_type": "CONSULTATION",
                "doctor_id": 2,
                "patient_id": 1,
                "rescheduled": False
            },
            {
                "id": str(uuid.uuid4()),
                "scheduling_date": "01/03/2025",
                "scheduling_time": "11:00",
                "scheduling_type": "CONSULTATION",
                "doctor_id": 3,
                "patient_id": 1,
                "rescheduled": False
            },
            {
                "id": str(uuid.uuid4()),
                "scheduling_date": "02/03/2025",
                "scheduling_time": "09:00",
                "scheduling_type": "CONSULTATION",
                "doctor_id": 1,
                "patient_id": 1,
                "rescheduled": False
            },
            {
                "id": str(uuid.uuid4()),
                "scheduling_date": "02/03/2025",
                "scheduling_time": "10:00",
                "scheduling_type": "CONSULTATION",
                "doctor_id": 2,
                "patient_id": 1,
                "rescheduled": False
            },
            {
                "id": str(uuid.uuid4()),
                "scheduling_date": "02/03/2025",
                "scheduling_time": "11:00",
                "scheduling_type": "CONSULTATION",
                "doctor_id": 3,
                "patient_id": 1,
                "rescheduled": False
            },
        ]
    )


def downgrade() -> None:
    op.drop_table('schedulings')
