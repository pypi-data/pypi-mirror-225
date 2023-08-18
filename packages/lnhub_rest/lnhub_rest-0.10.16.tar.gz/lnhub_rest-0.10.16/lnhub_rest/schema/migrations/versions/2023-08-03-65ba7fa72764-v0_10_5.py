"""v0.10.5.

Revision ID: 65ba7fa72764
Revises: 17dd170649b6
Create Date: 2023-08-03 13:53:31.649059

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

from lnhub_rest.schema.migrations.rls._2023_08_03_65ba7fa72764_v0_10_5 import (
    drop_rls_cloud_run_instance,
    drop_sql_rls_account_instance,
    sql_rls_account_instance,
    sql_rls_cloud_run_instance,
)

# revision identifiers, used by Alembic.
revision = "65ba7fa72764"
down_revision = "17dd170649b6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "cloud_run_instance", sa.Column("last_access_at", sa.DateTime(), nullable=True)
    )
    op.execute(sql_rls_account_instance)
    op.execute(sql_rls_cloud_run_instance)


def downgrade() -> None:
    op.drop_column("cloud_run_instance", "last_access_at")
    op.execute(drop_sql_rls_account_instance)
    op.execute(drop_rls_cloud_run_instance)
