# 🚀 API de Filtro de IPs da Rede TOR (Protegida por JWT)

Este projeto é uma API simples construída com FastAPI que gerencia e filtra endereços IP da rede TOR, utilizando **JSON Web Tokens (JWT)** para autenticação e proteção de rotas.

A API busca a lista atual de IPs de saída do TOR, permite ao usuário adicionar IPs específicos a uma lista de exclusão (persistida em um banco de dados) e, por fim, oferece um endpoint que retorna a lista de IPs do TOR *exceto* aqueles que foram excluídos.

## 🌟 Funcionalidades

* **Autenticação JWT:** Implementação completa de registro (`signup`) e login para proteger os endpoints principais.
* **Listar IPs do TOR [🔒]:** Busca e retorna a lista completa de IPs de saída da rede TOR (requer autenticação).
* **Excluir IP [🔒]:** Adiciona um IP a uma "lista de exclusão" no banco de dados (requer autenticação).
* **Listar IPs Filtrados [🔒]:** Retorna a lista de IPs do TOR subtraindo os IPs da lista de exclusão (requer autenticação).
* **Documentação Automática:** Fornece documentação interativa (Swagger UI e ReDoc) automaticamente.

## 🛠️ Endpoints da API

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `POST` | `/user/signup` | **Registra** um novo usuário no sistema. |
| `POST` | `/user/login` | **Autentica** o usuário e retorna o **Token JWT**. |
| `GET` | `/tor-ips` | **[🔒] Requer JWT.** Retorna a lista completa de IPs de saída do TOR (ou do cache). |
| `POST` | `/exclude-ip` | **[🔒] Requer JWT.** Adiciona um IP à lista de exclusão do banco de dados. |
| `GET` | `/filtered-tor-ips` | **[🔒] Requer JWT.** Retorna os IPs do TOR subtraindo a lista de exclusão. |
| `GET` | `/docs` | Acesso à documentação interativa (Swagger UI). |
| `GET` | `/redoc` | Acesso à documentação (ReDoc). |

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
    ```

3.  **Instale as dependências:**
    (Assumindo que você tem um `requirements.txt` com `fastapi`, `uvicorn`, `sqlalchemy`, `pyjwt`, `passlib`, etc.)
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor:**
    O comando `uvicorn` irá iniciar o servidor. O `main.py` está dentro da pasta `app/`, então usamos `app.main:app`.
    ```bash
    uvicorn app.main:app --port 8080
    ```

5.  **Acesse a API:**
    * **Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    * **Teste a autenticação:** Use `/user/signup` para criar um usuário e `/user/login` para obter o Token JWT.

---

### 2. Execução com Docker

Este método é ideal para simular um ambiente de produção ou para garantir que a aplicação rode de forma isolada e consistente.

**Pré-requisitos:**
* Docker

**Passos:**

1.  **Construa a imagem Docker:**
    No diretório raiz do projeto (onde está o `Dockerfile`), execute:
    ```bash
    # "tor-filter-api" é um nome sugerido para a imagem.
    docker build -t tor-filter-api .
    ```

2.  **Execute o contêiner:**
    Isso irá iniciar um contêiner a partir da imagem que acabamos de construir.
    ```bash
    # Mapeia a porta 8080 da sua máquina para a porta 8000 do contêiner (porta padrão do Gunicorn/Uvicorn)
    docker run -d -p 8080:8000 --name tor-api tor-filter-api
    ```

3.  **Acesse a API:**
    * **Docs (Swagger):** [http://localhost:8080/docs](http://localhost:8080/docs)

---

## 📄 Implementação em AWS EC2

### 1. Provisionamento da Infraestrutura (Console AWS)

Esta fase consiste em lançar a máquina virtual e configurar a conectividade básica:

| Ação | Detalhe |
| :--- | :--- |
| **Lançamento da Instância** | **Serviço:** EC2 (Launch Instances).<br>**AMI:** Amazon Linux 2023 ou Ubuntu LTS.<br>**Tipo:** `t2.micro` (ou `t3.micro`).<br>**Key Pair:** Criação/Seleção da chave `.pem` (necessária para acesso SSH). |
| **Configuração de Rede** | **Security Group (SG):** Criar um novo SG (obrigatório pela AWS). |
| **Permissões de Entrada** | **Porta 22 (SSH):** Origem *My IP* (ou bloco de rede específico).<br>**Porta 8000 (API):** Protocolo TCP. Origem **`0.0.0.0/0`** (Acesso público para testes). |
| **Finalização** | Obter o **IP Público** da instância após o status mudar para `Running`. |

### 2. Configuração do Servidor e Docker (Acesso via SSH)

Nesta fase, o software necessário para rodar o contêiner é instalado na instância EC2.

#### 2.1 Acesso Remoto

Conectar à instância usando a chave `.pem`:

```bash
# Exemplo de conexão (ajuste o usuário conforme a AMI)
ssh -i /caminho/para/chave.pem ec2-user@<IP_PÚBLICO_EC2>