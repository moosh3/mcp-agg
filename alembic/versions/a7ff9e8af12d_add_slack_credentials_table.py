"""Add slack_credentials table

Revision ID: a7ff9e8af12d
Revises: 84086008430a
Create Date: 2025-03-23 17:55:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a7ff9e8af12d'
down_revision: Union[str, None] = '84086008430a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add slack_credentials table."""
    # Create slack_credentials table
    op.create_table(
        'slack_credentials',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=False),
        sa.Column('refresh_token', sa.String(), nullable=True),
        sa.Column('token_type', sa.String(), nullable=True),
        sa.Column('scope', sa.String(), nullable=True),
        sa.Column('team_id', sa.String(), nullable=True),
        sa.Column('team_name', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_slack_credentials_id'), 'slack_credentials', ['id'], unique=False)
    op.create_index(op.f('ix_slack_credentials_user_id'), 'slack_credentials', ['user_id'], unique=True)
    
    # Check if github_credentials table exists and create it if not
    # This is in case the table wasn't already created elsewhere
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    
    if 'github_credentials' not in tables:
        op.create_table(
            'github_credentials',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('access_token', sa.String(), nullable=False),
            sa.Column('token_type', sa.String(), nullable=False, server_default='bearer'),
            sa.Column('scope', sa.String(), nullable=True),
            sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
            sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
            sa.PrimaryKeyConstraint('id')
        )
        op.create_index(op.f('ix_github_credentials_id'), 'github_credentials', ['id'], unique=False)
        op.create_index(op.f('ix_github_credentials_user_id'), 'github_credentials', ['user_id'], unique=True)


def downgrade() -> None:
    """Remove slack_credentials and github_credentials tables."""
    op.drop_index(op.f('ix_slack_credentials_user_id'), table_name='slack_credentials')
    op.drop_index(op.f('ix_slack_credentials_id'), table_name='slack_credentials')
    op.drop_table('slack_credentials')
    
    # Only drop github_credentials table if it was created by this migration
    # We check if the previous migration created it by inspecting the down_revision
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    tables = inspector.get_table_names()
    if 'github_credentials' in tables:
        context = op.get_context()
        revision = context.script.get_revision(down_revision)
        if not any('github_credentials' in str(cmd) for cmd in revision.downgrade_ops.ops):
            op.drop_index(op.f('ix_github_credentials_user_id'), table_name='github_credentials')
            op.drop_index(op.f('ix_github_credentials_id'), table_name='github_credentials')
            op.drop_table('github_credentials')
