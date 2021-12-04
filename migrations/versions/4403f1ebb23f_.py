"""empty message

Revision ID: 4403f1ebb23f
Revises: 22250a5e0ba0
Create Date: 2021-12-04 14:23:43.802724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4403f1ebb23f'
down_revision = '22250a5e0ba0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('books_clients_client_id_fkey', 'books_clients', type_='foreignkey')
    op.create_foreign_key(None, 'books_clients', 'clients', ['client_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'books_clients', type_='foreignkey')
    op.create_foreign_key('books_clients_client_id_fkey', 'books_clients', 'clients', ['client_id'], ['id'])
    # ### end Alembic commands ###
