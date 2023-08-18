from typing import Annotated

from fastapi import Query
from supabase.client import Client


def sb_insert_account(
    account_fields: dict,
    supabase_client: Client,
):
    data = supabase_client.table("account").insert(account_fields).execute().data
    if len(data) == 0:
        return None
    return data[0]


def sb_update_account(
    account_id: str,
    account_fields: dict,
    supabase_client: Client,
):
    data = (
        supabase_client.table("account")
        .update(account_fields)
        .eq("id", account_id)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]


def sb_select_account_by_id(
    id: str,
    supabase_client: Client,
):
    data = supabase_client.table("account").select("*").eq("id", id).execute().data
    if len(data) == 0:
        return None
    return data[0]


def sb_select_account_by_handle(
    handle: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("account").select("*").eq("handle", handle).execute().data
    )
    if len(data) == 0:
        return None
    return data[0]


def sb_select_all_accounts(supabase_client: Client):
    accounts = supabase_client.table("account").select("*").execute().data
    return accounts


def sb_delete_account(
    handle: str,
    supabase_client: Client,
):
    data = supabase_client.table("account").delete().eq("handle", handle).execute().data
    if len(data) == 0:
        return None
    return data[0]


def sb_select_single_avatar(
    lnid: str,
    supabase_client: Client,
):
    data = (
        supabase_client.table("account")
        .select("avatar_url")
        .eq("lnid", lnid)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]["avatar_url"]


def sb_select_bulk_avatars(
    lnids: Annotated[list[str], Query()],
    supabase_client: Client,
):
    data = (
        supabase_client.table("account")
        .select("lnid, avatar_url")
        .in_("lnid", lnids)
        .execute()
        .data
    )
    if len(data) == 0:
        return []
    return data


def sb_select_account_instances(
    handle: str,
    supabase_client: Client,
):
    account_instances = (
        supabase_client.table("account")
        .select(
            "account_instance(instance(*, storage(root),"
            " account!fk_instance_account_id_account(handle, id)))"
        )
        .eq("handle", handle)
        .execute()
        .data[0]["account_instance"]
    )
    account_instances = [entry["instance"] for entry in account_instances]
    return account_instances


def sb_select_account_own_instances(
    handle: str,
    supabase_client: Client,
):
    own_instances = (
        supabase_client.table("account")
        .select(
            "instance!fk_instance_account_id_account(*, storage(root),"
            " account!fk_instance_account_id_account(handle, id))"
        )
        .eq("handle", handle)
        .execute()
        .data[0]["instance"]
    )
    return own_instances


def sb_select_user_organizations(
    user_id: str,
    supabase_client: Client,
):
    organizations_user = (
        supabase_client.table("organization_user")
        .select("""*, account(*)""")
        .eq("user_id", user_id)
        .execute()
        .data
    )
    return organizations_user
