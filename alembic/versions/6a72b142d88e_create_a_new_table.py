"""create a new table

Revision ID: 6a72b142d88e
Revises: 
Create Date: 2022-01-06 17:05:15.905813

"""
import fastapi_utils
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6a72b142d88e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("task", sa.String(50), nullable=False),
    )


def downgrade():
    op.drop_table("todo")
