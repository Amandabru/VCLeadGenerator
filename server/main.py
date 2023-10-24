from datetime import datetime
import random
import re
from urllib.parse import urlparse

from bs4 import BeautifulSoup
import time
import sqlite3
from urllib import parse

from dotenv import load_dotenv
from seleniumwire import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import os
from database import Database
from website_scraper import WebsiteScraper

load_dotenv()

API_KEY = str(os.getenv("API_KEY"))

MIN_WAIT = 10
MAX_WAIT = 30

GEO_ID = 105117694  # GEO id for Sweden
HOME_URL = "https://www.linkedin.com/"
JOB_URL = "https://www.linkedin.com/jobs/search"
COMPANY_URL = "https://www.linkedin.com/company/"
PROFILE_URL = "https://www.linkedin.com/in/"

# TOGGLING THIS COSTS MONEY. ONLY USE IN PROD WHEN DATA IS ACTUALLY SAVED
# Also requires .env file in directory with API_KEY set
USE_PROXY = True

# Disable graphical interface
HEADLESS = True

# What database to use. dev | prod
DATABASE = "dev"


# randomized waiting to act more human
def wait():
    time.sleep(MIN_WAIT + random.random() * MAX_WAIT)


# ---- Soup Functions ----

valid_locations = {
    "stockholm", "solna", "kista", "gothenburg"
}

def extract_related_profiles(soup):
    profiles = set()
    related_profile_parent = soup.find("div", {"class": "aside-profiles-list"})
    if not related_profile_parent:
        return []
    related_profile_items = related_profile_parent.findAll("li")
    for related_profile_item in related_profile_items:
        try:
            profile_location = related_profile_item.find("div", {"class": "base-aside-card__metadata"})
            location_text = profile_location.text.strip().lower()
            valid = False
            for location in valid_locations:
                if location in location_text:
                    valid = True
                    break
            if not valid:
                continue
        except NoSuchElementException:
            continue
        profile_link = parse.unquote(related_profile_item.find("a", href=True)["href"])
        profile_id = profile_link[profile_link.index("in/") + len("in/"):profile_link.index("?")]
        profiles.add(profile_id)

    return list(profiles)


def extract_work_experience(company_id, soup):
    # start and end time

    start_date = None
    end_date = None
    try:
        timestamps = soup.findAll("time")
        try:
            if len(timestamps) == 1:
                start_date = datetime.strptime(timestamps[0].text, "%b %Y").strftime("%Y-%m-%d")
                end_date = None
            else:
                start_date = datetime.strptime(timestamps[0].text, "%b %Y").strftime("%Y-%m-%d")
                end_date = datetime.strptime(timestamps[1].text, "%b %Y").strftime("%Y-%m-%d")
        except ValueError:
            print("Err: could not parse dates 1", timestamps)

        if not start_date and not end_date:
            try:
                if len(timestamps) == 1:
                    start_date = datetime.strptime(timestamps[0].text, "%Y").strftime("%Y-%m-%d")
                    end_date = None
                else:
                    start_date = datetime.strptime(timestamps[0].text, "%Y").strftime("%Y-%m-%d")
                    end_date = datetime.strptime(timestamps[1].text, "%Y").strftime("%Y-%m-%d")
            except ValueError:
                print("Err: could not parse dates 2", timestamps)
    except:
        print("could not get duration or timestamp")
        pass

    # Role
    role = None
    try:
        role = soup.find("h3").text.strip()
    except:
        print("could not get role")
        pass

    return {
        "company_id": company_id,
        "role": role,
        "start_date": start_date,
        "end_date": end_date
    }


def extract_work_experiences(soup):
    experiences = []
    work_experience_items = soup.findAll("li", {"class": "experience-item"})
    for work_experience_item in work_experience_items:
        # company_id
        link = work_experience_item.find("a", href=True)
        if not link:
            continue
        job_link = parse.unquote(link["href"])
        company_id = job_link[job_link.index("company/") + len("company/"):job_link.index("?")]
        print("work exp", company_id)
        multiple_positions = None
        try:
            multiple_positions = work_experience_item.find("ul", {"class": "experience-group__positions"})
        except NoSuchElementException:
            print("no multiple positions")
            pass

        if multiple_positions:
            group_positions = work_experience_item.findAll("li", {"class": "experience-group-position"})
            for group_position in group_positions:
                experience = extract_work_experience(company_id, group_position)
                experiences.append(experience)
        else:
            experience = extract_work_experience(company_id, work_experience_item)
            experiences.append(experience)

    return experiences


