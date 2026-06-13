from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# 1. Health check
def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

# 2. Listar pacientes
def test_listar():
    r = client.get("/pacientes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

# 3. Buscar paciente inexistente
def test_paciente_inexistente():
    r = client.get("/pacientes/999999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Paciente não encontrado"

# 4. Remover da heap
def test_remover_heap():
    r = client.delete("/heap")
    assert r.status_code in [200, 404]
