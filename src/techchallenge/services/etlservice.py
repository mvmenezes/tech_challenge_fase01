import pandas as pd
from scripts.etl_books import get_all_books as get_all_books_etl
from scripts.etl_categories import get_all_categories as get_all_categories_etl
import numpy as np
import os
from sklearn.model_selection import train_test_split
import math
import random
import logging



logger = logging.getLogger(__name__)
def get_all_books_from_scraping():
    books = get_all_books_etl()
    books_df = pd.DataFrame(books)
    logger.info("Salvando Livros no CSV")
    _save_to_csv(books_df, name="books.csv")
    logger.info("Livros salvos no CSV")
    return books_df

def get_all_books():
    logger.info("Recuperando todos os livros do CSV")
    books_df = _get_from_csv("books.csv")
    logger.info("Livros recuperados do CSV")
    return books_df

    

def get_book_by_upc(upc):
    logger.info("Recuperando livro com UPC: "+upc)
    books_df = get_all_books()
    if books_df.empty:
        return books_df
    return books_df.loc[ books_df["id"] == upc]

def get_book_by_search(title, category):
    logger.info(f"Recuperando livro por titulo: {title} e categoria {category}")
    books_df = get_all_books()
    if books_df.empty:
        return books_df
    return books_df.loc[ (books_df["category"] == category) | (books_df["title"] == title)]

def get_all_categories_from_scraping():
    logger.info("Recuperando todas as categorias por scraping")
    cat = get_all_categories_etl()
    cat_df = pd.DataFrame(cat)
    logger.info("Categorias recuperadas")
    logger.info("Salvando categorias na base de dados")
    _save_to_csv(cat_df, name="categories.csv")
    logger.info("Categorias salvas na base de dados")
    return cat_df
    
def get_all_categories():
    logger.info("Recuperando todas as categorias do CSV")
    cat_df = _get_from_csv("categories.csv")
    logger.info("Recuperada categorias do CSV")
    return cat_df

def get_book_overview():
    books_df = get_all_books()
    if books_df.empty:
        return {}
    overview = {}
    overview["Total de Livros"] = books_df.shape[0]
    overview["Preço Medio"] = round(np.mean(books_df["price_with_tax"]),2)
    overview["Distribuicao de Ratings"] = books_df["rating"].value_counts().sort_index().to_dict()
    logger.info("Overview dos livros retornado")
    return overview

def get_category_overview():
    cat_df = get_all_categories()
    books_df = get_all_books()
    if cat_df.empty:
        return {}
    if books_df.empty:
        return {}
    qtd = 0
    list_overview = []
    for index, reg in cat_df.iterrows():
        list_overview.append({"Categoria": reg["title"], 
                              "Quantidade de Livros": books_df.loc[books_df["category"] == reg["title"]].shape[0],
                              "Preço Medio da Categoria": round(np.mean(books_df.loc[books_df["category"] == reg["title"]]["price_with_tax"]),2)
                              })
    logger.info("Overview das categorias retornado")
    return list_overview
    
def get_top_rated_books():
    books_df = get_all_books()
    if books_df.empty:
        return books_df

    return books_df.sort_values("rating",ascending=False).head(100)

def get_book_by_min_and_max(min, max):
    books_df = get_all_books()
    if books_df.empty:
        return books_df
    return books_df.loc[ (books_df["price_with_tax"] >= min) & (books_df["price_with_tax"] <= max)]


def get_training_data():
    books_df = get_all_books()
    if books_df.empty:
        return books_df
    population = books_df.shape[0]
    amostra = math.ceil(0.5 * population)
    k = math.ceil(population / amostra)
    start = random.randint(0,k)
    list_items = [x for x in range(start,population, k)]
    return books_df.iloc[list_items,:]
    
    


def _save_to_csv(df: pd.DataFrame, name="books.csv"):
    full_path = os.path.join(os.getcwd(),"src","techchallenge","data","input",name)
    df.to_csv(full_path, index=False, sep=";")

def _get_from_csv(name="books.csv"):
    full_path = os.path.join(os.getcwd(),"src","techchallenge","data","input",name)
    if os.path.exists(full_path):
        return pd.read_csv(full_path, sep=";")
    else:
        return pd.DataFrame()
    

