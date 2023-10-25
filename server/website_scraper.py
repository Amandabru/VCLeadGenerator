import os
import time
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
assert OPENAI_API_KEY, "OPENAI_API_KEY environment variable is missing from .env"

OPENAI_API_MODEL = os.getenv("OPENAI_API_MODEL", "gpt-3.5-turbo")
assert OPENAI_API_MODEL, "OPENAI_API_MODEL environment variable is missing from .env"

openai.api_key = OPENAI_API_KEY

HEADLESS = True

BASE_PROMPT = "YOU ARE A VENTURE CAPITALIST RESEARCHING A SPECIFIC COMPANY, WHAT IS IMPORTANT FOR YOU IS THE BUSINESS IDEA AND WHO THE FOUNDERS ARE AND WHAT THEY HAVE DONE PREVIOUSLY. "
SEARCH_HELP_PROMPT = "Which of these urls are most likely to contain important information about the business idea and leadership of the company? RESPOND BY ONLY A LIST OF URLS, SEPARATED BY NEWLINE, MINIMUM TWO, MAXIMUM 3:"
SUMMARIZE_PAGE_PROMPT = "Condense all important information about what this company is doing and discard unneccessary website information. You will get raw text data extracted from a webpage. RESPOND AS SHORTLY AS POSSIBLE WITHOUT REMOVING ANYTHING IMPORTANT. RESPOND ONLY WITH A SUMMARY. KEEP IT SHORT"
SUMMARIZE_ALL_PROMPT = "Combine inputs from the website, company linkedin and employee linkedin to create a concice summary with two tags [BUSINESS] and [FOUNDERS]. If founder information is not available don't write anything about it, including the tag Don't remove any important information, remove irrelevant information and keep it short. RESPOND ONLY WITH A SHORT AND RELEVANT SUMMARY"


# TODO Take a look at gpt functions and start implementing where possible

def gpt_summarize_all(webiste_information, linkedin_information, employee_information):
    website = "WEBSITE INFORMATION:\n" + "\n\n".join(webiste_information)
    linkedin = "LINKEDIN INFORMATION:\n" + str(linkedin_information)
    # Hur ska employees vara uppbyggt?
    # {Name, Role, Start} typ
    employees = "EMPLOYEE INFORMATION:\n" + str(employee_information)

    print("summarizer")
    print("website", website)
    print("linkedin", linkedin)
    print("employees", employees)

    message, reason = gpt(BASE_PROMPT + SUMMARIZE_ALL_PROMPT, website + linkedin + employees)
    return message["content"].strip()


def gpt_summarize_page(soup):
    message, reason = gpt(BASE_PROMPT + SUMMARIZE_PAGE_PROMPT, soup.text.strip())
    return message["content"].strip()


def gpt_get_urls(urls):
    functions = [
        {
            "name": "select_urls",
            "description": "Select one or two urls from the user input",
            "parameters": {
                "type": "object",
                "properties": {
                    "urls": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "description": "one url from the list supplied by the user"
                        },
                        "description": "list of urls that you have selected",
                    },
                    "unit": {"type": "array"},
                },
                "required": ["urls"],
            },
        }
    ]
    message, reason = gpt(SEARCH_HELP_PROMPT, ", ".join(urls))
    return message["content"].split()


def gpt(
        instruction_prompt: str,
        input_prompt: str,
        model: str = OPENAI_API_MODEL,
        temperature: float = 0.5,
        max_tokens: int = 500,
):
    while True:
        try:
            print("sending api request")
            messages = [{"role": "system", "content": instruction_prompt},
                        {"role": "user", "content": input_prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
                stop=None,
            )

            finish_reason = response.choices[0].finish_reason
            message = response.choices[0].message
            return message, finish_reason
        except openai.error.RateLimitError:
            print(
                "The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again."
            )
            time.sleep(10)  # Wait 10 seconds and try again

def gpt4(
        instruction_prompt: str,
        input_prompt: str,
        model: str = "gpt-4",
        temperature: float = 0.5,
        max_tokens: int = 2048,
):
    while True:
        try:
            print("sending api request")
            messages = [{"role": "system", "content": instruction_prompt},
                        {"role": "user", "content": input_prompt}]
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                n=1,
                stop=None,
            )

            finish_reason = response.choices[0].finish_reason
            message = response.choices[0].message
            return message, finish_reason
        except openai.error.RateLimitError:
            print(
                "The OpenAI API rate limit has been exceeded. Waiting 10 seconds and trying again."
            )
            time.sleep(10)  # Wait 10 seconds and try again


class WebsiteScraper:
    def __init__(self):
        print("Setting up... ")
        self.options = webdriver.ChromeOptions()
        if HEADLESS:
            self.options.add_argument("--headless")
        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--disable-dev-sh-usage')
        # self.options.add_argument('--blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(options=self.options)

    def get_navigation_urls(self, url, soup):
        all_links = soup.find_all('a', href=True)
        urls = []
        for link in all_links:
            absolute_url = urljoin(url, link['href'])
            if url in absolute_url:
                urls.append(absolute_url)
        return urls

    def summarize_page(self, url):
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        return gpt_summarize_page(soup)

    def info_search(self, url):
        print(url)
        self.driver.get(url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        urls = self.get_navigation_urls(url, soup)
        info_urls = gpt_get_urls(urls)
        all_info = [gpt_summarize_page(soup)]
        for url in info_urls:
            print(url)
            time.sleep(3)
            all_info.append(self.summarize_page(url))
        return all_info

    def separate_summary(self, summary):
        business = None
        founders = None
        if "[BUSINESS]" in summary:
            if "[FOUNDERS]" in summary:
                business = summary[summary.find("[BUSINESS]") + len("[BUSINESS]"):summary.find("[FOUNDERS]")].strip()
                founders = summary[summary.find("[FOUNDERS]") + len("[FOUNDERS]"):].strip()
            else:
                business = summary[summary.find("[BUSINESS]") + len("[BUSINESS]"):].strip()
        return business, founders

    def summarize_company_and_employees(self, company_info, employee_info):
        url = company_info["website"]
        website_info = self.info_search(url)
        summary = gpt_summarize_all(website_info, company_info, employee_info)
        business_info, founder_info = self.separate_summary(summary)
        print(business_info)
        print(founder_info)
        return business_info, founder_info


if __name__ == '__main__':
    scraper = WebsiteScraper()
    scraper.info_search("https://www.bemlo.se/")
