"""Fix datetime colum client and patient

Revision ID: 0552cfd4a976
Revises: b2ffd4070b37
Create Date: 2025-02-09 20:19:14.104037

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0552cfd4a976'
down_revision: str | None = 'b2ffd4070b37'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_revokedtoken_token', table_name='revokedtoken')
    op.drop_table('revokedtoken')
    op.drop_column('client', 'birth_date')
    op.drop_column('patient', 'birth_date')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('patient', sa.Column('birth_date', sa.DATE(), nullable=True))
    op.add_column('client', sa.Column('birth_date', sa.DATE(), nullable=True))
    op.create_table('revokedtoken',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('token', sa.VARCHAR(), nullable=False),
    sa.Column('revoked_at', sa.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_revokedtoken_token', 'revokedtoken', ['token'], unique=1)
    # ### end Alembic commands ###