def extract_profile_name(soup):
    try:
        top_card = soup.find("section", {"class": "top-card-layout"})
        name = top_card.find("h1").text.strip()
    except:
        return
    return name


def extract_education(soup):
    educations = []
    education_items = soup.findAll("li", {"class": "education__list-item"})
    for education_item in education_items:
        school_text = education_item.find("h3", {"class": "profile-section-card__title"}).text.strip()

        degree = education_item.find("h4", {"class": "profile-section-card__subtitle"})
        degree_spans = degree.findAll("span")
        degree_text = ""

        for span in degree_spans:
            text = span.text.strip()
            if text == "-":
                continue
            text = re.sub(r'[0-9]', "", text.replace(".", ""))
            degree_text += " " + text

        degree_text = degree_text.strip()
        educations.append({"school": school_text, "degree": degree_text})
    return educations


def extract_company_info(soup):
    size_string = soup.find("div", {"data-test-id": "about-us__size"}).find("dd").text.strip()
    size_string = size_string.replace(",", "").replace(" ", "")
    numbers = re.findall(r'\d+', size_string)
    size = numbers.pop()

    try:
        better_size = soup.find("a", {"class": "face-pile__cta"}).text.strip()
        better_size = "".join(i for i in better_size if i.isdigit())
        size = better_size
    except:
        pass

    name_string = soup.find("h1").text.strip()
    industry_string = soup.find("div", {"data-test-id": "about-us__industry"}).find("dd").text.strip()

    website = soup.find("div", {"data-test-id": "about-us__website"}).find("dd").find("a", href=True)
    website_url = None
    if website:

        website_url = parse.unquote(website["href"])
        if "?url=" in website_url:
            website_url = website_url[website_url.find("?url=") + len("?url="):]
        if "&" in website_url:
            website_url = website_url[:website_url.find("&")]
        parsed_url = urlparse(website_url)
        website_url = "https://" + parsed_url.netloc

    about_string = soup.find("p", {"data-test-id": "about-us__description"}).text.strip()

    # todo add employees
    # (extract person info)

    profiles = set()

    try:
        employees_parent = soup.find("section", {"data-test-id": "employees-at"})
        employee_items = employees_parent.findAll("li")
        for employee_item in employee_items:
            profile_link = parse.unquote(employee_item.find("a", href=True)["href"])
            profile_id = profile_link[profile_link.index("in/") + len("in/"):profile_link.index("?")]
            profiles.add(profile_id)
    except:
        pass

    company = {
        "name": name_string,
        "industry": industry_string,
        "size": size,
        "description": about_string,
        "website": website_url,
        "employees": list(profiles),
    }
    return company


def did_load_profile(url, soup):
    if "authwall" in url:
        print("Err: authwall")
        return False
    # Check if profile was fetched correctly, not authwall etc
    try:
        soup.find("li", {"class": "experience-item"})
        # soup.find("li", {"class": "education__list-item"})
        soup.find("div", {"class": "aside-profiles-list"})
    except NoSuchElementException:
        return False
    blurred = False
    try:
        blur = soup.find("div", {"class": "blur"})
        if blur:
            blurred = True
    except NoSuchElementException:
        pass
    if blurred:
        return False
    return True


def did_load_company(url, soup):
    if "authwall" in url:
        print("Err: authwall")
        return False
    return True


