"""update venue table address  version 01.

Revision ID: 895477e4c0c6
Revises: 49a8b5aea71b
Create Date: 2020-10-18 19:58:59.294089

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '895477e4c0c6'
down_revision = '49a8b5aea71b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###