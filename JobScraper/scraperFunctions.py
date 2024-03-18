import requests
import copy
from datetime import datetime
from bs4 import BeautifulSoup


class Profession:
    title = None
    company = None
    location = None
    date = None
    date_object = None
    content = None
    link = None
    platform = 'Simplify'
    type = None

    def clean_up(self):
        attributes = ['title', 'company', 'location', 'date', 'content', 'link', 'platform', 'type']
        for attribute in attributes:
            if getattr(self, attribute):
                cleaned_value = getattr(self, attribute).strip().lower()
                encoded_string = cleaned_value.encode("ascii", "ignore")
                cleaned_value = encoded_string.decode()
                setattr(self, attribute, cleaned_value)

    def convert_date(self):
        default_year = datetime.now().year
        default_date = "01"
        if len(self.date.split()[1]) == 2:
            try:
                self.date_object = datetime.strptime(self.date + ' ' + str(default_year), '%b %d %Y')
            except ValueError:
                self.date_object = datetime.strptime('Jan 01 2022', '%b %d %Y')
        elif len(self.date.split()[1]) == 4:
            try:
                self.date_object = datetime.strptime(
                    self.date.split()[0] + ' ' + default_date + ' ' + self.date.split()[1], '%b %d %Y')
            except ValueError:
                self.date_object = datetime.strptime('Jan 01 2022', '%b %d %Y')
        else:
            self.date_object = datetime.strptime('Jan 01 2022', '%b %d %Y')


def scrape_github(url,job_type):
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
