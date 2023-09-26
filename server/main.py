import random
import pickle
import re
from bs4 import BeautifulSoup
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import os

load_dotenv()

MIN_WAIT = 1
MAX_WAIT = 5

GEO_ID = 105117694  # GEO id for Sweden
JOB_URL = "https://www.linkedin.com/jobs/search"
COMPANY_URL = "https://www.linkedin.com/company/"
PROFILE_URL = "https://www.linkedin.com/in/"

USE_PROXY = False


# randomized waiting to act more human
def wait():
    time.sleep(MIN_WAIT + random.random() * MAX_WAIT)


# reroutes url via proxy to avoid authwall etc
def proxy(url):
    if not USE_PROXY:
        return url
    return 'https://proxy.scrapeops.io/v1/' + "?api_key=" + str(os.getenv("API_KEY") + "&url=" + url)


class Scraper:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")  # run without a browser window, nice to disable while debugging though
        self.driver = webdriver.Chrome(options=self.options)

    def get_profile_work_experience(self, profile_id):
        self.driver.get(proxy(PROFILE_URL + profile_id))
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        try:
            work_experience_items = soup.findAll("li", {"class": "experience-item"})
            for work_experience_item in work_experience_items:
                job_link = work_experience_item.find("a", href=True)["href"]
                company_id = job_link[job_link.index("company/") + len("company/"):job_link.index("?")]
                print(profile_id, company_id)
        except:
            print("Error: failed to fetch profile", profile_id)

    def get_company_details(self, company_id):
        self.driver.get(proxy(COMPANY_URL + company_id))
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        try:
            size_string = soup.find("div", {"data-test-id": "about-us__size"}).find("dd").text.strip()
            size_string = size_string.replace(",", "").replace(" ", "")
            numbers = re.findall(r'\d+', size_string)
            size = numbers[0]

            industry_string = soup.find("div", {"data-test-id": "about-us__industry"}).find("dd").text.strip()
            print(company_id, industry_string, size)
        except:
            print("Error: failed to fetch company", company_id)

        # almost always blocked by authwall, we need an account and cookies

    def get_companies_from_job_search(self, keyword, amount):
        companies = set()  # holds company ids - works like usernames
        self.driver.get(JOB_URL + "?keywords=" + keyword + "&geoId=" + str(GEO_ID))

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(companies) < amount:

            # Gather current job cards and extract id
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            job_cards = soup.find_all("div", {"class": "job-search-card"})
            for job_card in job_cards:
                job_name = job_card.find("h4", {"class": "base-search-card__subtitle"})
                job_link = job_name.find("a", href=True)["href"]
                company_id = job_link[job_link.index("company/") + len("company/"):job_link.index("?")]
                companies.add(company_id)
                print(len(companies), "/", amount)
                if len(companies) == amount:
                    break

            # Click if button and scroll down
            try:
                button = self.driver.find_element(By.CLASS_NAME, "infinite-scroller__show-more-button")
            except NoSuchElementException:
                button = None
            if button and button.is_displayed():
                button.click()
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait()
            current_height = self.driver.execute_script("return document.body.scrollHeight")
            if current_height == last_height:
                break
            last_height = current_height

        return list(companies)

    def start(self):
        self.get_profile_work_experience("victoria-dinic")
        # companies = self.get_companies_from_job_search("developer", 10)
        # wait()
        # for company in companies:
        #     self.get_company_details(company)
        #     wait()


if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
