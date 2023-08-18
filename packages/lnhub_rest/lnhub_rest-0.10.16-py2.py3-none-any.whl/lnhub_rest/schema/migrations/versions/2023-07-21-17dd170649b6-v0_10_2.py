"""v0.10.2.

Revision ID: 17dd170649b6
Revises: 4eefc779a2c6
Create Date: 2023-07-21 16:34:12.648043

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op
from sqlalchemy.dialects import postgresql

from lnhub_rest.schema.migrations.function._2023_07_21_17dd170649b6_v0_10_2 import (
    sql_function_is_instance_public,
)
from lnhub_rest.schema.migrations.rls._2023_07_21_17dd170649b6_v0_10_2 import (
    sql_drop_rls_cloud_run_instance,
    sql_drop_rls_db_user_public,
    sql_rls_cloud_run_instance,
    sql_rls_db_user_public,
)

# revision identifiers, used by Alembic.
revision = "17dd170649b6"
down_revision = "4eefc779a2c6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cloud_run_instance",
        sa.Column("lamin_instance_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column(
            "cloud_run_instance_name",
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False,
        ),
        sa.Column("api_url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["lamin_instance_id"],
            ["instance.id"],
            name=op.f("fk_cloud_run_instance_lamin_instance_id_instance"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_cloud_run_instance")),
    )
    op.create_index(
        op.f("ix_cloud_run_instance_created_at"),
        "cloud_run_instance",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cloud_run_instance_lamin_instance_id"),
        "cloud_run_instance",
        ["lamin_instance_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_cloud_run_instance_updated_at"),
        "cloud_run_instance",
        ["updated_at"],
        unique=False,
    )
    op.alter_column(
        "account_instance", "db_user_id", existing_type=postgresql.UUID(), nullable=True
    )
    op.alter_column(
        "db_user", "instance_id", existing_type=postgresql.UUID(), nullable=True
    )
    op.drop_constraint("fk_db_user_instance_id_instance", "db_user", type_="foreignkey")
    op.create_foreign_key(
        op.f("fk_db_user_instance_id_instance"),
        "db_user",
        "instance",
        ["instance_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.execute(sql_rls_cloud_run_instance)
    op.execute(sql_function_is_instance_public)
    op.execute(sql_rls_db_user_public)


def downgrade() -> None:
    op.execute(sql_drop_rls_cloud_run_instance)
    op.execute(sql_drop_rls_db_user_public)
    op.drop_constraint(
        op.f("fk_db_user_instance_id_instance"), "db_user", type_="foreignkey"
    )
    op.create_foreign_key(
        "fk_db_user_instance_id_instance",
        "db_user",
        "instance",
        ["instance_id"],
        ["id"],
    )
    op.alter_column(
        "db_user", "instance_id", existing_type=postgresql.UUID(), nullable=False
    )
    op.alter_column(
        "account_instance",
        "db_user_id",
        existing_type=postgresql.UUID(),
        nullable=False,
    )
    op.drop_index(
        op.f("ix_cloud_run_instance_updated_at"), table_name="cloud_run_instance"
    )
    op.drop_index(
        op.f("ix_cloud_run_instance_lamin_instance_id"), table_name="cloud_run_instance"
    )
    op.drop_index(
        op.f("ix_cloud_run_instance_created_at"), table_name="cloud_run_instance"
    )
    op.drop_table("cloud_run_instance")
