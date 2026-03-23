"""add satellite indices and SAR features

Revision ID: add_satellite_indices
Revises: 
Create Date: 2026-03-23

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_satellite_indices'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add new optical indices
    op.add_column('satellite_images', sa.Column('avg_lswi', sa.Float(), nullable=True))
    op.add_column('satellite_images', sa.Column('avg_ndbi', sa.Float(), nullable=True))
    
    # Add SAR features
    op.add_column('satellite_images', sa.Column('sar_vv_db', sa.Float(), nullable=True))
    op.add_column('satellite_images', sa.Column('sar_vh_db', sa.Float(), nullable=True))
    op.add_column('satellite_images', sa.Column('sar_ratio', sa.Float(), nullable=True))
    op.add_column('satellite_images', sa.Column('change_detected', sa.Boolean(), nullable=True, default=False))
    op.add_column('satellite_images', sa.Column('change_area_sqkm', sa.Float(), nullable=True))


def downgrade():
    # Remove SAR features
    op.drop_column('satellite_images', 'change_area_sqkm')
    op.drop_column('satellite_images', 'change_detected')
    op.drop_column('satellite_images', 'sar_ratio')
    op.drop_column('satellite_images', 'sar_vh_db')
    op.drop_column('satellite_images', 'sar_vv_db')
    
    # Remove optical indices
    op.drop_column('satellite_images', 'avg_ndbi')
    op.drop_column('satellite_images', 'avg_lswi')