class Scraper:

    def __init__(self):
        print("Setting up... ")
        headless = str(HEADLESS).lower()
        # Rotating Proxy Setup
        proxy_options = {
            'proxy': {
                'http': f'http://scrapeops.country=us.headless_browser_mode={headless}.optimize_request=true:{API_KEY}@proxy.scrapeops.io:5353',
                'https': f'http://scrapeops.country=us.headless_browser_mode={headless}.optimize_request=true:{API_KEY}@proxy.scrapeops.io:5353',
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
        self.options.add_argument('--ignore-certificate-errors')
        self.driver = webdriver.Chrome(options=self.options,
                                       seleniumwire_options=proxy_options)
        self.driver.set_page_load_timeout(60 * 2)
        self.database = Database(DATABASE)

    def profile_search(self, amount=10, start_profile_id=None):
        # get initial fetch
        if start_profile_id and start_profile_id not in self.database.potential_profiles:
            self.database.potential_profiles.add(start_profile_id)
            self.get_profile(start_profile_id)

        while amount > 0 and len(self.database.potential_profiles) > 0:
            profile_list = list(self.database.potential_profiles)  # grab an id from list
            profile_id = profile_list.pop(random.randint(0, len(profile_list) - 1))
            print("profile search", profile_id)

            success = False
            try:
                success = self.get_profile(profile_id)
            except Exception as e:
                print("UPPER ERROR:", e)

            if success:
                amount -= 1

            time.sleep(15)

        if amount == 0:
            print("search completed")
        elif len(self.database.potential_profiles) > 0:
            print("search ended early because of lack of users")

    def company_search(self, amount=10):
        print("company search")
        summarizer = WebsiteScraper()
        while amount > 0 and len(self.database.potential_companies) > 0:
            company_list = list(self.database.potential_companies)  # grab an id from list
            company_id = company_list.pop(random.randint(0, len(company_list) - 1))
            company = False
            try:
                company = self.get_company(company_id)
            except Exception as e:
                print("UPPER ERROR:", e)

            if company:
                amount -= 1

                for employee in company["employees"]:
                    self.get_profile(employee)

                employees = self.get_employees(company_id)
                summary = summarizer.summarize_company_and_employees(company, employees)
                print("result:")
                print(summary)
                # get employees

            time.sleep(15)

        if amount == 0:
            print("search completed")
        elif len(self.database.potential_companies) > 0:
            print("search ended early because of lack of companies")

    def company_list_summarize(self, companies):
        summarizer = WebsiteScraper()
        for company_id in companies:
            company = False
            try:
                company = self.get_company(company_id)
            except Exception as e:
                print("UPPER ERROR:", e)

            if company:
                wait()
                for employee in company["employees"]:
                    self.get_profile(employee, 2)
                    wait()

                employees = self.get_employees(company_id)
                summary = summarizer.summarize_company_and_employees(company, employees)
                print("result:")
                print(summary)
                # get employees

            wait()

    def get_profile(self, profile_id, tries=1):
        print("get_profile", profile_id)
        success = False
        while tries > 0 and not success:
            tries -= 1
            time.sleep(10)
            self.driver.get(PROFILE_URL + profile_id)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            if not did_load_profile(self.driver.current_url, soup):
                print("error loading", profile_id, )
                print("retrying", tries)
                continue

            try:
                # Get profile work experience
                print("getting work experience and education")
                work_experience = extract_work_experiences(soup)
                education_experience = extract_education(soup)
                if len(work_experience) == 0 and len(education_experience) == 0 and tries > 0:
                    print("retrying to get experience")
                    continue
                for experience in work_experience:
                    company_id = experience["company_id"]
                    start_date = experience["start_date"]
                    end_date = experience["end_date"]
                    role = experience["role"]
                    self.database.add_experience(profile_id, company_id, role, start_date, end_date)

                    # If the company is not added to database, add it
                    self.database.add_company(company_id)

                # Get profile education
                education_experience = extract_education(soup)
                for education in education_experience:
                    school = education["school"]
                    degree = education["degree"]
                    self.database.add_education(profile_id, school, degree)  # s error here??!??! something sqlite but idk

                # Enter that data has been saved in profile db
                print("getting name")
                name = extract_profile_name(soup)
                if not name:
                    name = profile_id.replace("-"," ")
                self.database.add_profile(profile_id, True, name)

                # Get related profiles and insert potential future profiles into database
                print("getting related")
                related_profiles = extract_related_profiles(soup)
                for related_profile_id in related_profiles:
                    self.database.add_profile(related_profile_id, False)
                print("loaded profile:", profile_id, "  work experience:", work_experience, " education:",
                      education_experience,
                      "  related:", related_profiles)
                success = True

            except Exception as e:
                print("ERROR:", e)
                self.database.rollback()
                success = False
                continue

        if not success:
            return False

        # Commit all database changes
        self.database.commit()
        return True

    def get_company(self, company_id):
        self.driver.get(COMPANY_URL + company_id)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        if not did_load_profile(self.driver.current_url, soup):
            print("error loading")
            return False

        company = extract_company_info(soup)
        self.database.add_company(company_id, company)
        self.database.commit()

        return company

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

    def get_employees(self, company_id):
        return self.database.get_employee_info(company_id)

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
        self.company_list_summarize(["andrepeat"])
        # self.profile_search(1, )
        # self.company_search(1)
        #print(self.get_company("winteria"))
        # self.get_employees("kth")

# TODO split summary text and add that to database too

if __name__ == '__main__':
    scraper = Scraper()
    scraper.start()
