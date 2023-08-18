from typing import Annotated, Union

from fastapi import APIRouter, Header, Query

from ..core.account._create_account import (
    create_organization_account,
    create_user_account,
)
from ..core.account._crud import (
    sb_select_account_by_handle,
    sb_select_account_by_id,
    sb_select_account_instances,
    sb_select_account_own_instances,
    sb_select_bulk_avatars,
    sb_select_single_avatar,
    sb_select_user_organizations,
)
from ..core.account._update_account import update_account as update_account_base
from .utils import extract_access_token, get_supabase_client

router = APIRouter(prefix="/account")


@router.post("/")
def create_account(
    handle: str,
    organization: Union[bool, None] = False,
    authentication: Union[str, None] = Header(default=None),
):
    """Create user or organization account in the Hub.

    Returns:
        message (str): status message. "success" or "handle-exists-already".
    """
    access_token = extract_access_token(authentication)
    if organization:
        message = create_organization_account(
            handle=handle,
            _access_token=access_token,
        )
    else:
        message = create_user_account(
            handle=handle,
            _access_token=access_token,
        )
    if message is None:
        return "success"
    return message


@router.put("/")
def update_account(
    handle: Union[str, None] = None,
    name: Union[str, None] = None,
    bio: Union[str, None] = None,
    github_handle: Union[str, None] = None,
    linkedin_handle: Union[str, None] = None,
    twitter_handle: Union[str, None] = None,
    website: Union[str, None] = None,
    authentication: Union[str, None] = Header(default=None),
):
    """Update account in the Hub.

    Returns:
        message (str): status message. "sucess" or "account-not-exists".
    """
    access_token = extract_access_token(authentication)
    message = update_account_base(
        handle=handle,
        name=name,
        bio=bio,
        github_handle=github_handle,
        linkedin_handle=linkedin_handle,
        twitter_handle=twitter_handle,
        website=website,
        _access_token=access_token,
    )
    if message is None:
        return "success"
    return message


@router.get("/bulk/avatars")
def get_account_avatars(lnids: Annotated[list[str], Query()]):
    """Get list of account records with their avatar URLs.

    Returns:
        bulk_avatars (List): list of account(lnid, avatar_url) records.
            Empty list if none are found.
    """
    supabase_client = get_supabase_client(None)
    bulk_avatars = sb_select_bulk_avatars(lnids, supabase_client)
    return bulk_avatars


@router.get("/avatar")
def get_account_avatar(lnid: str):
    """Get avatar URL for a single account.

    Returns:
        avatar (Union[str, None]): avatar URL. Returns None if not found.
    """
    supabase_client = get_supabase_client(None)
    avatar = sb_select_single_avatar(lnid, supabase_client)
    return avatar


@router.get("/{id}")
def get_account_by_id(id: str):
    """Get single account associated with an id.

    Returns:
        account (Union[dict, None]): account(*) record. Returns None if not found.
    """
    supabase_client = get_supabase_client(None)
    account = sb_select_account_by_id(id, supabase_client)
    return account


@router.get("/handle/{handle}")
def get_account_by_handle(handle: str):
    """Get single account associated with a handle.

    Returns:
        account (Union[dict, None]): account(*) record. Returns None if not found.
    """
    supabase_client = get_supabase_client(None)
    account = sb_select_account_by_handle(handle, supabase_client)
    return account


@router.get("/resources/instances/{handle}")
def get_account_instances(
    handle: str,
    owner: bool = False,
    authentication: Union[str, None] = Header(default=None),
):
    """Get list of instances in which an account is a collaborator.

    Returns:
        account_instances (List): list of instance(*, storage(root),
            account(handle, id)) records. Returns empty list if not found.
    """
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        if owner:
            account_instances = sb_select_account_own_instances(handle, supabase_client)
        else:
            account_instances = sb_select_account_instances(handle, supabase_client)
        return account_instances
    finally:
        supabase_client.auth.sign_out()


@router.get("/resources/organizations/{handle}")
def get_account_organizations(
    handle: str, authentication: Union[str, None] = Header(default=None)
):
    """Get list of organization_user records with which an account is associated.

    Returns:
        organizations_user (List): list of organization_user(*, account(*))
            records. Returns empty list if not found.
    """
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        user_id = get_account_by_handle(handle)["id"]
        organizations_user = sb_select_user_organizations(user_id, supabase_client)
        return organizations_user

    finally:
        supabase_client.auth.sign_out()
