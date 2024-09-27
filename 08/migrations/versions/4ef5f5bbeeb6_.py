"""empty message

Revision ID: 4ef5f5bbeeb6
Revises: 5ce676d3b258
Create Date: 2024-09-26 22:26:32.862573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef5f5bbeeb6'
down_revision = '5ce676d3b258'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.add_column(sa.Column('importance', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('message', schema=None) as batch_op:
        batch_op.drop_column('importance')

    # ### end Alembic commands ###
