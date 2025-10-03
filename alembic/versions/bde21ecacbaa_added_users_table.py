"""Added users table

Revision ID: bde21ecacbaa
Revises:
Create Date: 2025-10-03 20:04:25.678430

"""

from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = "bde21ecacbaa"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
