"""empty message

Revision ID: 25344e1a75ed
Revises: 0d49c11601f1
Create Date: 2023-02-22 04:45:34.192217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25344e1a75ed'
down_revision = '0d49c11601f1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planeta',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planeta')
    # ### end Alembic commands ###
