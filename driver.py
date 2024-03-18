# import undetected_chromedriver as webdriver
from selenium import webdriver
import undetected_chromedriver as uc


class web_driver:
    def __init__(self, url: str):
        self.exec_path = "/run/current-system/sw/bin/chromedriver"
        self.opt = webdriver.ChromeOptions()
        self.opt.binary_location = (
            "/etc/profiles/per-user/charles/bin/google-chrome-stable"
        )
        self.opt.add_argument("--user-data-dir=./user")
        self.opt.add_argument("--headless")
        try:
            self.driver = uc.Chrome(options=self.opt)
        except Exception:
            self.driver = webdriver.Chrome(options=self.opt)
        self.driver.get(url)
