from typing import List
import requests
from cristin_objects import Publication, PersonSearchParameters, Person

CRISTIN_API_BASE = "https://api.cristin.no/v2/"

def get_paginated(url: str, page: int, max_count: int=1000) -> List[dict]:
    res = requests.get(url, params={"page": page, "per_page": max_count})
    return res.json()

def get_all_paginated(url: str, max_count: int=1000) -> List[dict]:
    res = requests.get(url)
    count = int(res.headers["x-total-count"])
    page = 1
    total_results = []
    while len(total_results) < count:
        res = get_paginated(url, page, max_count)
        total_results += res
        page += 1
    return total_results

def get_author_papers_url(author_number: int) -> str:
    return f"{CRISTIN_API_BASE}persons/{author_number}/results"

def filter_articles(papers: List[Publication]) -> List[Publication]:
    return [x for x in papers if x.category.code == "ARTICLE"]

def get_all_papers_by_author(author_number: int) -> List[Publication]:
    url = get_author_papers_url(author_number)
    res = get_all_paginated(url)
    return filter_articles([Publication.from_dict(x) for x in res])

def get_person_search_url(search_params: PersonSearchParameters) -> str:
    return f"{CRISTIN_API_BASE}persons?{search_params.to_query_string()}"

def search_persons(search_params: PersonSearchParameters) -> List[dict]:
    url = get_person_search_url(search_params)
    res = get_all_paginated(url)
    return [Person.from_dict(x) for x in res]

def get_all_unit_persons(unit_id: str) -> List[Person]:
    search_params = PersonSearchParameters(parent_unit_id=unit_id)
    return search_persons(search_params)

def get_person_by_author_number(author_number: int) -> Person:
    search_params = PersonSearchParameters(id=author_number)
    return search_persons(search_params)[0]