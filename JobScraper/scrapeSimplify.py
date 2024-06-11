import requests
import copy
from bs4 import BeautifulSoup
from profession import Profession


def scrape_github(url, job_type):
    professions = []
    profession = Profession()
    profession.type = job_type
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    tables = soup.find_all('table')
    table_body = tables[1].find('tbody')
    table_rows = table_body.find_all('tr')
    for row in table_rows:
        cell = row.find_all('td')
        if cell[0].find('a'):
            profession.company = cell[0].find('a').text
        if cell[1]:
            profession.title = cell[1].text
        if cell[2]:
            profession.location = cell[2].text
        if cell[4]:
            profession.date = cell[4].text
        links = cell[3].find_all('a')
        for link in links:
            img = link.find('img')
            if img and img.has_attr('alt') and img['alt'] == 'Simplify':
                profession.link = link.get('href')
                professions.append(copy.deepcopy(profession))
    return professions


def scrape_simplify(url):
    job_content = ""
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    prefix_elements = soup.find_all(lambda tag: tag.has_attr('id') and tag['id'].startswith('details-card-'))
    content = prefix_elements[0]
    divs = content.find_all(class_="text-left")
    for div in divs:
        title = div.find(class_="mt-3 text-base font-semibold")
        if title:
            job_content += title.text + "\n"
        ul = div.find("ul")
        if ul:
            lists = div.find_all("li")
            for li in lists:
                job_content += li.text + "\n"
    return job_content
