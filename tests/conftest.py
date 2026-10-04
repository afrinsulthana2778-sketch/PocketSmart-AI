import os
import tempfile

from pathlib import Path


os.environ["SECRET_KEY"] = (
    "a" * 64
)

os.environ["GEMINI_API_KEY"] = ""


import db


TEST_DB = (
    Path(tempfile.gettempdir())
    / "pocketsmart_test.db"
)


db.DB_PATH = TEST_DB


from fastapi.testclient import TestClient

from app import app

import pytest


@pytest.fixture()
def client():

    if TEST_DB.exists():

        TEST_DB.unlink()

    db.init_db()

    with TestClient(app) as client:

        yield client