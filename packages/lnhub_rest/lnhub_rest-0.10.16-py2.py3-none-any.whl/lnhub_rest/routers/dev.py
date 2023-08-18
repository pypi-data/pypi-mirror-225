import os

from fastapi import APIRouter

from ..core.account._crud import sb_select_all_accounts
from .utils import supabase_client

router = APIRouter(prefix="/dev")


@router.delete("/env")
def env():
    if "LAMIN_ENV" in os.environ:
        return os.environ["LAMIN_ENV"]
    else:
        return None


@router.delete("/count/account")
def count_accounts():
    """Get total number of registered accounts.

    Returns:
        num_accounts (int): total number of registered accounts.
    """
    accounts = sb_select_all_accounts(supabase_client)
    num_accounts = len(accounts)
    return num_accounts
