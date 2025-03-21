"""initial migration

Revision ID: 9e6ec675c19f
Revises: 
Create Date: 2024-03-12 16:02:11.675027

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '9e6ec675c19f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('exercise_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('record_date', sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")))

    with op.batch_alter_table('food_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('record_date', sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")))

    with op.batch_alter_table('health_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('record_date', sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")))

    with op.batch_alter_table('mood_records', schema=None) as batch_op:
        batch_op.add_column(sa.Column('record_date', sa.Date(), nullable=False, server_default=sa.text("CURRENT_DATE")))

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
        batch_op.drop_column('birth_date')
        batch_op.drop_column('weight')
        batch_op.drop_column('nickname')
        batch_op.drop_column('gender')
        batch_op.drop_column('height')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('height', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('gender', sa.VARCHAR(length=10), nullable=True))
        batch_op.add_column(sa.Column('nickname', sa.VARCHAR(length=80), nullable=True))
        batch_op.add_column(sa.Column('weight', sa.FLOAT(), nullable=True))
        batch_op.add_column(sa.Column('birth_date', sa.DATE(), nullable=True))
        batch_op.alter_column('email',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)

    with op.batch_alter_table('mood_records', schema=None) as batch_op:
        batch_op.drop_column('record_date')

    with op.batch_alter_table('health_records', schema=None) as batch_op:
        batch_op.drop_column('record_date')

    with op.batch_alter_table('food_records', schema=None) as batch_op:
        batch_op.drop_column('record_date')

    with op.batch_alter_table('exercise_records', schema=None) as batch_op:
        batch_op.drop_column('record_date')

    # ### end Alembic commands ###
