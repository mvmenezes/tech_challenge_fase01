from flask import jsonify, Blueprint, request
from utils.jwt_utils import generate_token, token_mandatory, get_user_from_token
from services.etlservice import get_all_books, get_all_categories, get_book_by_upc, get_book_by_search, get_book_overview
from services.etlservice import get_category_overview,get_top_rated_books, get_training_data, get_book_by_min_and_max, get_all_books_from_scraping, get_all_categories_from_scraping
import json
import pandas as pd
import logging, time
api = Blueprint("api", __name__)



logger = logging.getLogger(__name__)
TEST_USERNAME = "marcus"
TEST_PASSWORD = "123456"

@api.route("/auth/login", methods = ["POST"])
def login():
    """
    Efetuar o login na Aplicacao.
    ---
    parameters:
      - name: username
        type: string
        required: true
        description: Username para realizar login
      - name: password
        type: string
        required: true
        description: Password para realizar login
    responses:
      200:
        description: Retorna o token do usuario caso usuario e senha estejam corretos
        examples:
          application/json: {"token": "TOKEN_GERADO_PELA_APLICACAO"}
      401:
        description: Retorna mensagem de erro informacndo que usuario ou senha náo estáo corretos]
        examples:
          application/json: {"error": "Credenciais invalidas"}
    """
    begin = time.time()
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")
    if TEST_USERNAME == username and TEST_PASSWORD == password:
        token = generate_token(username)
        logger.info(f"Usuario {username} realizou login com sucesso.")
        logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
        return jsonify({"token": token})
    else:
        logger.info(f"Credenciais invalidas para o usuario {username}.")
        logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
        return jsonify({"error": "Credenciais invalidas."}), 401


@api.route("/auth/refresh", methods = ["POST"])
@token_mandatory
def refresh():
    """
    Efetuar o refresh do token
    ---
    parameters:
    responses:
      200:
        description: Retorna o token do usuario
        examples:
          application/json: {"token": "TOKEN_GERADO_PELA_APLICACAO"}
      401:
        description: Retorna mensagem de erro informacndo que usu[ario ou senha náo estáo corretos]
        examples:
          application/json: {"error": "Credenciais invalidas"}
    """
    begin = time.time()
    token = generate_token(get_user_from_token())
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify({"token": token})
    
@api.route("/books", methods=["GET"])
@token_mandatory
def books():
    """
    Lista todos os livros disponíveis na base de dados.
    ---
    responses:
      200:
        description: Retorna lista de livros.
      404:
        description: Retorna 404 caso nao tenha livros ou a trigger inicial nao foi executafa
        examples:
          application/json: {"mensagem": "Livros nao encontrados"}
    """
    begin = time.time()
    logger.debug(f"Requisicao recebida em /books:")
    books_df = get_all_books()
    json_obj = books_df.to_json(orient='records', force_ascii=False)
    if books_df.empty:
      logger.info("Livros nao Encontrados")
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify({"mensagem": "Livros nao encontrados"}), 404
    logger.info("Livros retornados")
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(json.loads(json_obj))


@api.route("/books/<id>", methods=["GET"])
@token_mandatory
def books_by_id(id):
    """
    Busca livros pelo ID.
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: O id do livro para busca
    responses:
        200:
            description: Retorna apenas um livro com o ID especificado
        404:
            description: Retorna mensagem informando que o livro nao foi encontrado
            examples:
                application/json: {"mensagem": "Livro nao Encontrado"}

    """
    begin = time.time()
    books_df: pd.DataFrame = get_book_by_upc(id)
    if books_df.empty:
      logger.info("Livros náo encontrados")
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify({"mensagem": "Livro nao Encontrado, talvez seja necessario requisitar o Web Srapping em /api/v1/scraping/trigger"}), 404
    else:
      logger.info("Livros retornados")
      json_obj = books_df.to_json(orient='records', force_ascii=False)
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify(json.loads(json_obj))

