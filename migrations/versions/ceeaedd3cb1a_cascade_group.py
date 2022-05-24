"""cascade_group

Revision ID: ceeaedd3cb1a
Revises: d53bf848870b
Create Date: 2022-05-23 21:39:43.012586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ceeaedd3cb1a'
down_revision = 'd53bf848870b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('group_user_group_id_fkey', 'group_user', type_='foreignkey')
    op.drop_constraint('group_user_user_id_fkey', 'group_user', type_='foreignkey')
    op.create_foreign_key(None, 'group_user', 'user', ['user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'group_user', 'group', ['group_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'group_user', type_='foreignkey')
    op.drop_constraint(None, 'group_user', type_='foreignkey')
    op.create_foreign_key('group_user_user_id_fkey', 'group_user', 'user', ['user_id'], ['id'])
    op.create_foreign_key('group_user_group_id_fkey', 'group_user', 'group', ['group_id'], ['id'])
    # ### end Alembic commands ###