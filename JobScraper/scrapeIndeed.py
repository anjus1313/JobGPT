from bs4 import BeautifulSoup
from lxml import etree as et
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from profession import Profession
import dbFunctions as db


# function to get DOM from given URL
def get_dom(driver, url):
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    dom = et.HTML(str(product_soup))
    return dom


def get_page(driver, url):
    driver.get(url)
    page_content = driver.page_source
    product_soup = BeautifulSoup(page_content, 'html.parser')
    return product_soup


# functions to extract job link
def get_job_link(job):
    try:
        job_link = job.xpath('./descendant::h2/a/@href')[0]
    except Exception as e:
        job_link = 'Not available'
    return job_link


# functions to extract job title
def get_job_title(job):
    try:
        job_title = job.xpath('./descendant::h2/a/span/text()')[0]
    except Exception as e:
        job_title = 'Not available'
    return job_title


# functions to extract the company name
def get_company_name(job):
    try:
        company_name = job.xpath('./descendant::span[@data-testid="company-name"]/text()')[0]
    except Exception as e:
        company_name = 'Not available'
    return company_name


# functions to extract the company location
def get_company_location(job):
    try:
        company_location = job.xpath('./descendant::div[@data-testid="text-location"]/text()')[0]
    except Exception as e:
        company_location = 'Not available'
    return company_location


# functions to extract job type
def get_job_type(job):
    try:
        job_type = job.xpath('./descendant::div[@data-testid="attribute_snippet_testid"]/text()')[0]
    except Exception as e:
        job_type = 'Not available'
    return job_type


# functions to extract job description
def get_job_desc(job):
    try:
        # job_desc = job.xpath('./descendant::div[@id="jobDescriptionText"]')
        # print(et.tostring(job_desc, pretty_print=True, encoding='unicode'))
        job_description_div = job.find(id="jobDescriptionText")
        job_desc = job_description_div.get_text(separator='\n')
    except Exception as e:
        job_desc = 'Not available'
    return job_desc


def scrape_indeed(job_search_keyword=None):
    profession = Profession()
    profession.platform = "indeed"
    # define job and location search keywords
    if job_search_keyword is None:
        job_search_keyword = ['Software+Engineering+Intern']
    location_keyword = 'United States'

    # define base and pagination URLs
    base_url = 'https://www.indeed.com'
    paginaton_url = "https://www.indeed.com/jobs?q={}&l={}&radius=35&start={}"

    # initialize Chrome webdriver using ChromeDriverManager
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # open initial URL
    driver.get("https://www.indeed.com/q-USA-jobs.html?vjk=823cd7ee3c203ac3")

    for job_keyword in job_search_keyword:
        all_jobs = []
        for page_no in range(0, 10, 10):
            url = paginaton_url.format(job_keyword, location_keyword, page_no)
            page_dom = get_dom(driver, url)
            jobs = page_dom.xpath('//div[@class="job_seen_beacon"]')
            all_jobs = all_jobs + jobs
        for job in all_jobs:
            profession.link = base_url + get_job_link(job)
            profession.title = get_job_title(job)
            profession.company = get_company_name(job)
            profession.location = get_company_location(job)
            profession.type = get_job_type(job)
            job = get_page(driver, profession.link)
            profession.content = get_job_desc(job)
            profession.clean_up()
            profession.convert_date()
            db.load_table(profession)
    # Closing the web browser
    driver.quit()


scrape_indeed(["Data Science Intern"])
db.display_table_rows('indeed')
