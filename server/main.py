from datetime import datetime
import random
import re
from bs4 import BeautifulSoup
import time
import sqlite3
from urllib import parse, request

from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import os

load_dotenv()

API_KEY = str(os.getenv("API_KEY"))

MIN_WAIT = 1
MAX_WAIT = 5

GEO_ID = 105117694  # GEO id for Sweden
HOME_URL = "https://www.linkedin.com/"
JOB_URL = "https://www.linkedin.com/jobs/search"
COMPANY_URL = "https://www.linkedin.com/company/"
PROFILE_URL = "https://www.linkedin.com/in/"

# TOGGLING THIS COSTS MONEY. ONLY USE IN PROD WHEN DATA IS ACTUALLY SAVED
# Also requires .env file in directory with API_KEY set
USE_PROXY = False

# Disable graphical interface
HEADLESS = True

# What database to use. dev | prod
DATABASE = "dev"


# randomized waiting to act more human
def wait():
    time.sleep(MIN_WAIT + random.random() * MAX_WAIT)


# ---- Soup Functions ----

def extract_related_profiles(soup):
    profiles = set()
    related_profile_parent = soup.find("div", {"class": "aside-profiles-list"})
    if not related_profile_parent:
        return []
    related_profile_items = related_profile_parent.findAll("li")
    for related_profile_item in related_profile_items:
        profile_link = parse.unquote(related_profile_item.find("a", href=True)["href"])
        profile_id = profile_link[profile_link.index("in/") + len("in/"):profile_link.index("?")]
        profiles.add(profile_id)
    return list(profiles)


def extract_work_experience(soup):
    experiences = []
    work_experience_items = soup.findAll("li", {"class": "experience-item"})
    for work_experience_item in work_experience_items:
        # company_id
        link = work_experience_item.find("a", href=True)
        if not link:
            continue
        job_link = parse.unquote(link["href"])
        company_id = job_link[job_link.index("company/") + len("company/"):job_link.index("?")]

        # May have different positions w different timespans
        # TODO: dont skip this lol
        try:
            test = work_experience_item.find("ul", {"class": "experience-group__positions"})
            if test:
                continue
        except NoSuchElementException:
            pass
        # start and end time
        duration = work_experience_item.find("p", {"class": "experience-item__duration"})
        timestamps = duration.findAll("time")
        if len(timestamps) == 1:
            start_date = datetime.strptime(timestamps[0].text, "%b %Y")
            end_date = None
        else:
            start_date = datetime.strptime(timestamps[0].text, "%b %Y")
            end_date = datetime.strptime(timestamps[1].text, "%b %Y")

        experiences.append({
            "company_id": company_id,
            "start_date": start_date,
            "end_date": end_date
        })

    return experiences


def did_load_profile(soup):
    # Check if profile was fetched correctly, not authwall etc
    try:
        soup.find("li", {"class": "experience-item"})
        soup.find("div", {"class": "aside-profiles-list"})
    except NoSuchElementException:
        return False
    return True


class Scraper:

    def __init__(self):
        headless = str(HEADLESS).lower()
        # Rotating Proxy Setup
        proxy_options = {
            'proxy': {
                'http': f'http://scrapeops.headless_browser_mode={headless}:{API_KEY}@proxy.scrapeops.io:5353',
                'https': f'http://scrapeops.headless_browser_mode={headless}:{API_KEY}@proxy.scrapeops.io:5353',
                'no_proxy': 'localhost:127.0.0.1'
            }
        } if USE_PROXY else None

        # Chromedriver Setup
        self.options = webdriver.ChromeOptions()
        if HEADLESS:
            self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.options,
                                       seleniumwire_options=proxy_options)
        self.driver.set_page_load_timeout(60 * 2)

        # Database Setup
        self.con = sqlite3.connect(DATABASE + ".db")
        self.con.execute("CREATE TABLE IF NOT EXISTS profile(profile_id TEXT UNIQUE)")
        self.con.execute("CREATE TABLE IF NOT EXISTS company(company_id TEXT, description TEXT, website_url TEXT)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS experience(profile_id TEXT, company_id TEXT, start_date DATE, end_date DATE)")
        self.con.commit()

    def recursive_profile_search(self, start_profile_id):
        pass

    def get_profile(self, profile_id):
        self.driver.get(PROFILE_URL + profile_id)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        if not did_load_profile(soup):
            return
        work_experience = extract_work_experience(soup)
        self.con.execute(f"INSERT OR REPLACE INTO profile (profile_id) VALUES ('{profile_id}')")
        for experience in work_experience:
            company_id = experience["company_id"]
            start_date = experience["start_date"].strftime("%Y-%m-%d")
            if experience["end_date"]:
                end_date = experience["end_date"].strftime("%Y-%m-%d")
                self.con.execute(
                    f"INSERT INTO experience (profile_id, company_id, start_date, end_date) VALUES ('{profile_id}', '{company_id}', '{start_date}', '{end_date}')")
            else:
                self.con.execute(
                    f"INSERT INTO experience (profile_id, company_id, start_date) VALUES ('{profile_id}', '{company_id}', '{start_date}')")
        self.con.commit()
        related_profiles = extract_related_profiles(soup)
        return {
            "work_experience": work_experience,
            "related_profiles": related_profiles
        }

    def get_company_details(self, company_id):
        self.driver.get(COMPANY_URL + company_id)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        try:
            size_string = soup.find("div", {"data-test-id": "about-us__size"}).find("dd").text.strip()
            size_string = size_string.replace(",", "").replace(" ", "")
            numbers = re.findall(r'\d+', size_string)
            size = numbers[0]

            industry_string = soup.find("div", {"data-test-id": "about-us__industry"}).find("dd").text.strip()
            # Should also include description
            print(company_id, industry_string, size)
        except NoSuchElementException:
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

    def set_cookies(self):
        cookie = {"name": "lang",
                  "value": "\"v=2&lang=en-us\"",
                  "domain": ".linkedin.com"
                  }
        self.driver.execute_cdp_cmd('Network.enable', {})
        self.driver.execute_cdp_cmd('Network.setCookie', cookie)
        self.driver.execute_cdp_cmd('Network.disable', {})

    def start(self):
        self.set_cookies()
        self.get_profile("elias-lundgren")


if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
