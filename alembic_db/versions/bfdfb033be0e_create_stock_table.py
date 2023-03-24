"""create stock table

Revision ID: bfdfb033be0e
Revises: 0c159ec4a36d
Create Date: 2023-03-25 00:18:14.614971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfdfb033be0e'
down_revision = '0c159ec4a36d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('quantity_unit_id', sa.Integer(), nullable=True),
    sa.Column('stock_quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['quantity_unit_id'], ['quantity_units.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stocks_product_id'), 'stocks', ['product_id'], unique=False)
    op.alter_column('saled_products', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('saled_products', 'quantity_unit_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('saled_products', 'quantity_unit_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('saled_products', 'product_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_index(op.f('ix_stocks_product_id'), table_name='stocks')
    op.drop_table('stocks')
    # ### end Alembic commands ###
