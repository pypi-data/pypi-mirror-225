from supabase.client import Client


def sb_select_db_user_by_instance(instance_id: str, supabase_client: Client):
    """Get the DBAccount directly associated with Instance.

    By contrast this is not the DBAccount that is linked through the
    UserInstance table.
    """
    data = (
        supabase_client.table("db_user")
        .select("*")
        .eq("instance_id", instance_id)
        .execute()
        .data
    )
    if len(data) == 0:
        return None
    return data[0]
