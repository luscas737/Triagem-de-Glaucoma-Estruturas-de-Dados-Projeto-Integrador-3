# Triagem-de-Glaucoma-Estruturas-de-Dados-Projeto-Integrador-3
tutorial simples pra fazer rodar.
## clone
```
git clone https://github.com/luscas737/Triagem-de-Glaucoma-Estruturas-de-Dados-Projeto-Integrador-3.git
cd Triagem-de-Glaucoma-Estruturas-de-Dados-Projeto-Integrador-3
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

## abrir no navegador
```
http://127.0.0.1:8000/Dashboard.html

```
### Pré-requisitos Para Executar a Aplicação Localmente com Docker:

- Docker Desktop instalado no Windows ou Linux;

Executar:

## Inciar o Serviço do Docker (Linux)

```bash
sudo systemctl start docker
```

## Baixar a Imagem Docker na Máquina (Bash/Powershell/CMD)
```bash
docker pull jadilsonsa/glaucoma-app:latest
```

## Iniciar o Container da API
```bash
docker run -p 8000:8000 jadilsonsa/glaucoma-app:latest
```

## Para Acessar a API:
```
http://localhost:8000/Dashboard.html
```

## Testes Automatizados

Os testes automatizados foram desenvolvidos utilizando Pytest e FastAPI TestClient para validar o funcionamento dos principais endpoints da API.

### Executar os testes

Com o ambiente virtual ativado e as dependências instaladas, execute:

```bash
pytest -v
```

### Arquivo de testes

```text
tests/test_api.py
```

### Funcionalidades testadas

- Health Check (`/health`)
- Listagem de pacientes (`/pacientes`)
- Busca de paciente inexistente (`/pacientes/{id}`)
- Remoção da Heap (`/heap`)
  

## Pipeline CI/CD

O projeto utiliza um pipeline de Integração e Entrega Contínua (CI/CD) implementado com GitHub Actions para automatizar testes, validação e publicação da aplicação. O pipeline é executado automaticamente a cada *push* ou *pull request* realizado no repositório.
A primeira etapa é a Integração Contínua (CI), responsável por preparar o ambiente de execução, instalar todas as dependências necessárias e executar os testes automatizados da aplicação. Ao final dessa etapa, é gerado e publicado um relatório contendo os resultados dos testes, permitindo verificar rapidamente se o sistema continua funcionando corretamente após cada alteração realizada no código. Após a conclusão bem-sucedida dos testes, é executada a etapa de Build, na qual é realizada a construção da imagem Docker da aplicação e por fim, a etapa de Entrega Contínua (CD) é executada apenas quando ocorre um push na branch principal (main). Nessa fase, a imagem Docker gerada é publicada automaticamente no Docker Hub utilizando credenciais armazenadas de forma segura nos GitHub Secrets (`DOCKERHUB_USERNAME` e `DOCKERHUB_TOKEN`). Dessa forma, a versão mais recente da aplicação fica disponível para implantação e distribuição de maneira automatizada.
Esse processo garante maior confiabilidade ao desenvolvimento, pois cada alteração realizada passa por testes, validação da imagem Docker e publicação automatizada, reduzindo a possibilidade de erros e facilitando a manutenção e evolução do sistema.