@api.route("/books/search", methods=["GET"])
@token_mandatory
def books_by_search():
    """
    Busca livros por título e/ou categoria.
    ---
    parameters:
      - name: title
        in: path
        type: string
        required: false
        description: titulo do livro para busca
      - name: category
        in: path
        type: string
        required: false
        description: categoria do livro para busca
    responses:
      200:
        description: Retorna apenas um livro com o ID especificado
        examples:
          application/json: {"message": "Livro nao Encontrado"}
      404:
            description: Retorna mensagem informando que o livro nao foi encontrado
            examples:
                application/json: {"mensagem": "Livro nao Encontrado"}
    """
    begin = time.time()
    title: str = request.args.get("title") or ""
    category: str = request.args.get("category") or ""

    if len(title) == 0 and len(category) == 0:
      logger.info("Parametros nao informados")
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify({"mensagem": "Livro nao Encontrado, talvez seja necessario requisitar o Web Srapping em /api/v1/scraping/trigger"}), 404
         
    books_df: pd.DataFrame = get_book_by_search(title, category)
    if books_df.empty:
      logger.info("Livros nao encontrados")
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify({"mensagem": "Livro nao Encontrado, talvez seja necessario requisitar o Web Srapping em /api/v1/scraping/trigger"}), 404
    else:
      json_obj = books_df.to_json(orient='records', force_ascii=False)
      logger.info("Livros retornados")
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify(json.loads(json_obj))


@api.route("/categories", methods=["GET"])
@token_mandatory
def categories():
    """
    Busca categorias dos livros.
    ---
    responses:
        200:
            description: Retorna todas as categorias de livros
            examples:
                [
                    {
                        "link": "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
                        "title": "Travel"
                    }
                ]
        404:
            description: Retorna mensagem informando que a categoria nao foi encontrada
            examples:
                application/json: {"mensagem": "Categoria nao Encontrada"}

    """
    begin = time.time()
    cat_df = get_all_categories()
    if cat_df.empty:
      logger.info("Categorias nao encontradas")
      logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
      return jsonify({"mensagem": "Categorias náo encontrado, talvez seja necessario requisitar o Web Srapping em /api/v1/scraping/trigger"}), 404
    json_obj = cat_df.to_json(orient='records', force_ascii=False)
    logger.info("Categorias retornadas")
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(json.loads(json_obj))

@api.route("/health", methods=["GET"])
@token_mandatory
def health():
    """
    Checa a saude da aplicacao
    ---
    responses:
        200:
            description: Retorna 200 (OK).
            examples:
                application/json: {'status': 'ok'}

    """
    begin = time.time()
    logger.info("Healthcheck OK")
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify({'status': 'ok'}), 200

@api.route("/stats/overview", methods=["GET"])
@token_mandatory
def overview():
    """
    Estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings
    ---
    responses:
        200:
            description: Retorna as Estatísticas gerais da coleção (total de livros, preço médio, distribuição de ratings.
            examples:
                application/json: {'status': 'ok'}

    """
    begin = time.time()
    logger.info("Books Overview Requisitado")
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(get_book_overview())

@api.route("/stats/categories", methods=["GET"])
@token_mandatory
def stats_categories():
    """
    Estatísticas detalhadas por categoria (quantidade de livros, preços por categoria)
    ---
    responses:
        200:
            description: Retorna as Estatísticas detalhadas por categoria (quantidade de livros, preços por categoria)
            examples:
                application/json: {'status': 'ok'}

    """
    begin = time.time()
    logger.info("Overview de Categorias requisitado")
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(get_category_overview())

@api.route("/top-rated", methods=["GET"])
@token_mandatory
def top_rated():
    """
    Lista os livros com melhor avaliação rating mais alto
    ---
    responses:
        200:
            description: Retorna Lista dos livros com melhor avaliação (rating mais alto)
            examples:
                application/json: {'status': 'ok'}

    """
    begin = time.time()
    books_df = get_top_rated_books()
    logger.info("Top Rated Books requisitado")
    obj_json = books_df.to_json(orient="records", force_ascii=False)
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(json.loads(obj_json))


