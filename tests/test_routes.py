"""Smoke tests: every public GET route renders successfully."""

import pytest

ROUTES_AND_MARKERS = [
    ("/", "KVVSH Group of Companies Pvt Ltd"),
    ("/about", "ABOUT"),
    ("/business", "Business Divisions"),
    ("/leadership", "Leadership"),
    ("/career", "Career"),
    ("/jobs", "Job"),
    ("/news", "News"),
    ("/sustainability", "Sustainability"),
    ("/global-presence", "Global Presence"),
    ("/legal", "Legal"),
    ("/privacy-policy", "Privacy"),
    ("/terms-and-conditions", "Terms"),
    ("/contact", "Contact"),
]

GROUP_MARKERS = {
    "/group1": "Galaxxy TV",
    "/group2": "Galaxxy Grocery",
    "/group3": "Galaxxy Special Schools",
    "/group4": "OCEAN Mobiles",
    "/group5": "Galaxxy Constructions",
    "/group6": "Galaxxy Motors Manufacturing",
    "/group7": "Galaxxy EV",
    "/group8": "Galaxxy AirX",
    "/group9": "GOF Refineries",
    "/group10": "Galaxxy XPay",
}

NAVBAR_MARKERS = [
    "About Us",
    "Businesses",
    "Leadership",
    "Global Presence",
    "Career",
    "Contact",
]


def test_test_route(client):
    resp = client.get("/test")
    assert resp.status_code == 200
    assert b"Flask Working" in resp.data


@pytest.mark.parametrize("path,marker", ROUTES_AND_MARKERS)
def test_main_routes(client, path, marker):
    resp = client.get(path)
    assert resp.status_code == 200
    assert marker.encode() in resp.data


@pytest.mark.parametrize("path,marker", GROUP_MARKERS.items())
def test_group_routes(client, path, marker):
    resp = client.get(path)
    assert resp.status_code == 200
    assert marker.encode() in resp.data


@pytest.mark.parametrize("path", list(GROUP_MARKERS.keys()) + ["/about", "/business"])
def test_navbar_present_on_pages(client, path):
    resp = client.get(path)
    body = resp.get_data(as_text=True)
    for marker in NAVBAR_MARKERS:
        assert marker in body


def test_image_route(client):
    resp = client.get("/image/kvvsh-icon.webp")
    assert resp.status_code == 200


def test_missing_image_returns_404(client):
    resp = client.get("/image/does-not-exist.webp")
    assert resp.status_code == 404
