"""Add into Post table date_posted column

Revision ID: 27c9a1f2002c
Revises: 462402fdb886
Create Date: 2025-05-22 10:09:26.485077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27c9a1f2002c'
down_revision: Union[str, None] = '462402fdb886'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('date_posted', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'date_posted')
    # ### end Alembic commands ###
