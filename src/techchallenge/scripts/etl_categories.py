from bs4 import BeautifulSoup
from app.models import Book, Category
import requests
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

URL = "https://books.toscrape.com/"


def _initialize(url = URL):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_all_categories():
    list_categories = []
    soup = _initialize()
    ### Com base na pagina, acessa direto a pagina
    soup = _initialize(URL)

    ### Os livros estao separados pela tag article (Pega todos os livros da pagina {page_number})
    li_categories = soup.find("div", class_="side_categories")
    links = li_categories.find_all("a")
    for  link in (links):
        ### A intencao aqui é pegar o link de detalhes com todas as informacoes do livro.
        title = link.text.strip()
        link = URL+link.get("href")
        if title == "Books":
            continue

        list_categories.append(asdict(Category(title=title, link=link)))
    return list_categories

  
                