@api.route("/books/price-range", methods=["GET"])
@token_mandatory
def price_range():
    """
   Filtra livros dentro de uma faixa de preço específica.
    ---
    parameters:
      - name: max
        in: path
        type: float
        required: true
        description: Valor máximo em real
      - name: min
        in: path
        type: float
        required: true
        description: valor m[inimo em real]
    responses:
      200:
        description: Retorna todos os livros dentro da faixa de preço escolhida.
        examples:
      404:
            description: Retorna mensagem informando que o livro nao foi encontrado
            examples:
                application/json: {"mensagem": "Livro nao Encontrado"}
    """
    begin = time.time()
    try:
        min = float (request.args.get("min")) or 0.0
        max = float (request.args.get("max")) or 0.0

            
        logger.info("Requisitado livros por valor")
        books_df: pd.DataFrame = get_book_by_min_and_max(min, max)
        if books_df.empty:
          logger.info("Livros nao encontrados")
          logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
          return jsonify({"mensagem": "Livro nao Encontrado, talvez seja necessario requisitar o Web Srapping em /api/v1/scraping/trigger"}), 404
        else:
          logger.info("Livros retornados")
          json_obj = books_df.to_json(orient='records', force_ascii=False)
          logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
          return jsonify(json.loads(json_obj))
    except ValueError:
        logger.info("Valores incompativeis")
        logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
        return jsonify({"error":"Valores incompativeis"})


@api.route("/scraping/trigger", methods=["GET"])
@token_mandatory
def trigger():
    """
    Checa a saude da aplicacao
    ---
    responses:
        200:
            description: Retorna 200 (OK).
            examples:
                application/json: {'status': 'ok'}
        500:
            description: Em caso de erro, retorna mensagem informando falha
            examples:
                application/json: {"Livros": "Livro nao Encontrado"}

    """
    begin = time.time()
    logger.info("Requisitado raspagem de Website")
    to_be_returned = []
    books_df = get_all_books_from_scraping()
    status = 200
    if books_df.empty:
      logger.info("Livros nao encontrados")
      to_be_returned.append({"Livros":"Livros nao Encontrados"})
      status = 500
    else:
      logger.info("Livros carregados com sucesso")
      to_be_returned.append({"Livros":"Livros Carregados com sucesso"})
       
    categories_df = get_all_categories_from_scraping()
    if categories_df.empty:
       logger.info("Categorias nao encontradas")
       to_be_returned.append({"Categorias":"Categorias nao Encontradas"})
       status = 500
    else:
       logger.info("Categorias carregadas com sucesso")
       to_be_returned.append({"Categorias":"Categorias Carregadas com sucesso"})
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(to_be_returned), status

@api.route("/ml/features", methods=["GET"])
@token_mandatory
def features():
    """
    Retorna as features do modelo
    ---
    responses:
        200:
            description: Retorna Lista dos livros com melhor avaliação (rating mais alto)
            examples:
                application/json: {'status': 'ok'}

    """
    begin = time.time()
    list_features = []
    book_feature = {}
    category_feature = {}
    book_feature["Book"] = [{"name": "id", "type": "str"},
    {"name": "title", "type": "str"},
    {"name": "description", "type": "str"},
    {"name": "price_with_tax", "type": "float"},
    {"name": "price_no_tax", "type": "float"},
    {"name": "tax", "type": "float"},
    {"name": "availability", "type": "int"},
    {"name": "reviews", "type": "int"},
    {"name": "rating", "type": "int"},
    {"name": "link", "type": "str"},
    {"name": "category", "type": "str"},
    {"name": "image", "type": "str"}]
    category_feature["Category"] = [{"name": "title", "type": "str"}, {"name": "link", "type": "str"}]
    list_features.append(book_feature)
    list_features.append(category_feature)
    logger.info("Features retornadas")
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    
    return jsonify(list_features)


@api.route("/ml/training-data", methods=["GET"])
@token_mandatory
def training_data():
    """
    Retorna 60% dos dados para treinamento (Separados de forma esquematica)
    ---
    responses:
        200:
            description: Retorna 60% da Lista dos livros
            examples:
                application/json: {'status': 'ok'}

    """
    begin = time.time()
    logger.info("Dados de Treinamento requisitados")
    training_df = get_training_data()
    logger.info("Dados de Treinamento retornados")
    json_obj = training_df.to_json(orient="records", force_ascii=False)
    logger.info(f"Perfomance: Metodo finalizado em {round((time.time()-begin)*1000)}ms")
    return jsonify(json.loads(json_obj))