"""comment

Revision ID: 160b5b9bc979
Revises: 3a15f6162d87
Create Date: 2021-06-14 21:34:00.640908

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '160b5b9bc979'
down_revision = '3a15f6162d87'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('comment', sa.String(length=140), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'comment')
    # ### end Alembic commands ###
