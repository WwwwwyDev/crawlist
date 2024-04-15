from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import DesiredCapabilities


class BaseDriver(object):
    pass


class Browser:
    """
    Set of supported locator strategies.
    """

    Chrome = "chrome"
    Firefox = "firefox"


class Driver(BaseDriver):

    def get_driver(self) -> WebDriver:
        raise NotImplementedError

    def __call__(self) -> WebDriver:
        return self.get_driver()


class DefaultDriver(Driver):
    def __init__(self):
        pass

    def get_driver(self) -> WebDriver:
        option = wd.ChromeOptions()
        add_default_options(option)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        webdriver.implicitly_wait(10)
        return webdriver


class DefaultRemoteDriver(Driver):
    def __init__(self, webdriver_url: str):
        self.webdriver_url = webdriver_url

    def get_driver(self) -> WebDriver:
        option = wd.ChromeOptions()
        add_default_options(option)
        option.set_capability('cloud:options', DesiredCapabilities.CHROME)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        webdriver = wd.Remote(command_executor=self.webdriver_url, options=option)
        webdriver.implicitly_wait(10)
        return webdriver


def add_default_options(option: ArgOptions):
    arguments = [
        "no-sandbox",
        "--disable-extensions",
        '--disable-gpu',
        "--headless",
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
        "window-size=1920x3000",
        "start-maximized",
        'cache-control="max-age=0"'
    ]
    for argument in arguments:
        option.add_argument(argument)
    option.page_load_strategy = 'eager'


