from crawlist.processings.action import *

actionMap = {
    "click": Action.click,
    "inputKeyword": Action.inputKeyword,
    "sendEnter": Action.sendEnter,
    "switchLastTab": Action.switchLastTab,
    "switchTab": Action.switchTab,
    "searchRedirect": Action.searchRedirect,
    'redirect': Action.redirect,
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
        if action not in actionMap:
            return False
        is_success = actionMap[action](driver, xpath, info)
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
            Util.random_sleep(0.3 + interval, 0.5 + interval)
    if False in res:
        raise Exception("预处理脚本失败,失败信息:", scripy_list, res)

