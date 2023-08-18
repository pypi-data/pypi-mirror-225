import os
from pathlib import Path

import nbproject_test as test

# assuming this is in the tests folder
DOCS_FOLDER = Path(__file__).parents[1] / "docs/"
LAMIN_ENV = os.environ.get("LAMIN_ENV", "local")


def test_local():
    # logger.debug("\nmigrate")
    # test.execute_notebooks(DOCS_FOLDER, write=True)

    print("\naccount")
    test.execute_notebooks(DOCS_FOLDER / "02-account/", write=True)

    print("\ninstance")
    test.execute_notebooks(DOCS_FOLDER / "03-instance/", write=True)

    print("\nstorage")
    test.execute_notebooks(DOCS_FOLDER / "04-storage/", write=True)

    print("\norganization")
    test.execute_notebooks(DOCS_FOLDER / "05-organization/", write=True)
