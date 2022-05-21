"""visit_state

Revision ID: e455d34da812
Revises: cd0bd61ad13e
Create Date: 2022-05-21 18:34:26.070731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e455d34da812'
down_revision = 'cd0bd61ad13e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('visit', sa.Column('state', sa.Integer(), nullable=True, comment='State'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('visit', 'state')
    # ### end Alembic commands ###