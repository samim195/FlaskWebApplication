"""ped table

Revision ID: 5d92ebee63b6
Revises: 5842a5396d1d
Create Date: 2019-11-20 12:40:11.614098

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d92ebee63b6'
down_revision = '5842a5396d1d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('device', sa.Column('date_delivered', sa.String(length=10), nullable=True))
    op.add_column('device', sa.Column('date_returned', sa.String(length=10), nullable=True))
    op.add_column('device', sa.Column('delivered_to_customer', sa.String(length=1), nullable=True))
    op.add_column('device', sa.Column('returned_to_logistics', sa.String(length=1), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('device', 'returned_to_logistics')
    op.drop_column('device', 'delivered_to_customer')
    op.drop_column('device', 'date_returned')
    op.drop_column('device', 'date_delivered')
    # ### end Alembic commands ###
