"""Added users table

Revision ID: dd55d5245210
Revises: bde21ecacbaa
Create Date: 2025-10-03 20:07:30.497799

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "dd55d5245210"
down_revision: Union[str, Sequence[str], None] = "bde21ecacbaa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
