"""Fix RevokedToken model

Revision ID: b2ffd4070b37
Revises: b58ab944f4af
Create Date: 2025-02-09 19:29:05.211487

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2ffd4070b37'
down_revision: Union[str, None] = 'b58ab944f4af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('revokedtoken')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('revokedtoken',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(), nullable=False),
    sa.Column('revoked_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
