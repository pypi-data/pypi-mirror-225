sql_drop_rls_db_user = """
    DROP POLICY "Enable owner all operations database user" ON public.db_user;
    DROP POLICY "Enable admin collaborators to add database user" ON public.db_user;
    DROP POLICY "Enable admin collaborators to update database user" ON public.db_user;
    DROP POLICY "Enable admin collaborators to delete database user" ON public.db_user;
    DROP POLICY "Enable owner to delete database user" ON public.db_user;
    DROP POLICY "Enable collaborators to select db user of their instances" ON public.db_user;
"""  # noqa

sql_rls_db_user = """
    ALTER TABLE db_user ENABLE ROW LEVEL SECURITY;
    CREATE POLICY "Enable owner all operations database user"
    ON "public"."db_user"
    AS PERMISSIVE FOR ALL
    TO public
    USING (is_instance_owner(auth.uid(), instance_id))
    WITH CHECK (is_instance_owner(auth.uid(), instance_id));
    CREATE POLICY "Enable admin collaborators to add database user"
    ON public.db_user
    FOR INSERT
    WITH CHECK (
        is_instance_admin(auth.uid(), instance_id)
    );
    CREATE POLICY "Enable admin collaborators to update database user"
    ON public.db_user
    FOR UPDATE USING (
        is_instance_admin(auth.uid(), instance_id)
    )
    WITH CHECK (
        is_instance_admin(auth.uid(), instance_id)
    );
    CREATE POLICY "Enable admin collaborators to delete database user"
    ON public.db_user
    FOR DELETE USING (
        is_instance_admin(auth.uid(), instance_id)
    );
    CREATE POLICY "Enable owner to delete database user"
    ON public.db_user
    FOR DELETE USING (
        is_instance_owner(auth.uid(), instance_id)
    );
    CREATE POLICY "Enable collaborators to select db user of their instances"
    ON public.db_user
    FOR SELECT USING (
        is_instance_collaborator(auth.uid(), instance_id)
    );
"""  # noqa
