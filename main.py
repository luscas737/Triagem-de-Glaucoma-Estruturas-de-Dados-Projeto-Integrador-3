from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from estrutura_abb import *
from estrutura_avl import *
from estrutura_heap import *
from metrics import gerar_metricas
from images import gerar_resultados
app = FastAPI()
BST = ArvoreBinariaBusca()
AVL = ArvoreAVL()
HEAP = FilaPrioridade()
pacientes = {}
@app.get("/health")
def health():
    return {"status": "ok"}

class PacienteRequest(BaseModel):
    id: int
    imagem: str

@app.post("/pacientes")
def criar_paciente(dados: PacienteRequest):
    score = float(predict(dados.imagem)[0])
    BST.inserir(dados.id, score)
    AVL.inserir(dados.id, score)
    paciente_heap = Paciente(dados.id, score)
    HEAP.inserir(paciente_heap)
    pacientes[dados.id] = {
    "id": dados.id,
    "imagem": dados.imagem,
    "score": score
    }
    return {
    "mensagem": "Paciente cadastrado",
    "id": dados.id,
    "score": score
    }

@app.get("/ranking")
def ranking():

    return [
        {
            "id": entrada[3].id,
            "score": entrada[3].risco
        }
        for entrada in sorted(HEAP.heap)
    ]

@app.get("/pacientes/{id}")
def buscar_paciente(id: int):

    if id not in pacientes:
        raise HTTPException(
            status_code=404,
            detail="Paciente não encontrado"
        )

    return pacientes[id]

@app.delete("/heap")
def remover_paciente():

    paciente_removido = HEAP.remover()

    if paciente_removido is None:
        raise HTTPException(
            status_code=404,
            detail="Heap vazia"
        )
    pacientes.pop(paciente_removido.id, None)
    return {
        "mensagem": "Paciente removido da heap",
        "id": paciente_removido.id,
        "score": paciente_removido.risco
    }

@app.post("/metricas")
def metricas():
    return gerar_metricas()

