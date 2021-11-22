"""empty message

Revision ID: a7ca4c716701
Revises: 0ee5ae1dc839
Create Date: 2021-11-16 19:42:24.366297

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7ca4c716701'
down_revision = '0ee5ae1dc839'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('description', sa.Text(), nullable=True))
    op.drop_column('books', 'descripion')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('books', sa.Column('descripion', sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_column('books', 'description')
    # ### end Alembic commands ###