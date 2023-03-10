"""Exporter functional tests."""
URL = "http://127.0.0.1:8675"


def test_software_inventory_exporter_endpoints(session):
    endpoints = ["docs", "hostname", "kernel", "dpkg", "snap"]
    for endpoint in endpoints:
        response = session.get(f"{URL}/{endpoint}")
        assert response.status_code == 200
        if endpoint not in ["docs", "hostname"]:
            content = response.json()
            assert len(content) > 0


def test_unknown_endpoint(session):
    response = session.get(f"{URL}/unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
