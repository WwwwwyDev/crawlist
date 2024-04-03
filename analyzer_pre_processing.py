from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from analyzer_util import *


class Action:

    @staticmethod
    def click(driver: WebDriver, xpath: str, info: dict) -> bool:
        """
        处理点击事件
        :param driver: selenium webdriver
        :param xpath: 点击按钮的xpath路径
        :param info: 该事件无需携带info
        :return: 是否成功
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        # 尝试点击两次
        try:
            element.click()
            AnalyzerUtil.random_sleep(0.1, 0.2)
        except Exception:
            try:
                element.click()
            except Exception:
                return False
        return True

    @staticmethod
    def inputKeyword(driver: WebDriver, xpath: str, info: dict) -> bool:
        """
        处理键盘输入事件
        :param driver: selenium webdriver
        :param xpath: 输入框的xpath路径
        :param info:  需要传入keyword关键词，{”keyword":"your keyword"}
        :return: 是否成功
        """
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        element = driver.find_element(By.XPATH, xpath)
        try:
            element.send_keys(info['keyword'])
        except Exception:
            return False
        return True

    @staticmethod
    def sendEnter(driver: WebDriver, xpath: str, info: dict) -> bool:
        """
        按一下回车键
        :param driver: selenium webdriver
        :param xpath: 输入框的xpath路径
        :param info: 该事件无需携带info
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
    def switchTab(driver: WebDriver, xpath: str, info: dict) -> bool:
        """
        切换到最后一个句柄
        :param driver: selenium webdriver
        :param xpath: 该事件无需携带xpath
        :param info: 该事件无需携带info
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
    def searchRedirect(driver: WebDriver, xpath, info: dict) -> bool:
        """
        将路径中的%s替换成keyword，并重定向
        :param driver:  selenium webdriver
        :param xpath: 该事件无需携带xpath
        :param info: 需要传入keyword关键词，{”keyword":"your keyword","url":"your url"}
        :return: 是否成功
        """
        try:
            url = AnalyzerUtil.url_format(info['url'], r"%s", info['keyword'])
            driver.get(url)
        except Exception:
            return False
        return True


action_mp = {
    "click": Action.click,
    "inputKeyword": Action.inputKeyword,
    "sendEnter": Action.sendEnter,
    "switchTab": Action.switchTab,
    "searchRedirect": Action.searchRedirect
}


def processing(driver: WebDriver, scripy: str, info=None) -> bool:
    """
        执行脚本
        :Args:
         - driver - webdriver驱动器
         - scripy - 脚本 例如: click://*[@id="tab-relation"] 点击xpath为//*[@id="tab-relation"]的元素
         - info - 传递的信息
    """
    if info is None:
        info = {'url': "", 'keyword': ""}
    try:
        action, xpath = "", ""
        if ":" not in scripy:
            action = scripy
        else:
            action, xpath = scripy.split(":")  # 通过":"分开事件与选择器
        if action not in action_mp:
            return False
        is_success = action_mp[action](driver, xpath, info)
        return is_success
    except Exception:
        return False


def pre_processing(driver: WebDriver, scripys: str, info=None, interval: int = 0.1) -> None:
    """
        执行脚本
        :Args:
         - driver - webdriver驱动器
         - scripys - 多个脚本,使用;分割
         - info - 传递的信息
         - interval - 每个动作的间隔时间
    """
    if info is None:
        info = {'url': "", 'keyword': ""}
    scripy_list = []
    if ";" not in scripys and scripys != "":
        scripy_list.append(scripys)
    else:
        scripy_list = scripys.split(";")  # 根据分号区分多个脚本
    res = []
    for scripy in scripy_list:
        res.append(processing(driver, scripy, info))
    # 如果有失败的，再执行一遍
    if False in res:
        res = []
        for scripy in scripy_list:
            res.append(processing(driver, scripy, info))
            AnalyzerUtil.random_sleep(0.3 + interval, 0.5 + interval)
    if False in res:
        raise Exception("预处理脚本失败,失败信息:", scripy_list, res)


