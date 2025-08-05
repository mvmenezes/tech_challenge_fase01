from dataclasses import dataclass


@dataclass
class Book:
    id: str
    title: str
    description: str
    price_with_tax: float
    price_no_tax: float
    tax: float
    availability: int
    reviews: int
    rating: int
    link: str
    category: str
    image: str

@dataclass
class Category:
    title: str
    link: str