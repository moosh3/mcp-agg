"""add_mcp_tokens_table

Revision ID: 78df465a4bd3
Revises: a7ff9e8af12d
Create Date: 2025-03-23 18:42:46.369483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '78df465a4bd3'
down_revision: Union[str, None] = 'a7ff9e8af12d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema to add MCP tokens table."""
    op.create_table(
        'mcp_tokens',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('token', sa.String(), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('is_revoked', sa.Boolean(), default=False, nullable=True),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_mcp_tokens_id'), 'mcp_tokens', ['id'], unique=False)
    op.create_index(op.f('ix_mcp_tokens_token'), 'mcp_tokens', ['token'], unique=True)


def downgrade() -> None:
    """Downgrade schema by dropping MCP tokens table."""
    op.drop_index(op.f('ix_mcp_tokens_token'), table_name='mcp_tokens')
    op.drop_index(op.f('ix_mcp_tokens_id'), table_name='mcp_tokens')
    op.drop_table('mcp_tokens')
