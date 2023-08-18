from typing import Union

from fastapi import APIRouter, Header

from lnhub_rest.core.collaborator._crud import sb_insert_collaborator
from lnhub_rest.core.db_user._crud import sb_select_db_user_by_instance
from lnhub_rest.core.instance._crud import (
    sb_select_full_instance_by_name,
    sb_select_instance_accounts,
)
from lnhub_rest.core.instance._delete_instance import (
    delete_instance as delete_instance_base,
)
from lnhub_rest.core.instance._update_instance import (
    update_instance as update_instance_base,
)

from .account import get_account_by_handle
from .utils import (
    extract_access_token,
    get_account_role_for_instance,
    get_supabase_client,
)

router = APIRouter(prefix="/instance")


@router.get("/{account_handle}/{name}")
def get_instance_by_name(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Get full instance information by name.

    Returns:
        instance_with_role (dict): dictionary with keys "instance" and "role".
            "instance": instance(*, storage(root), account(handle, id))
            "role": "admin", "write", or "read"
    """
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        account = get_account_by_handle(account_handle)
        instance = sb_select_full_instance_by_name(account["id"], name, supabase_client)

        if instance is not None:
            if authentication is not None:
                role = get_account_role_for_instance(instance["id"], access_token)
            else:
                role = None
        else:
            role = None

        instance_with_role = {"instance": instance, "role": role}

        return instance_with_role

    finally:
        supabase_client.auth.sign_out()


@router.get("/resources/accounts/{account_handle}/{name}")
def get_instance_accounts(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Get collaborators of an instance.

    Returns:
        collaborators_with_role (dict):  dictionary with keys "accounts" and "role".
            "accounts": account_instance(*, account(*)). Returns None if no
                collaborators exist.
            "role": "admin", "write", or "read". Returns None if caller not
                authenticated or no collaborators exist.
    """
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        account = get_account_by_handle(account_handle)
        instance_accounts = sb_select_instance_accounts(
            account["id"], name, supabase_client
        )
        if instance_accounts is not None:
            collaborators = instance_accounts["account_instance"]
            if authentication is not None:
                role = get_account_role_for_instance(
                    instance_accounts["id"], access_token
                )
            else:
                role = None
        else:
            collaborators = None
            role = None

        collaborators_with_role = {"accounts": collaborators, "role": role}

        return collaborators_with_role

    finally:
        supabase_client.auth.sign_out()


@router.post("/resources/accounts/")
def add_collaborator(
    handle: str,
    instance_owner_handle: str,
    instance_name: str,
    role: str = "read",
    authentication: Union[str, None] = Header(default=None),
):
    """Add collaborator in the hub.

    Returns:
        message (str): status message. "success", "collaborator-exists-already",
            or "account-not-exists".
    """
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        account = get_account_by_handle(handle)
        if account is None:
            return "account-not-exists"
        response = get_instance_by_name(
            instance_owner_handle, instance_name, authentication
        )
        if response["instance"] is None:
            return "instance-not-exists"
        if response["instance"]["db"] is None or response["instance"]["db"].startswith(
            "sqlite://"
        ):
            db_user_id = None
        else:
            db_user = sb_select_db_user_by_instance(
                response["instance"]["id"], supabase_client
            )
            if db_user is None:
                return "db-user-not-reachable"
            else:
                db_user_id = db_user["id"]

        account_instance_fields = {
            "account_id": account["id"],
            "instance_id": response["instance"]["id"],
            "role": role,
            "db_user_id": db_user_id,
        }
        data = sb_insert_collaborator(account_instance_fields, supabase_client)

        assert data is not None

        if data == "collaborator-exists-already":
            return data
        return "success"

    finally:
        supabase_client.auth.sign_out()


@router.delete("/")
def delete_instance(
    account_handle: str,
    name: str,
    authentication: Union[str, None] = Header(default=None),
):
    """Delete instance in the hub.

    Returns:
        message (str): status message. "sucess", "account-not-exists", or
            "instance-not-reachable".
    """
    access_token = extract_access_token(authentication)
    message = delete_instance_base(
        owner=account_handle, name=name, _access_token=access_token
    )
    if message is None:
        return "success"
    return message


@router.put("/")
def update_instance(
    instance_id: str,
    account_id: Union[str, None] = None,
    public: Union[bool, None] = None,
    description: Union[str, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    """Update instance in the Hub.

    Returns:
        message (str): status message. "success" or "instance-not-updated".
    """
    access_token = extract_access_token(authentication)
    message = update_instance_base(
        instance_id=instance_id,
        account_id=account_id,
        public=public,
        description=description,
        _access_token=access_token,
    )
    if message is None:
        return "success"
    return message
