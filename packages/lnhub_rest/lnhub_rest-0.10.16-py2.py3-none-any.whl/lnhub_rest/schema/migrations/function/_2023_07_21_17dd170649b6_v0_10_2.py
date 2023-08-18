sql_function_is_instance_public = """
    CREATE OR REPLACE FUNCTION is_instance_public(_instance_id uuid) RETURNS boolean
       LANGUAGE plpgsql
       SECURITY DEFINER SET search_path = public
    AS
    $$BEGIN
       RETURN EXISTS (SELECT 1 FROM instance AS ai
                      WHERE ai.id = _instance_id
                      AND public = TRUE);
    END;$$;
"""  # noqa
