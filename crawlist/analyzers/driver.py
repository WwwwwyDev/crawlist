from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import DesiredCapabilities


class BaseDriver(object):
    pass


class Driver(BaseDriver):

    def get_driver(self) -> WebDriver:
        raise NotImplementedError

    def __call__(self) -> WebDriver:
        return self.get_driver()


class DefaultDriver(Driver):
    def __init__(self, is_debug: bool = False, is_eager: bool = False):
        self.is_debug = is_debug
        self.is_eager = is_eager

    def get_driver(self) -> WebDriver:
        option = wd.ChromeOptions()
        add_default_chrome_options(option)
        if not self.is_debug:
            option.add_argument("--headless")
        if self.is_eager:
            option.page_load_strategy = 'eager'
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => false
                })
              """
        })
        webdriver.implicitly_wait(10)
        return webdriver


class DefaultRemoteDriver(Driver):
    def __init__(self, webdriver_url: str, is_eager: bool = False):
        self.webdriver_url = webdriver_url
        self.is_eager = is_eager

    def get_driver(self) -> WebDriver:
        option = wd.ChromeOptions()
        add_default_chrome_options(option)
        option.add_argument("--headless")
        if self.is_eager:
            option.page_load_strategy = 'eager'
        option.set_capability('cloud:options', DesiredCapabilities.CHROME)
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        webdriver = wd.Remote(command_executor=self.webdriver_url, options=option)
        webdriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                  get: () => false
                })
              """
        })
        webdriver.implicitly_wait(10)
        return webdriver


def add_default_chrome_options(option: ArgOptions):
    arguments = [
        "no-sandbox",
        "--disable-extensions",
        '--disable-gpu',
        'User-Agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"',
        "window-size=1920x3000",
        "start-maximized",
        'cache-control="max-age=0"',
        "disable-blink-features=AutomationControlled"
    ]
    for argument in arguments:
        option.add_argument(argument)
