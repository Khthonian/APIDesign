"""Add timestamp

Revision ID: aecdda41aba6
Revises: a3ca5d83001c
Create Date: 2024-04-11 09:22:23.001221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aecdda41aba6'
down_revision: Union[str, None] = 'a3ca5d83001c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('locations', sa.Column('timestamp', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('locations', 'timestamp')
    # ### end Alembic commands ###
