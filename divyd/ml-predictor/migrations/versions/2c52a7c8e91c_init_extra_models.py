"""init extra models

Revision ID: 2c52a7c8e91c
Revises: b55cb028a4c9
Create Date: 2019-08-20 19:00:53.393605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c52a7c8e91c'
down_revision = 'b55cb028a4c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_input',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('category', sa.String(length=200), nullable=True),
    sa.Column('weekday', sa.String(length=100), nullable=True),
    sa.Column('day_of_month', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('prediction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=True),
    sa.Column('prediction', sa.Float(precision=200), nullable=True),
    sa.ForeignKeyConstraint(['model_id'], ['persistent_model.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prediction')
    op.drop_table('user_input')
    # ### end Alembic commands ###