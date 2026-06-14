from fastapi import FastAPI
from fastapi import HTTPException
from estrutura_abb import *
from estrutura_avl import *
from estrutura_heap import *
from metrics import gerar_metricas
from images import gerar_resultados
from predict_service import predict
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile, File, Form
import os

app = FastAPI()
BST = ArvoreBinariaBusca()
AVL = ArvoreAVL()
HEAP = FilaPrioridade()
pacientes = {}
@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/pacientes")
async def criar_paciente(
    id: int = Form(...),
    imagem: UploadFile = File(...)
):

    if not imagem.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Arquivo enviado não é uma imagem"
        )

    os.makedirs("Images", exist_ok=True)

    caminho_imagem = f"Images/{imagem.filename}"

    with open(caminho_imagem, "wb") as buffer:
        buffer.write(await imagem.read())

    try:
        score = float(predict(caminho_imagem)[0])

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Erro ao processar imagem"
        )

    BST.inserir(id, score)
    AVL.inserir(id, score)

    paciente_heap = Paciente(id, score)
    HEAP.inserir(paciente_heap)

    pacientes[id] = {
        "id": id,
        "imagem": caminho_imagem,
        "score": score
    }

    return {
        "mensagem": "Paciente cadastrado",
        "id": id,
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
@app.get("/pacientes")
def listar_pacientes():
    return list(pacientes.values())

app.mount(
    "/graficos",
    StaticFiles(directory="graficos"),
    name="graficos"
)
app.mount("/", StaticFiles(directory="front-end", html=True), name="frontend")