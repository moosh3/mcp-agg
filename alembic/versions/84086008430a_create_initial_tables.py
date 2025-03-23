"""Create initial tables

Revision ID: 84086008430a
Revises: 
Create Date: 2025-03-23 17:02:22.985530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84086008430a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('apps', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('apps', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('apps', sa.Column('last_accessed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tools', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('tools', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('tools', sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'is_admin')
    op.drop_column('tools', 'last_used_at')
    op.drop_column('tools', 'updated_at')
    op.drop_column('tools', 'created_at')
    op.drop_column('apps', 'last_accessed_at')
    op.drop_column('apps', 'updated_at')
    op.drop_column('apps', 'created_at')
    # ### end Alembic commands ###
