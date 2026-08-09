"""Error page tests: 404 and 500 handlers render properly."""

from werkzeug.exceptions import InternalServerError


def test_404_page(client):
    resp = client.get("/this-route-does-not-exist")
    assert resp.status_code == 404
    assert b"404" in resp.data or b"Page" in resp.data


def test_500_handler_renders(client):
    spec = client.application.error_handler_spec[None][500]
    handler = spec[InternalServerError]
    result = handler(InternalServerError())
    if isinstance(result, tuple):
        response, status = result
        assert status == 500
    else:
        response = result
        assert getattr(response, "status_code", None) == 500
    body = response.get_data(as_text=True) if hasattr(response, "get_data") else response
    body = body.lower()
    assert "500" in body or "error" in body
