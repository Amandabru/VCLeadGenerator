import random

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

MIN_WAIT = 1
MAX_WAIT = 5

GEO_ID = 105117694
JOB_URL = "https://www.linkedin.com/jobs/search"


def wait():
    time.sleep(MIN_WAIT + random.random() * MAX_WAIT)


class Scraper:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options)

    def get_company_details(self, company_id):
        pass

    def get_companies_from_job_search(self, keyword, amount):
        companies = set()  # holds company ids - works like usernames
        self.driver.get('http://www.linkedin.com/jobs/search' + "?keywords=" + keyword + "&geoId=" + str(GEO_ID))

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while len(companies) < amount:

            # Gather current job cards and extract id
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            job_cards = soup.find_all("div", {"class": "job-search-card"})
            for job_card in job_cards:
                job_name = job_card.find("h4", {"class": "base-search-card__subtitle"})
                job_link = job_name.find("a", href=True)["href"]
                company_id = job_link[job_link.index("company/") + len("company/"):job_link.index("?")]
                print(company_id)
                companies.add(company_id)
                print(len(companies),"/",amount)
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
        companies = self.get_companies_from_job_search("developer", 40)
        print(companies)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
