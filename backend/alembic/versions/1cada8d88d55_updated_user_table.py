"""updated user table

Revision ID: 1cada8d88d55
Revises: f005e24dc34a
Create Date: 2026-02-06 10:34:58.752256

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '1cada8d88d55'
down_revision: Union[str, Sequence[str], None] = 'f005e24dc34a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the ENUM type first
    op.execute("CREATE TYPE usertype AS ENUM ('USER', 'STAFF', 'ADMIN')")
    
    # Then add the column with the enum type
    op.add_column('users', sa.Column('user_type', sa.Enum('USER', 'STAFF', 'ADMIN', name='usertype'), nullable=False, server_default='USER'))
    op.alter_column('users', 'user_id',
               existing_type=sa.VARCHAR(length=11),
               type_=sqlmodel.sql.sqltypes.AutoString(length=12),
               existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('users', 'user_id',
               existing_type=sqlmodel.sql.sqltypes.AutoString(length=12),
               type_=sa.VARCHAR(length=11),
               existing_nullable=False)
    op.drop_column('users', 'user_type')
    
    # Drop the ENUM type
    op.execute("DROP TYPE usertype")
