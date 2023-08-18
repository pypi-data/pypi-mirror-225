from typing import Union

import jwt
from fastapi import Header

from lnhub_rest.core.collaborator._crud import sb_select_collaborator_role
from lnhub_rest.orm._sbclient import connect_hub, connect_hub_with_auth

supabase_client = connect_hub()


def get_account_role_for_instance(instance_id: str, access_token: str):
    """Get authenticated account's role for an instance.

    Returns:
        role (str): collaborator role. One of "admin", "write", or "read". If
            account is not a collaborator, returns None.
    """
    supabase_client = connect_hub_with_auth(access_token=access_token)
    session_payload = jwt.decode(
        access_token, algorithms="HS256", options={"verify_signature": False}
    )
    role = sb_select_collaborator_role(
        session_payload["sub"], instance_id, supabase_client
    )
    return role


def extract_access_token(authentication: Union[str, None] = Header(default=None)):
    if authentication is not None:
        return authentication.split(" ")[1]
    return None


def get_supabase_client(access_token: Union[str, None]):
    if access_token is None:
        return connect_hub()
    else:
        return connect_hub_with_auth(access_token=access_token)


def get_user_by_id(id: str, authentication: Union[str, None] = Header(default=None)):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)
    user = supabase_client.table("users").select("*").eq("id", id).execute().data
    if len(user) == 0:
        return None
    return user[0]
