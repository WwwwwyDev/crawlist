from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager


class BaseDriver(object):
    pass


class Driver(BaseDriver):

    def get_driver(self) -> WebDriver:
        raise NotImplementedError

    def __call__(self) -> WebDriver:
        return self.get_driver()


class DefaultDriver(Driver):
    def __init__(self):
        pass

    def get_driver(self) -> WebDriver:
        arguments = [
            "no-sandbox",
            "--disable-extensions",
            '--disable-gpu',
            "--headless=chrome",
            'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
            "window-size=1920x3000",
            "start-maximized",
            'cache-control="max-age=0"'
        ]
        option = wd.ChromeOptions()
        for argument in arguments:
            option.add_argument(argument)
        option.page_load_strategy = 'eager'

        webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        webdriver.implicitly_wait(10)
        return webdriver
