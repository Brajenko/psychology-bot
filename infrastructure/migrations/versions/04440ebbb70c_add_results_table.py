"""add results table

Revision ID: 04440ebbb70c
Revises: 57b379d1d9a0
Create Date: 2025-01-14 23:54:15.977854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04440ebbb70c'
down_revision: Union[str, None] = '57b379d1d9a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('results',
    sa.Column('poll_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['poll_id'], ['polls.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('completions', sa.Column('score', sa.Integer(), nullable=False))
    op.drop_column('completions', 'result')


def downgrade() -> None:
    op.add_column('completions', sa.Column('result', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('completions', 'score')
    op.drop_table('results')
