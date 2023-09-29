from datetime import datetime
import random
import re
from bs4 import BeautifulSoup
import time
import sqlite3
from urllib import parse

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

# TODO: improve these, sometimes they return empty, Month sometimes missing, etc
# We should do proper error handling if stuff is not found

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
        print("Setting up... ")
        headless = str(HEADLESS).lower()
        # Rotating Proxy Setup
        proxy_options = {
            'proxy': {
                'http': f'http://scrapeops.headless_browser_mode={headless}.country=us:{API_KEY}@proxy.scrapeops.io:5353',
                'https': f'http://scrapeops.headless_browser_mode={headless}.country=us:{API_KEY}@proxy.scrapeops.io:5353',
                'no_proxy': 'localhost:127.0.0.1'
            }
        } if USE_PROXY else None

        # Chromedriver Setup
        self.options = webdriver.ChromeOptions()
        if HEADLESS:
            self.options.add_argument("--headless")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-sh-usage')
        self.options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(options=self.options,
                                       seleniumwire_options=proxy_options)
        self.driver.set_page_load_timeout(60 * 2)

        # Database Setup
        self.con = sqlite3.connect(DATABASE + ".db")
        self.con.execute("CREATE TABLE IF NOT EXISTS profile(profile_id TEXT UNIQUE, saved BOOLEAN)")
        self.con.execute("CREATE TABLE IF NOT EXISTS company(company_id TEXT, description TEXT, website_url TEXT)")
        self.con.execute(
            "CREATE TABLE IF NOT EXISTS experience(profile_id TEXT, company_id TEXT, start_date DATE, end_date DATE)")
        self.con.commit()

        self.cursor = self.con.cursor()
        self.saved_profiles = set()
        self.potential_profiles = set()
        for row in self.cursor.execute("SELECT profile_id, saved FROM profile").fetchall():
            profile_id, saved = row[0], row[1]
            if saved:
                self.saved_profiles.add(profile_id)
            else:
                self.potential_profiles.add(profile_id)

        print("saved:", list(self.saved_profiles))
        print("potential:", list(self.potential_profiles))

    def profile_search(self, amount=10, start_profile_id=None):

        # get initial fetch
        if start_profile_id and start_profile_id not in self.saved_profiles:
            self.potential_profiles.add(start_profile_id)
            self.get_profile(start_profile_id)

        while amount > 0 and len(self.potential_profiles) > 0:
            profile_id = list(self.potential_profiles).pop()  # grab an id from list
            print("fetching profile:", profile_id)
            success = self.get_profile(profile_id)
            if success:
                amount -= 1
            else:
                print("FAILED")

            print("waiting")
            time.sleep(15)
        if amount == 0:
            print("search completed")
        elif len(self.potential_profiles) > 0:
            print("search ended early because of lack of users")

    def get_profile(self, profile_id):

        self.potential_profiles.remove(profile_id)
        self.driver.get(PROFILE_URL + profile_id)

        if "authwall" in self.driver.current_url:
            print("Err: authwall")
            return False
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        if not did_load_profile(soup):
            print("Err: couldnt find html")
            return False
        work_experience = extract_work_experience(soup)
        print("got experiences")
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
        self.con.execute(f"INSERT OR REPLACE INTO profile (profile_id, saved) VALUES ('{profile_id}', true)")
        self.saved_profiles.add(profile_id)
        related_profiles = extract_related_profiles(soup)
        print("got related")
        for related_profile_id in related_profiles:
            self.con.execute(
                f"INSERT INTO profile (profile_id, saved) VALUES ('{related_profile_id}', false) ON CONFLICT DO NOTHING")
            if related_profile_id not in self.saved_profiles:
                self.potential_profiles.add(related_profile_id)
        print("commited to db")
        self.con.commit()
        print("loaded profile:", profile_id, "  work experience:", work_experience, "  related:", related_profiles)
        return True

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
        # self.set_cookies()
        self.profile_search(3)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
