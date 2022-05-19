"""init

Revision ID: 62c8d6bae11c
Revises: 
Create Date: 2022-05-19 15:29:47.682564

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62c8d6bae11c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pair',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True, comment='Name'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True, comment='Name'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=70), nullable=False, comment='Username'),
    sa.Column('email', sa.String(length=70), nullable=False, comment='Email'),
    sa.Column('password', sa.String(length=200), nullable=False, comment='Пароль'),
    sa.Column('token', sa.String(length=500), nullable=True, comment='Push notification token'),
    sa.Column('confirmation_codes', sa.JSON(), nullable=True, comment='Коды подтверждений'),
    sa.Column('staff', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('is_email_confirmed', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.String(length=40), nullable=False, comment='Значение токена'),
    sa.Column('user_id', sa.Integer(), nullable=True, comment='Пользователь'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('visit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('when', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('visit')
    op.drop_table('user_role')
    op.drop_table('token')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('pair')
    # ### end Alembic commands ###
