"""user_init

Revision ID: 02f14d84cca8
Revises: 52348df29a78
Create Date: 2023-11-19 20:42:28.294019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02f14d84cca8'
down_revision = '52348df29a78'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tasks', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('tasks', sa.Column('approved', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tasks', 'approved')
    op.drop_column('tasks', 'created_at')
    # ### end Alembic commands ###
