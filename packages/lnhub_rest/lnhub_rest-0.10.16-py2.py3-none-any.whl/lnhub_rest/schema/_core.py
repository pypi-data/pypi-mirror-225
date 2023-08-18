from datetime import datetime
from typing import List, Optional  # noqa
from uuid import UUID, uuid4

import sqlmodel
from sqlalchemy import Column
from sqlmodel import SQLModel  # type: ignore  # noqa
from sqlmodel import (
    Field,
    ForeignKey,
    MetaData,
    PrimaryKeyConstraint,
    Relationship,
    UniqueConstraint,
)

from ._timestamps import CreatedAt, UpdatedAt
from ._type import instance_role, organization_role


class User(SQLModel, table=True):  # type: ignore
    __tablename__ = "users"
    metadata = MetaData(schema="auth")
    id: Optional[UUID] = Field(primary_key=True)


class Account(SQLModel, table=True):  # type: ignore
    """Accounts."""

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: Optional[UUID] = Field(foreign_key=User.id, index=True)
    """Maybe None because it may be an organizational account."""
    lnid: str = Field(index=True, unique=True)
    """User-facing base62 ID."""
    handle: str = Field(index=True, unique=True)
    name: Optional[str] = Field(default=None, index=True)
    bio: Optional[str] = None
    website: Optional[str] = None
    github_handle: Optional[str] = None
    twitter_handle: Optional[str] = None
    linkedin_handle: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Storage(SQLModel, table=True):  # type: ignore
    """Storage locations.

    A dobject or run-associated file can be stored in any desired S3,
    GCP, Azure or local storage location. This table tracks these locations
    along with metadata.
    """

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    lnid: str = Field(index=True)
    """User-facing base62 ID."""
    created_by: UUID = Field(foreign_key=Account.id, index=True)
    """ID of owning account."""
    root: str = Field(index=True, unique=True)
    """An s3 path, a local path, etc."""  # noqa
    type: Optional[str] = None
    """Local vs. s3 vs. gcp etc."""
    region: Optional[str] = None
    """Cloud storage region if applicable."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class Instance(SQLModel, table=True):  # type: ignore
    """Instances."""

    __table_args__ = (UniqueConstraint("account_id", "name"),)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_id: UUID = Field(foreign_key=Account.id, index=True)
    """ID of owning account."""
    name: str
    """Instance name."""
    storage_id: UUID = Field(foreign_key=Storage.id, index=True)
    """Default storage for loading an instance."""
    db_scheme: Optional[str] = Field(default="postgresql")  # default to postgres
    db_host: Optional[str]  # e.g., 123.456.897.123
    db_port: Optional[int]  # e.g., 5432
    db_database: Optional[str]
    db_users: List["DBUser"] = Relationship(back_populates="instance")
    db: Optional[str] = Field(
        default=None, unique=True
    )  # TODO: remove after individual database fields are validated
    """Database connection string. None for SQLite."""
    schema_str: Optional[str] = None
    """Comma-separated string of schema modules."""
    description: Optional[str] = None
    """Short text describing the instance."""
    public: Optional[bool] = False
    """Flag indicating if the instance is publicly visible."""
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class DBUser(SQLModel, table=True):  # type: ignore
    __tablename__ = "db_user"
    __table_args__ = (UniqueConstraint("instance_id", "db_user_name"),)

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    instance_id: UUID = Field(
        sa_column=Column(
            sqlmodel.sql.sqltypes.GUID(),
            ForeignKey(Instance.id, ondelete="CASCADE"),
            index=True,
        )
    )
    instance: Instance = Relationship(back_populates="db_users")
    name: Optional[str] = None  # e.g., "Data science team 1"
    db_user_name: str  # e.g., team1
    db_user_password: str


class AccountInstance(SQLModel, table=True):  # type: ignore
    """Relationships between accounts and instances."""

    __tablename__ = "account_instance"
    __table_args__ = (PrimaryKeyConstraint("account_id", "instance_id"),)

    account_id: UUID = Field(
        sa_column=Column(
            sqlmodel.sql.sqltypes.GUID(),
            ForeignKey(Account.id, ondelete="CASCADE"),
            index=True,
        )
    )
    instance_id: UUID = Field(
        sa_column=Column(
            sqlmodel.sql.sqltypes.GUID(),
            ForeignKey(Instance.id, ondelete="CASCADE"),
            index=True,
        )
    )
    role: instance_role = instance_role.read
    db_user_id: Optional[UUID] = Field(foreign_key=DBUser.id, index=True)
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class OrganizationUser(SQLModel, table=True):  # type: ignore
    """Relationships between organizational accounts and users."""

    __tablename__ = "organization_user"
    __table_args__ = (PrimaryKeyConstraint("organization_id", "user_id"),)

    organization_id: UUID = Field(
        sa_column=Column(
            sqlmodel.sql.sqltypes.GUID(),
            ForeignKey(Account.id, ondelete="CASCADE"),
            index=True,
        )
    )
    user_id: UUID = Field(
        sa_column=Column(
            sqlmodel.sql.sqltypes.GUID(),
            ForeignKey(User.id, ondelete="CASCADE"),
            index=True,
        )
    )
    role: organization_role = organization_role.member
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt


class CloudRunInstance(SQLModel, table=True):  # type: ignore
    """Instances deployed in Cloud Run."""

    __tablename__ = "cloud_run_instance"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    lamin_instance_id: UUID = Field(
        sa_column=Column(
            sqlmodel.sql.sqltypes.GUID(),
            ForeignKey(Instance.id, ondelete="CASCADE"),
            index=True,
        )
    )
    cloud_run_instance_name: str
    api_url: str
    last_access_at: Optional[datetime] = None
    created_at: datetime = CreatedAt
    updated_at: Optional[datetime] = UpdatedAt
