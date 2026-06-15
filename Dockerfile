# ===== STAGE 1 =====
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ===== STAGE 2 =====
FROM python:3.12-slim

# 1. Preparação do sistema (Ainda como ROOT)
RUN apt-get update && apt-get install -y \
    libxcb1 \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

WORKDIR /app

# Copia as dependências da aplicação para o diretório global (Ainda como ROOT)
COPY --from=builder /install /usr/local

# Ajusta as permissões da pasta de trabalho antes de mudar de usuário
RUN chown appuser:appuser /app

# 2. Transição para o Usuário Comum (O mais cedo possível para a aplicação)
USER appuser

# Agora esta cópia é processada sob o contexto do appuser
COPY --chown=appuser:appuser . .

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
 CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
