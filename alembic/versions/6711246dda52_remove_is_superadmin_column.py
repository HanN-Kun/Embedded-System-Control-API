"""remove is_superadmin column

Revision ID: 6711246dda52
Revises: 9edb2bee08ac
Create Date: 2026-09-11 11:02:46.583478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6711246dda52'
down_revision: Union[str, Sequence[str], None] = '9edb2bee08ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('users', 'is_superadmin')


def downgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_superadmin', sa.Boolean(), nullable=False, server_default=sa.false()),
    )
