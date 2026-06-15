FROM python:3.12-slim

# 1. ETAPA ROOT (Obrigatória)
# Instala pacotes do sistema e cria o usuário appuser logo de início
RUN apt-get update && apt-get install -y \
   libxcb1 \
   libgl1 \
   libglib2.0-0 \
   && rm -rf /var/lib/apt/lists/* \
   && useradd -m appuser

# Define o diretório de trabalho
WORKDIR /app

# Altera a propriedade da pasta /app para o appuser antes de mudar de usuário
RUN chown appuser:appuser /app

# 2. TRANSIÇÃO PARA USUÁRIO COMUM
# A partir daqui, absolutamente tudo roda com privilégios limitados
USER appuser

# Cria e ativa um Virtual Environment para isolar as permissões do PIP
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Copia o requirements garantindo que o dono seja o appuser
COPY --chown=appuser:appuser requirements.txt .

# Instala as dependências Python (rodando 100% como appuser)
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código do projeto garantindo a propriedade correta
COPY --chown=appuser:appuser . .

EXPOSE 8000

# O Healthcheck também rodará como appuser
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
