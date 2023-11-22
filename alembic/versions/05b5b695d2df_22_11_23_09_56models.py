"""22_11_23_09_56models

Revision ID: 05b5b695d2df
Revises: c15e1111d061
Create Date: 2023-11-22 06:56:24.240990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05b5b695d2df'
down_revision: Union[str, None] = 'c15e1111d061'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_group_role_fkey', 'users', type_='foreignkey')
    op.drop_constraint('users_user_role_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'group_role')
    op.drop_column('users', 'user_role')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('user_role', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('group_role', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_user_role_fkey', 'users', 'user_roles', ['user_role'], ['id'])
    op.create_foreign_key('users_group_role_fkey', 'users', 'user_group_roles', ['group_role'], ['id'])
    # ### end Alembic commands ###
