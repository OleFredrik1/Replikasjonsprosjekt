
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Preview:
    first_name: str
    surname: str

    @staticmethod
    def from_dict(obj: dict) -> 'Preview':
        _first_name = str(obj.get("first_name"))
        _surname = str(obj.get("surname"))
        return Preview(_first_name, _surname)

@dataclass
class Name:
    en: str

    @staticmethod
    def from_dict(obj: dict) -> 'Name':
        _en = str(obj.get("en"))
        return Name(_en)

@dataclass
class Category:
    code: str
    name: Name

    @staticmethod
    def from_dict(obj: dict) -> 'Category':
        _code = str(obj.get("code"))
        _name = Name.from_dict(obj.get("name"))
        return Category(_code, _name)

@dataclass
class Channel:
    title: str

    @staticmethod
    def from_dict(obj: dict) -> 'Channel':
        if obj is None:
            return None
        _title = str(obj.get("title"))
        return Channel(_title)

@dataclass
class Contributors:
    url: str
    count: int
    preview: List[Preview]

    @staticmethod
    def from_dict(obj: dict) -> 'Contributors':
        _url = str(obj.get("url"))
        _count = int(obj.get("count"))
        _preview = [Preview.from_dict(y) for y in obj.get("preview")]
        return Contributors(_url, _count, _preview)

@dataclass
class Link:
    url_type: str
    url: str

    @staticmethod
    def from_dict(obj: dict) -> 'Link':
        _url_type = str(obj.get("url_type"))
        _url = str(obj.get("url"))
        return Link(_url_type, _url)


@dataclass
class Pages:
    _from: str
    to: str

    @staticmethod
    def from_dict(obj: dict) -> 'Pages':
        if obj is None:
            return None
        _from = str(obj.get("from"))
        _to = str(obj.get("to"))
        return Pages(_from, _to)

@dataclass
class Title:
    en: str

    @staticmethod
    def from_dict(obj: dict) -> 'Title':
        _en = str(obj.get("en"))
        return Title(_en)

@dataclass
class Publication:
    category: Category
    channel: Channel
    contributors: Contributors
    cristin_result_id: str
    links: List[Link]
    original_language: str
    title: Title
    year_published: str
    url: str
    pages: Pages

    @staticmethod
    def from_dict(obj: dict) -> 'Publication':
        _category = Category.from_dict(obj.get("category"))
        _channel = Channel.from_dict(obj.get("channel"))
        _contributors = Contributors.from_dict(obj.get("contributors"))
        _cristin_result_id = str(obj.get("cristin_result_id"))
        _links = [Link.from_dict(y) for y in obj.get("links")] if obj.get("links") is not None else []
        _original_language = str(obj.get("original_language"))
        _title = Title.from_dict(obj.get("title"))
        _year_published = str(obj.get("year_published"))
        _url = str(obj.get("url"))
        _pages = Pages.from_dict(obj.get("pages"))
        return Publication(_category, _channel, _contributors, _cristin_result_id, _links, _original_language, _title, _year_published, _url, _pages)

@dataclass
class PersonSearchParameters:
    id: Optional[str] = None
    national_id: Optional[str] = None
    name: Optional[str] = None
    institution: Optional[str] = None
    parent_unit_id: Optional[str] = None
    levels: Optional[str] = None
    user: Optional[str] = None
    page: Optional[str] = None
    per_page: Optional[str] = None

    @staticmethod
    def from_dict(obj: dict) -> 'PersonSearchParameters':
        _id = str(obj.get("id"))
        _national_id = str(obj.get("national_id"))
        _name = str(obj.get("name"))
        _institution = str(obj.get("institution"))
        _parent_unit_id = str(obj.get("parent_unit_id"))
        _levels = str(obj.get("levels"))
        _user = str(obj.get("user"))
        _page = str(obj.get("page"))
        _per_page = str(obj.get("per_page"))
        return PersonSearchParameters(_id, _national_id, _name, _institution, _parent_unit_id, _levels, _user, _page, _per_page)
    
    def to_query_string(self) -> str:
        """Only not null variables are added to the query string"""
        return "&".join([f"{k}={v}" for k, v in self.__dict__.items() if v is not None])

@dataclass
class Person:
    first_name: str
    surname: str
    url: str
    cristin_person_id: str

    @staticmethod
    def from_dict(obj: dict) -> 'Person':
        _first_name = str(obj.get("first_name"))
        _surname = str(obj.get("surname"))
        _url = str(obj.get("url"))
        _cristin_person_id = str(obj.get("cristin_person_id"))
        return Person(_first_name, _surname, _url, _cristin_person_id)