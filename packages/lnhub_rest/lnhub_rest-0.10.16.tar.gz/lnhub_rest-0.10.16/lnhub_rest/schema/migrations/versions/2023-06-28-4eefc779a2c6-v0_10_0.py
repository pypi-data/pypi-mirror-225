"""v0.10.0.

Revision ID: 4eefc779a2c6
Revises: 1092ae46baba
Create Date: 2023-06-28 23:40:31.431591

"""
import sqlalchemy as sa  # noqa
import sqlmodel  # noqa
from alembic import op

from lnhub_rest.schema.migrations.rls._2023_06_28_4eefc779a2c6_v0_10_0 import (
    sql_drop_rls_db_user,
    sql_rls_db_user,
)

# revision identifiers, used by Alembic.
revision = "4eefc779a2c6"
down_revision = "1092ae46baba"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "db_user",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("instance_id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("db_user_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "db_user_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["instance_id"],
            ["instance.id"],
            name=op.f("fk_db_user_instance_id_instance"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_db_user")),
        sa.UniqueConstraint(
            "instance_id", "db_user_name", name=op.f("uq_db_user_instance_id")
        ),
    )
    op.create_index(
        op.f("ix_db_user_instance_id"), "db_user", ["instance_id"], unique=False
    )
    op.add_column(
        "account_instance",
        sa.Column("db_user_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
    )
    op.create_index(
        op.f("ix_account_instance_db_user_id"),
        "account_instance",
        ["db_user_id"],
        unique=False,
    )
    op.create_foreign_key(
        op.f("fk_account_instance_db_user_id_db_user"),
        "account_instance",
        "db_user",
        ["db_user_id"],
        ["id"],
    )
    op.add_column(
        "instance",
        sa.Column("db_scheme", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column(
        "instance",
        sa.Column("db_host", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )
    op.add_column("instance", sa.Column("db_port", sa.Integer(), nullable=True))
    op.add_column(
        "instance",
        sa.Column("db_database", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    )

    op.execute(sql_rls_db_user)


def downgrade() -> None:
    op.execute(sql_drop_rls_db_user)
    op.drop_column("instance", "db_database")
    op.drop_column("instance", "db_port")
    op.drop_column("instance", "db_host")
    op.drop_column("instance", "db_scheme")
    op.drop_constraint(
        op.f("fk_account_instance_db_user_id_db_user"),
        "account_instance",
        type_="foreignkey",
    )
    op.drop_index(op.f("ix_account_instance_db_user_id"), table_name="account_instance")
    op.drop_column("account_instance", "db_user_id")
    op.drop_index(op.f("ix_db_user_instance_id"), table_name="db_user")
    op.drop_table("db_user")
