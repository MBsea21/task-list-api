"""empty message

Revision ID: e53a06306936
Revises: 9b364957f065
Create Date: 2024-10-31 17:07:18.921981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e53a06306936'
down_revision = '9b364957f065'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('is_complete',
               existing_type=sa.BOOLEAN(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.alter_column('is_complete',
               existing_type=sa.BOOLEAN(),
               nullable=False)

    # ### end Alembic commands ###
