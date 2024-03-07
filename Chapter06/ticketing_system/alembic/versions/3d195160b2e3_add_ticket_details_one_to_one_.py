"""add ticket details one to one relationship

Revision ID: 3d195160b2e3
Revises: 9a9cfeb65ea4
Create Date: 2024-03-07 10:02:25.781652

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d195160b2e3"
down_revision: Union[str, None] = "9a9cfeb65ea4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ticket_details",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "ticket_id", sa.Integer(), nullable=False
        ),
        sa.Column("seat", sa.String(), nullable=True),
        sa.Column(
            "ticket_type", sa.String(), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["ticket_id"],
            ["tickets.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute("""
        INSERT INTO ticket_details (ticket_id)
        SELECT id FROM tickets
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ticket_details")
    # ### end Alembic commands ###
