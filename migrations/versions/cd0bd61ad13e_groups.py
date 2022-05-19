"""groups

Revision ID: cd0bd61ad13e
Revises: f5726465945d
Create Date: 2022-05-19 19:15:26.607679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cd0bd61ad13e'
down_revision = 'f5726465945d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True, comment='Name'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('group_user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='User'),
    sa.Column('group_id', sa.Integer(), nullable=True, comment='Group'),
    sa.ForeignKeyConstraint(['group_id'], ['group.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('group_user')
    op.drop_table('group')
    # ### end Alembic commands ###
