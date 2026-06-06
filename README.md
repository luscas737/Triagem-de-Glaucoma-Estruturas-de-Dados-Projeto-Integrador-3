# Triagem-de-Glaucoma-Estruturas-de-Dados-Projeto-Integrador-3
tutorial simples pra fazer rodar.
## clone
```
git clone https://github.com/tiagopessoalima/glaucoma-app.git
cd glaucoma-app
```

## windows 
```
python -m venv venv
venv\Scripts\activate
```
## linux
```
python -m venv venv
source venv/bin/activate
```

## dependencias
```
pip install -r requirements.txt
```

## iniciar servidor
```
uvicorn main:app --reload
```

## api fica disponivel em
```
http://localhost:8000
```