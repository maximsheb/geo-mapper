"""v1_init

Revision ID: a5f7fbc42401
Revises: 
Create Date: 2024-08-28 01:53:21.453409

"""
from typing import List

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5f7fbc42401'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Task',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('status', sa.Enum('RUNNING', 'DONE', name='taskstatusenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('GeoPoint',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('task_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_task_id', 'GeoPoint', ['task_id'], unique=False)
    op.create_table('LinkedDistance',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('distance', sa.Float(), nullable=False),
    sa.Column('task_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['Task.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('LinkedDistance')
    op.drop_index('idx_task_id', table_name='GeoPoint')
    op.drop_table('GeoPoint')
    op.drop_table('Task')
    # ### end Alembic commands ###
