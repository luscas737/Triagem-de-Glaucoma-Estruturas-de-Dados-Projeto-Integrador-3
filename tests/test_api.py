from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_listar():
    r = client.get("/pacientes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_paciente_inexistente():
    r = client.get("/pacientes/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Paciente não encontrado"

def test_remover_heap():
    r = client.delete("/heap")
    assert r.status_code in [200, 404]
