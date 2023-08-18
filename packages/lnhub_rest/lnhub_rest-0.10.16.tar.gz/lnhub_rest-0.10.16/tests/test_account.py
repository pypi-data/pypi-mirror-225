import pytest
from faker import Faker

from lnhub_rest.core.account import create_user_account, update_account
from lnhub_rest.core.account._crud import (
    sb_delete_account,
    sb_insert_account,
    sb_select_account_by_handle,
    sb_update_account,
)
from lnhub_rest.orm._sbclient import connect_hub_with_auth
from lnhub_rest.utils._id import base62
from lnhub_rest.utils._test import create_test_auth

FAKE = Faker()


def test_create_duplicate_user_account(auth_1, user_account_1):
    message = create_user_account(
        handle=auth_1["handle"],
        _access_token=auth_1["access_token"],
    )
    assert message == "handle-exists-already"


def test_update_account(auth_1, user_account_1, hub):
    new_name = FAKE.name()
    message = update_account(
        handle=user_account_1["handle"],
        name=new_name,
        bio=None,
        github_handle=None,
        linkedin_handle=None,
        twitter_handle=None,
        website=None,
        _access_token=auth_1["access_token"],
    )

    assert message is None

    account = sb_select_account_by_handle(user_account_1["handle"], hub)
    assert account["name"] == new_name


def test_update_nonexisting_account(auth_2):
    new_auth = create_test_auth()
    new_name = FAKE.name()
    message = update_account(
        handle="account_2 handle",  # this handle doesn't exist
        name=new_name,
        bio=None,
        github_handle=None,
        linkedin_handle=None,
        twitter_handle=None,
        website=None,
        _access_token=new_auth["access_token"],
    )
    assert message == "account-not-exists"


def test_everyone_can_see_account(hub, user_account_2):
    account = sb_select_account_by_handle(user_account_2["handle"], hub)
    assert account


def test_anon_supabase_client_cannot_insert_account(auth_1, hub):
    with pytest.raises(Exception) as error:
        _ = sb_insert_account(
            account_fields={
                "id": auth_1["id"],
                "user_id": auth_1["id"],
                "lnid": base62(8),
                "handle": auth_1["handle"],
            },
            supabase_client=hub,
        )

        assert "new row violates row-level security policy" in error.value.message


def test_auth_supabase_client_can_insert_account(auth_1, account_hub_1):
    auth = create_test_auth()
    try:
        hub = connect_hub_with_auth(access_token=auth["access_token"])
        account = sb_insert_account(
            account_fields={
                "id": auth["id"],
                "user_id": auth["id"],
                "lnid": base62(8),
                "handle": auth["handle"],
            },
            supabase_client=hub,
        )
        assert account
    finally:
        hub.auth.sign_out()


def test_auth_supabase_client_can_update_account(auth_1, user_account_1, account_hub_1):
    new_name = FAKE.name()
    account = sb_update_account(
        account_id=auth_1["id"],
        account_fields={"name": new_name},
        supabase_client=account_hub_1,
    )
    assert account is not None

    assert (
        sb_select_account_by_handle(
            handle=auth_1["handle"], supabase_client=account_hub_1
        )["name"]
        == new_name  # noqa: W503
    )


def test_wrong_auth_supabase_client_cannot_update_account(
    auth_1, user_account_1, account_hub_1, account_hub_2
):
    new_name = FAKE.name()
    account = sb_update_account(
        account_id=auth_1["id"],
        account_fields={"name": new_name},
        supabase_client=account_hub_2,
    )
    assert account is None

    assert (
        sb_select_account_by_handle(
            handle=auth_1["handle"], supabase_client=account_hub_1
        )["name"]
        != new_name  # noqa: W503
    )


def test_anon_auth_supabase_client_cannot_update_account(auth_1, user_account_1, hub):
    new_name = FAKE.name()
    account = sb_update_account(
        account_id=auth_1["id"],
        account_fields={"name": new_name},
        supabase_client=hub,
    )
    assert account is None

    assert (
        sb_select_account_by_handle(handle=auth_1["handle"], supabase_client=hub)[
            "name"
        ]
        != new_name  # noqa: W503
    )


def test_auth_supabase_client_can_delete_account(account_to_test_deletion):
    """RLS will allow deletion."""
    auth, account_hub, _ = account_to_test_deletion
    account = sb_delete_account(handle=auth["handle"], supabase_client=account_hub)

    assert (
        sb_select_account_by_handle(handle=auth["handle"], supabase_client=account_hub)
        is None
    )
    assert account


def test_wrong_auth_supabase_client_cannot_delete_account(
    auth_2, user_account_2, account_hub_1, account_hub_2
):
    """RLS will prevent deletion."""
    account = sb_delete_account(handle=auth_2["handle"], supabase_client=account_hub_1)

    assert (
        sb_select_account_by_handle(
            handle=auth_2["handle"], supabase_client=account_hub_2
        )
        is not None
    )
    assert account is None


def test_anon_auth_supabase_client_cannot_delete_account(auth_2, user_account_2, hub):
    """RLS will prevent deletion."""
    account = sb_delete_account(handle=auth_2["handle"], supabase_client=hub)

    assert (
        sb_select_account_by_handle(handle=auth_2["handle"], supabase_client=hub)
        is not None
    )
    assert account is None
