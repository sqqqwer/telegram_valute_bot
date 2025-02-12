"""empty message

Revision ID: 2ccf149b2361
Revises: 75e65609bce3
Create Date: 2025-02-12 14:18:45.638303

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ccf149b2361'
down_revision: Union[str, None] = '75e65609bce3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('valutes', sa.String(), nullable=False))
    op.add_column('users', sa.Column('crypto', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'crypto')
    op.drop_column('users', 'valutes')
    # ### end Alembic commands ###
