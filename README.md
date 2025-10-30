# 🚀 API de Filtro de IPs da Rede TOR

Este projeto é uma API simples construída com FastAPI que gerencia e filtra endereços IP da rede TOR.

A API busca a lista atual de IPs de saída do TOR, permite ao usuário adicionar IPs específicos a uma lista de exclusão (que é persistida em um banco de dados) e, por fim, oferece um endpoint que retorna a lista de IPs do TOR *exceto* aqueles que foram excluídos.

## 🌟 Funcionalidades

* **Listar IPs do TOR:** Busca e retorna a lista completa de IPs de saída da rede TOR.
* **Excluir IP:** Adiciona um IP a uma "lista de exclusão" no banco de dados.
* **Listar IPs Filtrados:** Retorna a lista de IPs do TOR subtraindo os IPs da lista de exclusão.
* **Documentação Automática:** Fornece documentação interativa (Swagger UI e ReDoc) automaticamente.

## 🛠️ Endpoints da API

* `GET /tor-ips`: Retorna a lista completa de IPs de saída do TOR.
* `POST /exclude-ip`: Adiciona um IP à lista de exclusão.
* `GET /filtered-tor-ips`: Retorna a lista de IPs do TOR, exceto aqueles na lista de exclusão.
* `GET /docs`: Acesso à documentação interativa (Swagger UI).
* `GET /redoc`: Acesso à documentação (ReDoc).

---

## ⚙️ Como Executar

Você pode executar este projeto de duas maneiras: localmente usando um ambiente virtual (`venv`) ou via Docker.

### 1. Execução Local (com `venv`)

Este método é ideal para desenvolvimento e testes rápidos.

**Pré-requisitos:**
* Python 3.9+
* Git (opcional, para clonar)

**Passos:**

1.  **Clone o repositório:**
    ```bash
    # Substitua pela URL do seu repositório
    git clone [https://github.com/seu-usuario/seu-projeto.git](https://github.com/seu-usuario/seu-projeto.git)
    cd seu-projeto
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Criar o venv
    python3 -m venv venv

    # Ativar no Linux/macOS
    source venv/bin/activate

    # Ativar no Windows (PowerShell)
    .\\venv\\Scripts\\Activate.ps1
    # Ou no Windows (CMD)
    .\\venv\\Scripts\\activate.bat
    ```

3.  **Instale as dependências:**
    (Assumindo que você tem um `requirements.txt` com `fastapi`, `uvicorn`, `sqlalchemy`, etc.)
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor:**
    O comando `uvicorn` irá iniciar o servidor. O `main.py` está dentro da pasta `app/`, então usamos `app.main:app`.
    ```bash
    uvicorn app.main:app --reload
    ```

5.  **Acesse a API:**
    * **Aplicação:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
    * **Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 2. Execução com Docker

Este método é ideal para simular um ambiente de produção ou para garantir que a aplicação rode de forma isolada e consistente.

**Pré-requisitos:**
* Docker

**Passos:**

1.  **Construa a imagem Docker:**
    No diretório raiz do projeto (onde está o `Dockerfile`), execute:
    ```bash
    # "tor-filter-api" é um nome sugerido para a imagem. O "." indica o contexto atual.
    docker build -t tor-filter-api .
    ```

2.  **Execute o contêiner:**
    Isso irá iniciar um contêiner a partir da imagem que acabamos de construir.
    ```bash
    # -d: Roda em modo "detached" (em segundo plano)
    # -p 8080:8080: Mapeia a porta 8080 da sua máquina para a porta 8080 do contêiner
    # --name tor-api: Dá um nome fácil ao contêiner
    docker run -d -p 8080:8080 --name tor-api tor-filter-api
    ```

3.  **Acesse a API:**
    Como o `Dockerfile` expõe a porta `8080`, a aplicação estará disponíveis em:
    * **Aplicação:** [http://localhost:8080](http://localhost:8080)
    * **Docs (Swagger):** [http://localhost:8080/docs](http://localhost:8080/docs)

---