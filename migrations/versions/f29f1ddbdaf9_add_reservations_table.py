"""Add reservations table

Revision ID: f29f1ddbdaf9
Revises: f11d94c5334c
Create Date: 2025-04-24 11:35:51.559490

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f29f1ddbdaf9'
down_revision = 'f11d94c5334c'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'car_categories',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('title', sa.String(50), nullable=False),
        sa.Column('image', sa.String(255)),
        sa.Column('description', sa.Text()),
        sa.Column('rate', sa.Float()),
    )

    op.create_table(
        'cars',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('model', sa.String(50)),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('price_per_day', sa.Float()),
        sa.Column('quantity', sa.Integer()),
    )

    op.create_table(
        'reservations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('firstname', sa.String(50), nullable=False),
        sa.Column('lastname', sa.String(50), nullable=False),
        sa.Column('email', sa.String(100), nullable=False),
        sa.Column('home', sa.String(20)),
        sa.Column('cell', sa.String(20)),
        sa.Column('car_id', sa.Integer(), sa.ForeignKey('cars.id'), nullable=False),
        sa.Column('start_date', sa.Date(), nullable=False),
        sa.Column('end_date', sa.Date(), nullable=False),
        sa.Column('total_price', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
    )



def downgrade():
    op.drop_table('reservations')
    op.drop_table('cars')
    op.drop_table('car_categories')
    # op.create_table('car_categories',
    # sa.Column('id', sa.INTEGER(), nullable=False),
    # sa.Column('title', sa.VARCHAR(length=50), nullable=False),
    # sa.Column('image', sa.VARCHAR(length=255), nullable=True),
    # sa.Column('description', sa.TEXT(), nullable=True),
    # sa.Column('rate', sa.FLOAT(), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('cars',
    # sa.Column('id', sa.INTEGER(), nullable=False),
    # sa.Column('name', sa.VARCHAR(length=100), nullable=False),
    # sa.Column('model', sa.VARCHAR(length=50), nullable=True),
    # sa.Column('category', sa.VARCHAR(length=50), nullable=False),
    # sa.Column('price_per_day', sa.FLOAT(), nullable=True),
    # sa.Column('quantity', sa.INTEGER(), nullable=True),
    # sa.PrimaryKeyConstraint('id')
    # )
    # op.create_table('reservations',
    # sa.Column('id', sa.INTEGER(), nullable=False),
    # sa.Column('firstname', sa.VARCHAR(length=50), nullable=False),
    # sa.Column('lastname', sa.VARCHAR(length=50), nullable=False),
    # sa.Column('email', sa.VARCHAR(length=100), nullable=False),
    # sa.Column('home', sa.VARCHAR(length=20), nullable=True),
    # sa.Column('cell', sa.VARCHAR(length=20), nullable=True),
    # sa.Column('car_id', sa.INTEGER(), nullable=False),
    # sa.Column('start_date', sa.DATE(), nullable=False),
    # sa.Column('end_date', sa.DATE(), nullable=False),
    # sa.Column('total_price', sa.FLOAT(), nullable=False),
    # sa.Column('created_at', sa.DATETIME(), nullable=True),
    # sa.ForeignKeyConstraint(['car_id'], ['cars.id'], ),
    # sa.PrimaryKeyConstraint('id')
    # )
