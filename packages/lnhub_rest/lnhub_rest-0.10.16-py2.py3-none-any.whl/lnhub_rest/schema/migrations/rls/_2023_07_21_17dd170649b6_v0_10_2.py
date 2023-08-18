sql_rls_cloud_run_instance = """
    ALTER TABLE cloud_run_instance ENABLE ROW LEVEL SECURITY;

    CREATE POLICY "Enable owners to select their Cloud Run instance"
    ON public.cloud_run_instance
    FOR SELECT USING (
        is_instance_owner(auth.uid(), lamin_instance_id)
    );

    CREATE POLICY "Enable collaborators to select their Cloud Run instance"
    ON public.cloud_run_instance
    FOR SELECT USING (
        is_instance_collaborator(auth.uid(), lamin_instance_id)
    );

    CREATE POLICY "Enable instance owner or admin collaborators to create a Cloud Run instance"
    ON public.cloud_run_instance
    FOR INSERT
    WITH CHECK (
        is_instance_owner(auth.uid(), lamin_instance_id) OR is_instance_admin(auth.uid(), lamin_instance_id)
    );

    CREATE POLICY "Enable admin collaborators to update their Cloud Run instance"
    ON public.cloud_run_instance
    FOR UPDATE USING (
        is_instance_admin(auth.uid(), lamin_instance_id)
    )
    WITH CHECK (
        is_instance_admin(auth.uid(), lamin_instance_id)
    );

    CREATE POLICY "Enable instance owner or admin collaborators to delete their Cloud Run instance"
    ON public.cloud_run_instance
    FOR DELETE USING (
        is_instance_owner(auth.uid(), lamin_instance_id) OR is_instance_admin(auth.uid(), lamin_instance_id)
    );
"""  # noqa

sql_drop_rls_cloud_run_instance = """
    DROP POLICY "Enable owners to select their Cloud Run instance" ON public.cloud_run_instance;
    DROP POLICY "Enable collaborators to select their Cloud Run instance" ON public.cloud_run_instance;
    DROP POLICY "Enable instance owner or admin collaborators to create a Cloud Run instance" ON public.cloud_run_instance;
    DROP POLICY "Enable admin collaborators to update their Cloud Run instance" ON public.cloud_run_instance;
    DROP POLICY "Enable instance owner or admin collaborators to delete their Cloud Run instance" ON public.cloud_run_instance;
"""  # noqa

sql_rls_db_user_public = """
    CREATE POLICY "Enable everyone to select database users for public instances"
    ON public.db_user
    FOR SELECT USING (
        is_instance_public(instance_id)
    );

"""  # noqa

sql_drop_rls_db_user_public = """
    DROP POLICY "Enable everyone to select database users for public instances" on public.db_user
"""  # noqa
