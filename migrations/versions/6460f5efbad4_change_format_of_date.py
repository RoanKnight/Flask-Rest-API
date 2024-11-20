"""Change format of date

Revision ID: 6460f5efbad4
Revises: fde6bcd7fa2e
Create Date: 2024-11-19 20:54:05.343223

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6460f5efbad4'
down_revision = 'fde6bcd7fa2e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('date_of_birth',
               existing_type=sa.DATETIME(),
               type_=sa.Date(),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customers', schema=None) as batch_op:
        batch_op.alter_column('date_of_birth',
               existing_type=sa.Date(),
               type_=sa.DATETIME(),
               existing_nullable=False)

    # ### end Alembic commands ###