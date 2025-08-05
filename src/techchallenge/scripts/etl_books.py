from bs4 import BeautifulSoup
from src.techchallenge.app.models import Book
import requests
from dataclasses import asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

URL = "https://books.toscrape.com/"


def _initialize(url = URL):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_all_books():
    list_books = []
    number_of_processors = 10
    soup = _initialize()
    ### Preciso pegar a quantidade de paginas para conseguir interagir com as paginas estaticas de cada pagina
    number_of_pages = _get_number_of_pages(soup)

    ###A pagina comeca de 1 e precisa ir até o [ultimo n[umero]], por isso o +1
    for page_number in range(1, number_of_pages+1, number_of_processors):

        urls = [URL+f"catalogue/page-{str(page)}.html" for page in range(page_number, page_number + number_of_processors)]
        with ThreadPoolExecutor(max_workers=number_of_processors) as executor:
            runs = [executor.submit(_get_books_from_page, url) for url in urls]

            for processed in as_completed(runs):
                list_books.extend(processed.result())
    return list_books

def _get_number_of_pages(soup):
    text = soup.find("li", class_="current").text
    return int(text.split(" of ")[1])

def _get_books_from_page(url):
    list_books = []
    ### Com base na pagina, acessa direto a pagina
    soup = _initialize(url)

    ### Os livros estao separados pela tag article (Pega todos os livros da pagina {page_number})
    articles = soup.find_all("article")
    for  art in (articles):
        ### A intencao aqui é pegar o link de detalhes com todas as informacoes do livro.
        div_book = art.find("div",class_="image_container")
        link_details = div_book.find_next("a").get("href")
        book_link= URL+f"catalogue/{link_details}"
        list_books.append(_get_details_book(book_link))
    return list_books

def _get_details_book(link):
    ### Comeca a verificar o link de detalhes do livro
    soup_details = _initialize(link)

    ## Pega a categoria
    ul_category = soup_details.find("ul",class_="breadcrumb")
    category = ""
    for cat in ul_category.find_all("a"):
        if "/books/" in str(cat.get("href")):
            category = cat.text

    ## Pega a imagem
    div_image = soup_details.find("div", id= "product_gallery")
    image_link = URL + str(div_image.find("img").get("src"))[6:]

    ### Descricao do Produto
    div_desc = soup_details.find(id="product_description")
    description = ''
    if div_desc:
        description = div_desc.find_next("p").text
    id = soup_details.find("th", string="UPC").find_next("td").text
    availability = int(re.findall(r'\d+', str(soup_details.find("th", string="Availability").find_next("td").text))[0])
    price_no_tax = float(soup_details.find("th", string="Price (excl. tax)").find_next("td").text[2:])
    price_with_tax = float(soup_details.find("th", string="Price (incl. tax)").find_next("td").text[2:])
    reviews = int(soup_details.find("th", string="Number of reviews").find_next("td").text)
    tax = float(soup_details.find("th", string="Tax").find_next("td").text[2:])
    title = soup_details.title.string.replace("\n","").strip()
    rating = str(soup_details.find("p", class_="star-rating").get('class')).split(" ")[1].replace("']", "").replace("'", "")
    rating = int(rating.replace("One", "1").replace("Two", "2").replace("Three", "3").replace("Four", "4").replace("Five", "5"))
    book = Book(id, 
                 title, 
                 description, 
                 price_with_tax, 
                 price_no_tax, 
                 tax, 
                 availability, 
                 reviews, 
                 rating, 
                 link,
                 category,
                 image_link)
    return asdict(book)



