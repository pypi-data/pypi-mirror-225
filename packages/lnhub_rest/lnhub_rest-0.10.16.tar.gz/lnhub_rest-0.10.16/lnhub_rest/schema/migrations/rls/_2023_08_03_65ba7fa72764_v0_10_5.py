sql_rls_cloud_run_instance = """
    CREATE POLICY "Enable anyone to select the Cloud Run instance for public instances"
    ON public.cloud_run_instance
    FOR SELECT USING (
        is_instance_public(lamin_instance_id)
    );

    CREATE POLICY "Enable anyone to update a Cloud Run instance"
    ON public.cloud_run_instance
    FOR UPDATE USING (
        true
    );

    DROP POLICY "Enable instance owner or admin collaborators to create a Cloud Run instance" ON public.cloud_run_instance;

    DROP POLICY "Enable instance owner or admin collaborators to delete their Cloud Run instance" ON public.cloud_run_instance;

"""  # noqa

sql_rls_account_instance = """
    CREATE POLICY "Enable everyone to select collaborators for public instances"
    ON public.account_instance
    FOR SELECT USING (
        is_instance_public(instance_id)
    );
"""  # noqa

drop_rls_cloud_run_instance = """
    CREATE POLICY "Enable instance owner or admin collaborators to create a Cloud Run instance"
    ON public.cloud_run_instance
    FOR INSERT
    WITH CHECK (
        is_instance_owner(auth.uid(), lamin_instance_id) OR is_instance_admin(auth.uid(), lamin_instance_id)
    );

    CREATE POLICY "Enable instance owner or admin collaborators to delete their Cloud Run instance"
    ON public.cloud_run_instance
    FOR DELETE USING (
        is_instance_owner(auth.uid(), lamin_instance_id) OR is_instance_admin(auth.uid(), lamin_instance_id)
    );

    DROP POLICY "Enable anyone to select the Cloud Run instance for public instances" ON public.cloud_run_instance;

    DROP POLICY "Enable anyone to update a Cloud Run instance" ON public.cloud_run_instance;
"""  # noqa

drop_sql_rls_account_instance = """
    DROP POLICY "Enable everyone to select collaborators for public instances" ON public.account_instance;
"""  # noqa
