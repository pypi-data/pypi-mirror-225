"""Schema."""
from .. import __version__ as _version

_schema_id = "cbwk"
_name = "hub"
_migration = "65ba7fa72764"
__version__ = _version

from . import versions  # noqa
from ._core import Account, Instance, OrganizationUser, Storage, User  # noqa
