from driver import web_driver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random


# TODO add llm to answer questions


def main():
    logged_in = False
    job_search = input("Enter job title: ")
    indeed = Indeed(job_search)
    time.sleep(random.randint(5, 15))
    if not logged_in and "logged in" not in open("login.txt").read():
        print("Login on browser for bot to work")
        with open("login.txt", "w") as file:
            file.write(input('type "logged in" when you have logged in \n--> '))
    leads = indeed.leads()
    for lead in leads:
        lead.apply()


class Indeed:
    def __init__(self, job_title: str) -> None:
        self.root_url = "https://www.indeed.com"
        self.driver = web_driver(self.root_url).driver
        self.job_title = job_title
        self.done_jobs_search = False

    def search(self) -> None:
        input = self.driver.find_element(By.ID, "text-input-what")
        input.send_keys(self.job_title)
        input.send_keys(Keys.ENTER)

    def job_list(self):
        # gets a list of job cards
        if not self.done_jobs_search:
            self.search()
            self.done_jobs_search = True
        driver = self.driver
        self.done_jobs_search = True
        return driver.find_elements(By.CLASS_NAME, "job_seen_beacon")

    def leads(self):
        driver = self.driver
        if not self.done_jobs_search:
            self.search()
            self.done_jobs_search = True
        jobs = self.job_list()

        leads = [
            Job(
                job.find_element(By.TAG_NAME, "a").text,
                job.find_element(By.TAG_NAME, "a").get_attribute("href"),
                self.is_easy_apply(job),
                driver,
            )
            for job in jobs
        ]
        return leads

    def is_easy_apply(self, job) -> bool:
        if "Easily apply" in job.text:
            return True
        return False


class Job:
    def __init__(self, title: str, url: str, is_easy_apply, driver):
        self.title = title
        self.is_easy_apply = is_easy_apply
        self.driver = driver
        self.url = url

    def __str__(self):
        return (
            f"Title: {self.title}\nURL: {self.url} \nEasy Apply: {self.is_easy_apply}"
        )

    def apply(self) -> None:
        print(f"attempting to apply for {self.title}")
        clickables = [
            "apply",
            "apply now",
            "continue",
            "continue applying",
            "next",
            "submit",
            "submit your application",
            "review your application",
        ]
        page = self.driver
        page.get(self.url)
        time.sleep(5)
        if self.is_easy_apply:
            try:
                apply_button = page.find_element(
                    By.XPATH, "//button[@data-testid='commute-check-continue-button']"
                )
                print(apply_button.text)
                apply_button.click()
            except Exception as e:
                print("No commute check")
            try:
                apply_button = page.find_element(By.ID, "indeedApplyButton")
                print(apply_button.text)
                apply_button.click()
                text = ""
                limit = 8
                attempts = 0
                while True:
                    attempts += 1
                    time.sleep(random.randint(5, 25))
                    buttons = page.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        text = button.text.lower()
                        if text in clickables:
                            button.click()
                    if (
                        text == "submit your application"
                        or text == "return to job search"
                    ):
                        print(f"Application submitted to {self.title}")
                        break
                    if attempts > limit:
                        break
            except Exception as e:
                print(e)
                print("No apply button")


if __name__ == "__main__":
    main()
