"""zero product stock

Revision ID: 0083954b09bb
Revises: 68a62d9f91af
Create Date: 2026-10-13 21:29:56.863267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0083954b09bb'
down_revision: Union[str, Sequence[str], None] = '68a62d9f91af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.drop_constraint(
    #     "ck_quantity_nonnegative",
    #     "products",
    #     type_="check",
    # )
    op.create_check_constraint(
        "ck_products_quantity_nonnegative",
        "products",
        "quantity >= 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_products_quantity_nonnegative",
        "products",
        type_="check",
    )
    op.create_check_constraint(
        "ck_quantity_nonnegative",
        "products",
        "quantity > 0",
    )