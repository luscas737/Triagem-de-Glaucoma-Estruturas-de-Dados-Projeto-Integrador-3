import requests

BASE_URL = "http://127.0.0.1:8000"


# 1. Health check
def test_health():
    r = requests.get(f"{BASE_URL}/health")
    assert r.status_code == 200


# 2. Criar paciente
def test_create_paciente():
    with open("Images/image_4.jpg", "rb") as img:
        files = {
            "imagem": ("image_4.jpg", img, "image/jpeg")
        }

        data = {
            "id": 1
        }

        r = requests.post(
            f"{BASE_URL}/pacientes",
            data=data,
            files=files
        )

    assert r.status_code in [200, 201]

    resposta = r.json()
    assert "id" in resposta
    assert "score" in resposta


# 3. Listar pacientes
def test_listar():
    r = requests.get(f"{BASE_URL}/pacientes")

    assert r.status_code == 200
    assert isinstance(r.json(), list)


# 4. Buscar paciente 
def test_buscar_paciente():
    r = requests.get(f"{BASE_URL}/pacientes/999999")

    assert r.status_code in [200, 404]


# 5.Buscar paciente inexistentepytest -v
def test_paciente_inexistente():
    r = requests.get(f"{BASE_URL}/pacientes/999999")

    assert r.status_code == 404
    assert r.json()["detail"] == "Paciente não encontrado"


# 6. Remover da heap
def test_remover_heap():
    r = requests.delete(f"{BASE_URL}/heap")

    assert r.status_code in [200, 404]