from datetime import datetime
from typing import Union

from fastapi import APIRouter, Header

from lnhub_rest.orm._sbclient import connect_hub_with_service_role

from .utils import extract_access_token, get_supabase_client

router = APIRouter(prefix="/cloud-run")


@router.get("/linked-instance/{lamin_instance_id}")
def get_linked_cloud_run_instance(
    lamin_instance_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    access_token = extract_access_token(authentication)
    supabase_client = get_supabase_client(access_token)

    try:
        data = (
            supabase_client.table("cloud_run_instance")
            .select("*")
            .eq("lamin_instance_id", lamin_instance_id)
            .execute()
            .data
        )
        if len(data) == 0:
            return None
        return data[0]
    finally:
        supabase_client.auth.sign_out()


@router.post("/auto-link/{lamin_instance_id}")
def link_to_evicted_cloud_run_instance(
    lamin_instance_id: str,
    authentication: Union[str, None] = Header(default=None),
):
    # access_token = extract_access_token(authentication)
    supabase_client = connect_hub_with_service_role()
    cloud_run_instance_id = get_evicted_cloud_run_instance(authentication)["id"]

    try:
        data = (
            supabase_client.table("cloud_run_instance")
            .update(
                {
                    "lamin_instance_id": lamin_instance_id,
                    "updated_at": str(datetime.now()),
                    "last_access_at": str(datetime.now()),
                }
            )
            .eq("id", cloud_run_instance_id)
            .execute()
            .data
        )
        if len(data) == 0:
            return None
        return data[0]
    finally:
        supabase_client.auth.sign_out()


@router.post("/link/{lamin_instance_id}/{cloud_run_instance_id}")
def link_to_cloud_run_instance(lamin_instance_id: str, cloud_run_instance_id: str):
    # access_token = extract_access_token(authentication)
    supabase_client = connect_hub_with_service_role()

    try:
        data = (
            supabase_client.table("cloud_run_instance")
            .update(
                {
                    "lamin_instance_id": lamin_instance_id,
                    "updated_at": str(datetime.now()),
                    "last_access_at": str(datetime.now()),
                }
            )
            .eq("id", cloud_run_instance_id)
            .execute()
            .data
        )
        if len(data) == 0:
            return None
        return data[0]
    finally:
        supabase_client.auth.sign_out()


@router.get("/{cloud_run_instance_name}")
def get_cloud_run_instance_by_name(cloud_run_instance_name: str):
    supabase_client = connect_hub_with_service_role()

    try:
        data = (
            supabase_client.table("cloud_run_instance")
            .select("*")
            .eq("cloud_run_instance_name", cloud_run_instance_name)
            .execute()
            .data
        )
        if len(data) == 0:
            return None
        return data[0]
    finally:
        supabase_client.auth.sign_out()


@router.post("/update-last-access-at/{cloud_run_instance_id}")
def update_last_access_at(cloud_run_instance_id: str):
    supabase_client = connect_hub_with_service_role()

    try:
        data = (
            supabase_client.table("cloud_run_instance")
            .update(
                {
                    "last_access_at": str(datetime.now()),
                }
            )
            .eq("id", cloud_run_instance_id)
            .execute()
            .data
        )
        if len(data) == 0:
            return None
        return data[0]
    finally:
        supabase_client.auth.sign_out()


def get_evicted_cloud_run_instance(
    authentication: Union[str, None] = Header(default=None)
):
    # access_token = extract_access_token(authentication)
    supabase_client = connect_hub_with_service_role()

    try:
        data = (
            supabase_client.table("cloud_run_instance")
            .select("*")
            .order("last_access_at")
            .like("cloud_run_instance_name", "generic-instance-%")
            .execute()
            .data
        )
        if len(data) == 0:
            return None
        return data[0]
    finally:
        supabase_client.auth.sign_out()


def get_default_instance_identifier():
    return "laminlabs/laminapp-default-instance"
