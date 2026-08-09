"""Contact and job application form tests.

The real MySQL database is never touched; get_db_connection() is
monkeypatched so behaviour is deterministic offline.
"""

import pytest

import app as app_module


class FakeCursor:
    def execute(self, *args, **kwargs):
        pass

    def close(self):
        pass


class FakeConnection:
    def cursor(self):
        return FakeCursor()

    def commit(self):
        pass

    def close(self):
        pass


def test_contact_get_renders(client):
    resp = client.get("/contact")
    assert resp.status_code == 200


def test_contact_post_missing_fields_redirects_empty(client):
    resp = client.post("/contact", data={"name": "", "email": "", "phoneno": "", "textarea": ""})
    assert resp.status_code == 302
    assert resp.location.endswith("status=empty")


def test_contact_post_db_unavailable_redirects_db_error(client, monkeypatch):
    monkeypatch.setattr(app_module, "get_db_connection", lambda: None)
    resp = client.post(
        "/contact",
        data={"name": "Tester", "email": "t@example.com", "phoneno": "123", "textarea": "Hello"},
    )
    assert resp.status_code == 302
    assert resp.location.endswith("status=db_error")


def test_contact_post_success(client, monkeypatch):
    monkeypatch.setattr(app_module, "get_db_connection", lambda: FakeConnection())
    monkeypatch.setattr(app_module.mail, "send", lambda msg: None)
    resp = client.post(
        "/contact",
        data={"name": "Tester", "email": "t@example.com", "phoneno": "123", "textarea": "Hello"},
    )
    assert resp.status_code == 302
    assert resp.location.endswith("status=success")


def test_job_post_missing_fields_redirects_empty(client):
    resp = client.post("/submit_job", data={"name": "", "email": "", "phone": "", "job_position": ""})
    assert resp.status_code == 302
    assert resp.location.endswith("status=empty")


def test_job_post_db_unavailable_redirects_db_error(client, monkeypatch):
    monkeypatch.setattr(app_module, "get_db_connection", lambda: None)
    resp = client.post(
        "/submit_job",
        data={"name": "Tester", "email": "t@example.com", "phone": "123", "job_position": "Engineer"},
    )
    assert resp.status_code == 302
    assert resp.location.endswith("status=db_error")


def test_job_post_success(client, monkeypatch):
    monkeypatch.setattr(app_module, "get_db_connection", lambda: FakeConnection())
    monkeypatch.setattr(app_module.mail, "send", lambda msg: None)
    resp = client.post(
        "/submit_job",
        data={"name": "Tester", "email": "t@example.com", "phone": "123", "job_position": "Engineer"},
    )
    assert resp.status_code == 302
    assert resp.location.endswith("status=success")


