import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Action:

    @staticmethod
    def click(driver: WebDriver, xpath: str) -> bool:
        """
        处理点击事件
        :param driver: selenium webdriver
        :param xpath: 点击按钮的xpath路径
        :return: 是否成功
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        # 尝试点击两次
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
    def inputKeyword(driver: WebDriver, xpath: str, keyword: str) -> bool:
        """
        处理键盘输入事件
        :param driver: selenium webdriver
        :param xpath: 输入框的xpath路径
        :param keyword:  需要传入keyword关键词
        :return: 是否成功
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        try:
            element.send_keys(keyword)
        except Exception:
            return False
        return True

    @staticmethod
    def sendEnter(driver: WebDriver, xpath: str) -> bool:
        """
        按一下回车键
        :param driver: selenium webdriver
        :param xpath: 输入框的xpath路径
        :return: 是否成功
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        try:
            element.send_keys(Keys.RETURN)
        except Exception:
            return False
        return True

    @staticmethod
    def switchLastTab(driver: WebDriver) -> bool:
        """
        切换到最后一个句柄
        :param driver: selenium webdriver
        :return: 是否成功
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
    def switchTab(driver: WebDriver, index: int) -> bool:
        """
        切换到第index个句柄
        :param driver: selenium webdriver
        :param index: 第index个句柄
        :return: 是否成功
        """
        try:
            window_handles = driver.window_handles
            driver.switch_to.window(window_handles[index])
        except Exception as e:
            return False
        return True

    @staticmethod
    def searchRedirect(driver: WebDriver, url: str, keyword: str) -> bool:
        """
        将路径中的%s替换成keyword,并重定向
        :param driver:  selenium webdriver
        :param url: 含%s的链接
        :param keyword: 需要传入keyword关键词
        :return: 是否成功
        """
        try:
            url = url.replace(r"%s", keyword)
            driver.get(url)
        except Exception:
            return False
        return True

    @staticmethod
    def redirect(driver: WebDriver, url: str) -> bool:
        """
        将路径中的%s替换成keyword,并重定向
        :param driver:  selenium webdriver
        :param url: 需要重定向的链接
        :return: 是否成功
        """
        try:
            driver.get(url)
        except Exception:
            return False
        return True
