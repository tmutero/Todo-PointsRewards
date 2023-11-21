"""add_tasks_table2

Revision ID: a06e39a82db8
Revises: 8411f81288b8
Create Date: 2023-11-18 14:20:03.161259

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a06e39a82db8'
down_revision = '8411f81288b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('image_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('file_location', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('image_id')
    )
    op.create_index(op.f('ix_image_image_id'), 'image', ['image_id'], unique=False)
    op.create_table('tasks',
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('due_date', sa.DateTime(), nullable=True),
    sa.Column('completed_date', sa.DateTime(), nullable=True),
    sa.Column('task_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_name', sa.String(), nullable=False),
    sa.Column('points', sa.Integer(), nullable=False),
    sa.Column('completed', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('task_id')
    )
    op.create_index(op.f('ix_tasks_task_id'), 'tasks', ['task_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_tasks_task_id'), table_name='tasks')
    op.drop_table('tasks')
    op.drop_index(op.f('ix_image_image_id'), table_name='image')
    op.drop_table('image')
    # ### end Alembic commands ###
