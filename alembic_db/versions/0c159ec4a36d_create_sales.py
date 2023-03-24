"""create sales

Revision ID: 0c159ec4a36d
Revises: 9c13e085e5f6
Create Date: 2023-03-23 23:06:29.563561

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c159ec4a36d'
down_revision = '9c13e085e5f6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sales',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('saled_products',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=True),
    sa.Column('sales_id', sa.Integer(), nullable=True),
    sa.Column('quantity_unit_id', sa.Integer(), nullable=True),
    sa.Column('barcode', sa.String(), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['quantity_unit_id'], ['quantity_units.id'], ondelete='set null'),
    sa.ForeignKeyConstraint(['sales_id'], ['sales.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_saled_products_barcode'), 'saled_products', ['barcode'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_saled_products_barcode'), table_name='saled_products')
    op.drop_table('saled_products')
    op.drop_table('sales')
    # ### end Alembic commands ###
