import os
import shutil
from pathlib import Path

import nox
from laminci.nox import login_testuser1, login_testuser2, run_pre_commit

nox.options.default_venv_backend = "none"


@nox.session
def lint(session: nox.Session) -> None:
    run_pre_commit(session)


@nox.session
def test_lnhub_ui(session: nox.Session):
    session.run(*"pip install -e .[dev,test,server]".split())
    session.run(
        "lnhub",
        "alembic",
        "upgrade",
        "head",
        env={
            "LAMIN_ENV": "local",
        },
    )
    session.run(
        "pytest",
        "-n",
        "1",  # ensure that supabase thread exits properly
        "-s",
        "--cov=lnhub_rest",
        "--cov-append",
        "--cov-report=term-missing",
        env={
            "LAMIN_ENV": "local",
            "POSTGRES_DSN": os.environ["DB_URL"].replace('"', ""),
            "SUPABASE_API_URL": os.environ["API_URL"].replace('"', ""),
            "SUPABASE_ANON_KEY": os.environ["ANON_KEY"].replace('"', ""),
            "SUPABASE_SERVICE_ROLE_KEY": os.environ["SERVICE_ROLE_KEY"].replace(
                '"', ""
            ),
        },
    )


@nox.session
@nox.parametrize("lamin_env", ["local", "staging", "prod"])
def test_lamindb_setup(session: nox.Session, lamin_env: str):
    # define environment
    env = {
        "LAMIN_ENV": lamin_env,
        "SUPABASE_API_URL": os.environ["API_URL"].replace('"', "")
        if lamin_env == "local"
        else os.environ["SUPABASE_API_URL"],
        "SUPABASE_ANON_KEY": os.environ["ANON_KEY"].replace('"', "")
        if lamin_env == "local"
        else os.environ["SUPABASE_ANON_KEY"],
        "SUPABASE_SERVICE_ROLE_KEY": os.environ["SERVICE_ROLE_KEY"].replace('"', "")
        if lamin_env == "local"
        else os.environ["SUPABASE_SERVICE_ROLE_KEY"],
    }
    session.run(*"pip install .[dev,test,server]".split())
    session.run(*"pip install ./lamindb-setup[dev,test,aws]".split())
    if lamin_env != "local":
        # this is running "integration tests" within lamindb-setup against
        # staging and prod
        login_testuser1(session, env=env)
        login_testuser2(session, env=env)
        with session.chdir("./lamindb-setup"):
            session.run(
                *"pytest -n 1 --ignore tests/test_bionty.py --ignore tests/hub"
                " ./tests".split(),
                env=env
            )
    else:
        # in order to run local hub tests within lamindb-setup, need to
        # replicate fixtures
        # will need the following line soon!
        # Path("./lamindb-setup/tests/conftest.py").rename(
        #     "./lamindb-setup/tests/conftest_save.py"
        # )
        session.run(
            "lnhub",
            "alembic",
            "upgrade",
            "head",
            env={
                "LAMIN_ENV": "local",
            },
        )
        shutil.copy("./tests/conftest.py", "./lamindb-setup/tests/")
        try:
            with session.chdir("./lamindb-setup"):
                session.run(*"pytest -n 1 ./tests/hub".split(), env=env)
        finally:
            # clean up temporary conftest.py
            Path("./lamindb-setup/tests/conftest.py").unlink()
            # will need the following line soon!
            # Path("./lamindb-setup/tests/conftest_save.py").rename(
            #     "./lamindb-setup/tests/conftest.py"
            # )
