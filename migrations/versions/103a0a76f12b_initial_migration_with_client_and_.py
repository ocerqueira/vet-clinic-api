"""Initial migration with Client and Patient

Revision ID: 103a0a76f12b
Revises: 
Create Date: 2025-02-03 23:25:41.218825

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 


# revision identifiers, used by Alembic.
revision: str = '103a0a76f12b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('lastname', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('gender', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=True),
    sa.Column('document', sqlmodel.sql.sqltypes.AutoString(length=25), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('phone', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=150), nullable=False),
    sa.Column('address', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=True),
    sa.Column('number', sqlmodel.sql.sqltypes.AutoString(length=10), nullable=True),
    sa.Column('neighborhood', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('city', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('state', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=True),
    sa.Column('zip_code', sqlmodel.sql.sqltypes.AutoString(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document'),
    sa.UniqueConstraint('email')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=200), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('species', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('breed', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('patient')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_table('user')
    op.drop_table('client')
    # ### end Alembic commands ###
