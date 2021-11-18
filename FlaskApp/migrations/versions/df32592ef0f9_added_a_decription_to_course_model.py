"""Added a decription to course model

Revision ID: df32592ef0f9
Revises: 58acad769c45
Create Date: 2021-11-18 11:57:44.339687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df32592ef0f9'
down_revision = '58acad769c45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('courses', sa.Column('description', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('courses', 'description')
    # ### end Alembic commands ###
