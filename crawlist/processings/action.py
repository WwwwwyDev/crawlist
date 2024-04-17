import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from crawlist.annotation import check


class Action:

    @staticmethod
    @check(exclude="driver")
    def click(driver: WebDriver, xpath: str) -> bool:
        """
        Handling click events
        :param driver: selenium webdriver
        :param xpath: Click on the xpath path of the button
        :return: Whether successful
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        # Try clicking twice
        try:
            element.click()
            time.sleep(random.uniform(0.1, 0.2))
        except Exception:
            try:
                element.click()
            except Exception:
                return False
        return True

    @staticmethod
    @check(exclude="driver")
    def inputKeyword(driver: WebDriver, xpath: str, keyword: str) -> bool:
        """
        Handling keyboard input events
        :param driver: selenium webdriver
        :param xpath: The xpath path of the input box
        :param keyword: keyword needs to be passed in
        :return: Whether successful
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        try:
            element.send_keys(keyword)
        except Exception:
            return False
        return True

    @staticmethod
    @check(exclude="driver")
    def sendEnter(driver: WebDriver, xpath: str) -> bool:
        """
        Press the enter key once
        :param driver: selenium webdriver
        :param xpath: The xpath path of the input box
        :return: Whether successful
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        try:
            element.send_keys(Keys.RETURN)
        except Exception:
            return False
        return True

    @staticmethod
    @check(exclude="driver")
    def switchLastTab(driver: WebDriver) -> bool:
        """
        Switch to the last handle
        :param driver: selenium webdriver
        :return: Whether successful
        """
        try:
            window_handles = driver.window_handles
            if len(window_handles) < 2:
                return False
            driver.switch_to.window(window_handles[-1])
        except Exception as e:
            return False
        return True

    @staticmethod
    @check(exclude="driver")
    def switchTab(driver: WebDriver, index: int) -> bool:
        """
        Switch to the index handle
        :param driver: selenium webdriver
        :param index: The index handle
        :return: Whether successful
        """
        try:
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[index])
        except Exception as e:
            return False
        return True

    @staticmethod
    @check(exclude="driver")
    def searchRedirect(driver: WebDriver, url: str, keyword: str) -> bool:
        """
        Replace % s in the path with keyword and redirect it
        :param driver:  selenium webdriver
        :param url: Link containing %s
        :param keyword: keyword needs to be passed in
        :return: Whether successful
        """
        try:
            url = url.replace(r"%s", keyword)
            driver.get(url)
        except Exception:
            return False
        return True

    @staticmethod
    @check(exclude="driver")
    def redirect(driver: WebDriver, url: str) -> bool:
        """
        Direct redirection
        :param driver:  selenium webdriver
        :param url: Links that require redirection
        :return: Whether successful
        """
        try:
            driver.get(url)
        except Exception:
            return False
        return True
