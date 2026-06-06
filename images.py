from pathlib import Path
import pandas as pd
from predict_service import predict

CSV_PATH = "paciente.csv"
IMAGES_DIR = Path("Images")

def gerar_resultados():
    df = pd.read_csv(CSV_PATH)

    resultados = {}

    for _, row in df.iterrows():

        caminho_antigo = row["imagem"]

        if pd.notna(caminho_antigo) and str(caminho_antigo).strip():

            nome_arquivo = Path(caminho_antigo).name

            caminho_imagem = IMAGES_DIR / nome_arquivo

            if not caminho_imagem.exists():
                continue

            pred = predict(str(caminho_imagem))

            id_paciente = row["id_paciente"]

            resultados[id_paciente] = float(pred[0])

    return resultados