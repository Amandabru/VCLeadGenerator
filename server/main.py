import random
import pickle
import re
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

MIN_WAIT = 1
MAX_WAIT = 5

GEO_ID = 105117694  # GEO id for Sweden
JOB_URL = "https://www.linkedin.com/jobs/search"
COMPANY_URL = "https://www.linkedin.com/company/"


def wait():
    time.sleep(MIN_WAIT + random.random() * MAX_WAIT)


class Scraper:

    def __init__(self):
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument("--headless")  # run without a browser window, nice to disable while debugging though
        self.driver = webdriver.Chrome(options=self.options)

    def get_company_details(self, company_id):
        self.driver.get(COMPANY_URL + company_id)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        try:
            size_string = soup.find("div", {"data-test-id": "about-us__size"}).find("dd").text.strip()
            size_string = size_string.replace(",", "").replace(" ", "")
            numbers = re.findall(r'\d+', size_string)
            size = numbers[0]

            industry_string = soup.find("div", {"data-test-id": "about-us__industry"}).find("dd").text.strip()
            print(company_id, industry_string, size)
        except:
            print(company_id, "failed to fetch")

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

    def load_cookies(self):
        self.driver.get("https://www.linkedin.com/")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            self.driver.add_cookie(cookie)
        wait()
        self.driver.get("https://www.linkedin.com/feed")
        wait()

    def create_cookies(self):
        self.driver.get("https://www.linkedin.com/")
        # let user login on linkedin and get cookies
        time.sleep(60)
        print("saving cookies:",self.driver.get_cookies())
        # dump the cookie to use in scraping
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def start(self):
        self.load_cookies()
        #self.create_cookies()

        # companies = self.get_companies_from_job_search("developer", 10)
        # wait()
        # for company in companies:
        #     self.get_company_details(company)
        #     wait()


if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
