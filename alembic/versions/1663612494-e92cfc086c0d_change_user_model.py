"""Change user model

Revision ID: e92cfc086c0d
Revises: 63d087421b9c
Create Date: 2022-09-19 23:34:54.239017

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e92cfc086c0d'
down_revision = '63d087421b9c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), server_default='0', nullable=False))
    op.drop_column('users', 'is_demo')
    op.drop_column('users', 'deleted_at')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('deleted_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('is_demo', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=False))
    op.drop_column('users', 'is_superuser')
    # ### end Alembic commands ###