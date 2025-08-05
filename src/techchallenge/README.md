
# Tech Challenge Scrap Book

## Descrição do Projeto

O **Tech Challenge Scrap Book** é uma aplicação desenvolvida para realizar **web scraping** no site [Books to Scrape](https://books.toscrape.com/), coletando informações de **livros** e **categorias**. Através de uma API RESTful, o usuário pode acessar diferentes endpoints para obter dados organizados sobre os livros disponíveis no site, filtrando por critérios como categoria, título e classificação.

---

## Arquitetura

A aplicação segue uma arquitetura **monolítica** e está organizada nos seguintes módulos:

```
📁 app       → Criação e configuração do Flask app  
📁 api       → Contém a definição das rotas da API  
📁 data      → Armazenamento dos arquivos CSV com os dados extraídos  
📁 scripts   → Scripts de ETL responsáveis por realizar o scraping  
📁 servicos  → Camada de serviço que conecta as rotas ao scraping e trata os dados
```

**Tecnologias utilizadas:**

- Python 3.12
- [Flask](https://flask.palletsprojects.com/)
- [Poetry](https://python-poetry.org/)
- [Flasgger](https://github.com/flasgger/flasgger) (para documentação Swagger)
- BeautifulSoup e requests (ETL)
- Armazenamento local em **CSV**

---

## Instruções de Instalação

> Pré-requisitos: Python 3.12 e Poetry instalado.

1. **Clone o repositório**
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Instale o Poetry**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Instale as dependências**
   ```bash
   poetry install
   ```

4. **Ative o ambiente virtual**
   ```bash
   poetry shell
   ```

5. **Execute o app (por exemplo, via Visual Studio Code ou com o comando abaixo):**
   ```bash
   python app/run.py
   ```

---

## Documentação das Rotas da API

A documentação Swagger estará disponível em:
`http://localhost:5000/apidocs/`


## Rotas Disponíveis

### Autenticação

- `POST /auth/login`  
  Realiza login na aplicação (usuário de teste: `marcus`, senha: `123456`).  
  **Request:**
  ```json
  {
    "username": "marcus",
    "password": "123456"
  }
  ```
  **Response:**
  ```json
  {
    "access_token": "..."
  }
  ```

---

### Livros

- `GET /livros`  
  Retorna todos os livros armazenados em cache local (CSV).

- `GET /livros/scraping`  
  Realiza o scraping ao vivo e retorna todos os livros atualizados.

- `GET /livros/<upc>`  
  Busca livro por código UPC.

- `GET /livros/search/<search>`  
  Busca livro pelo título ou parte do nome.

- `GET /livros/overview/<upc>`  
  Retorna um resumo detalhado de um livro específico.

- `GET /livros/minmax?min=<valor>&max=<valor>`  
  Filtra livros com base em um intervalo de preço.

- `GET /livros/top`  
  Retorna os livros com melhor avaliação.

---

### Categorias

- `GET /categorias`  
  Retorna todas as categorias armazenadas localmente.

- `GET /categorias/scraping`  
  Realiza scraping ao vivo das categorias.

- `GET /categorias/overview/<categoria>`  
  Retorna um resumo de todos os livros de uma categoria.

---

### Machine Learning

- `GET /training_data`  
  Retorna os dados formatados para treinamento de modelos de Machine Learning.

---

## Autenticação

- Todas as rotas (exceto `/auth/login`) requerem **token JWT**.
- Envie o token no header da requisição:

```
Authorization: Bearer <seu_token_aqui>
```

---

## 🧩 Dependências

- Flask
- Pandas
- JWT
- Flasgger (para Swagger Docs)

---

## Execução

O projeto pode ser executado diretamente no Visual Studio Code, após ativar o ambiente com `poetry shell`.

---

