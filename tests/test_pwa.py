from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_manifest_endpoint():
    response = client.get("/manifest.json")
    assert response.status_code == 200
    assert "application/manifest+json" in response.headers["content-type"]
    data = response.json()
    assert "HEMIS" in data["name"]
    assert data["display"] == "standalone"
    assert len(data["icons"]) >= 2

def test_service_worker_endpoint():
    response = client.get("/sw.js")
    assert response.status_code == 200
    assert "application/javascript" in response.headers["content-type"]
    assert response.headers.get("Service-Worker-Allowed") == "/"
    assert "addEventListener" in response.text

def test_pwa_icons_accessible():
    resp192 = client.get("/static/images/icons/icon-192.png")
    assert resp192.status_code == 200
    assert "image/png" in resp192.headers["content-type"]

    resp512 = client.get("/static/images/icons/icon-512.png")
    assert resp512.status_code == 200
    assert "image/png" in resp512.headers["content-type"]
