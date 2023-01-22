from typing import List
from cristin_objects import Link
from downloader import download_papers_from_doi_links
from cristin_api import get_all_papers_by_author, get_all_unit_persons, get_person_by_author_number
import os

def get_doi_link_from_links(links: List[Link]) -> str:
    for link in links:
        if link.url_type == "DOI":
            return link.url
    return ""

def download_papers_from_author(author_number: int) -> None:
    papers = get_all_papers_by_author(author_number)
    person = get_person_by_author_number(author_number)
    doi_links = [get_doi_link_from_links(x.links) for x in papers if get_doi_link_from_links(x.links) != ""]
    if not doi_links:
        return
    print(person)
    output_dir = f"./Papers/{person.first_name} {person.surname}/"
    if os.path.exists(output_dir):
        print("Already downloaded")
        return
    os.makedirs(output_dir, exist_ok=True)
    download_papers_from_doi_links(doi_links, f"{os.path.abspath(output_dir)}\\")

def download_papers_from_unit(unit_id: str) -> None:
    persons = get_all_unit_persons(unit_id)
    for person in persons:
        download_papers_from_author(person.cristin_person_id)

if __name__ == "__main__":
    download_papers_from_unit("194.67.40.0")