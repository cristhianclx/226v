"""empty message

Revision ID: b41d5b3effae
Revises: 
Create Date: 2024-09-26 20:15:12.247231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b41d5b3effae'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nickname', sa.Text(), nullable=False),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###