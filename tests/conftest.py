import os
import sys
import pytest

os.environ.setdefault("MYSQL_PASSWORD", "test-dummy")
os.environ.setdefault("MAIL_PASSWORD", "test-dummy")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module


@pytest.fixture(scope="session")
def client():
    app_module.app.config.update(TESTING=True)
    with app_module.app.test_client() as test_client:
        yield test_client
