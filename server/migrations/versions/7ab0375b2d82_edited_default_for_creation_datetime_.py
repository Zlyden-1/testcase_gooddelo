"""Edited default for creation datetime column

Revision ID: 7ab0375b2d82
Revises: 4ba832d9c71e
Create Date: 2023-08-28 22:29:44.724007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ab0375b2d82'
down_revision: Union[str, None] = '4ba832d9c71e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###