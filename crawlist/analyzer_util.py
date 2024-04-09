import re
import random
import time
# import requests as req
# from bs4 import BeautifulSoup as BS
import parsel
from datetime import datetime


class AnalyzerUtil:
    """
    网页分析工具类
    """

    # @staticmethod
    # def get_html(url: str) -> str:
    #     try:
    #         headers = {
    #             "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
    #                           "Chrome/70.0.3538.77 Safari/537.36"
    #         }
    #         proxies = {
    #             'http': "",
    #             'https': ""
    #         }
    #         r = req.get(url, headers=headers, proxies=proxies)
    #         r.raise_for_status()
    #         r.encoding = r.apparent_encoding
    #         return r.text
    #     except Exception:
    #         return ""

    # @staticmethod
    # def get_website_latency(url):
    #     try:
    #         start_time = time.time()  # 请求发送前的时间
    #         response = req.get(url)
    #         end_time = time.time()  # 请求返回后的时间

    #         # 计算网络延迟
    #         latency = end_time - start_time
    #         # print(f"网络延迟：{latency * 1000} 毫秒")

    #         return latency, response.status_code
    #     except req.exceptions.RequestException as e:
    #         return 0.8, 500

    # 选择html元素
    selector_rules = {"xpath", "css", "regExp", "jsPath"}
    @staticmethod
    def html_selector(html: str, rule: str, selector: str) -> list:
        """
        根据规则解析html文本内容
        :param html: html文本
        :param rule: 解析规则（"xpath", "css", "regExp", "jsPath"）
        :param selector: 选择器
        :return:
        """
        assert rule in AnalyzerUtil.selector_rules
        html = AnalyzerUtil.html_replace_str(html)  # 清洗html文本
        res = []
        if rule == "xpath":
            # select = etree.HTML(html, etree.HTMLParser())
            # res_xpath = select.xpath(selector)
            # for e in res_xpath:
            #     res.append(etree.tostring(e, pretty_print=True, encoding='unicode'))
            p_selector = parsel.Selector(text=html)
            res = p_selector.xpath(selector).getall()
        elif rule == "css":
            # select = BS(html, features="lxml")
            # res_bs = select.select(selector)
            # for e in res_bs:
            #     res.append(e.prettify())
            p_selector = parsel.Selector(text=html)
            res = p_selector.css(selector).getall()
        elif rule == "regExp":
            # pattern = re.compile(selector)
            # res = pattern.findall(html)
            p_selector = parsel.Selector(text=html)
            res = p_selector.re(selector)
        elif rule == "jsPath":
            # Node.js脚本，用于解析HTML并获取元素
            p_selector = parsel.Selector(text=selector)
            selector_res = p_selector.re('("(.*)")')
            if len(selector_res) == 0:
                selector_res = selector
            else:
                selector_res = selector_res[0]
            p_selector = parsel.Selector(text=html)
            res = p_selector.css(selector_res).getall()
            # html = BS(html, features="lxml").prettify()
            # node_script = """
            #     const jsdom = require('jsdom');
            #     const { JSDOM } = jsdom;
            #     var htmlContent = `%s`
            #     const dom = new JSDOM(htmlContent);
            #     function getElement() {
            #         let nodelist = dom.window.%s
            #         if (nodelist.length === undefined){
            #             return [nodelist.outerHTML]
            #         }
            #         let res = Array()
            #         for(let i = 0; i < nodelist.length ; i++){
            #             res.push(nodelist[i].outerHTML)
            #         }
            #         return res
            #     }
            # """%(html, selector)
            # print(node_script)
            # context = execjs.get()
            # ctx = context.compile(node_script)
            # res = ctx.call("getElement")
        return res

    @staticmethod
    def url_format(url: str, old_text, new_text: str) -> str:
        """
        替换url中的字符，主要是为了替换%v和%s
        :param url: url字符串
        :param old_text: 旧文本
        :param new_text: 新文本
        :return:
        """
        return url.replace(old_text, new_text)

    @staticmethod
    def random_sleep(start, end):
        """
        随机延时
        :param start: 范围左界
        :param end: 范围右界
        :return:
        """
        # 产生一个start到end之间的随机小数
        random_delay = random.uniform(start, end)
        # 延时,拟人行为
        time.sleep(random_delay)

    judge_nextPage_button_texts = {"下一页", "下页", ">", "》"}

    @staticmethod
    def judge_next_page_button(element_text: str) -> bool:
        for e in AnalyzerUtil.judge_nextPage_button_texts:
            if e in element_text:
                return True
        return False

    @staticmethod
    def data_work(data_list: list, rule: str, data_list_rules_mp: dict) -> dict:
        if rule == 'xpath':
            root = "//" + \
                   re.findall(r"<([A-Za-z0-9]{1,})(>|\s)",
                              data_list[0])[0][0] + "/"
            for k in data_list_rules_mp.keys():
                if data_list_rules_mp[k] != "":
                    data_list_rules_mp[k] = root + data_list_rules_mp[k]
        res = {}
        for key, pattern in data_list_rules_mp.items():
            res[key] = []
            if pattern != "":
                for e in data_list:
                    select = AnalyzerUtil.html_selector(e, rule, pattern)
                    if len(select) > 0:
                        res[key].append(select[0])
                    else:
                        res[key].append("")
            else:
                for _ in range(len(data_list)):
                    res[key].append("")
        return res

    filter_set = {"\n", "\r", "\t", "<br>"}

    @staticmethod
    def html_filter(html: str) -> str:
        # 去除html中无用信息
        result = ""
        i = 0
        while i < len(html):
            flag = True
            for e in AnalyzerUtil.filter_set:
                if html[i:i + len(e)] == e:
                    i += len(e)
                    flag = False
            if flag:
                result += html[i]
                i += 1
        return result

    @staticmethod
    def html_replace_str(html: str) -> str:
        # 去除html中无用信息
        html = html.replace("\n", '')
        html = html.replace("\r", '')
        html = html.replace("\t", '')
        html = html.replace("<br>", '')
        return html

    @staticmethod
    def deal_format_date(date_str: str):
        # 日期处理
        if date_str == "刚刚":
            return [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), 1]
        if re.findall("秒前", date_str):
            num = re.search("\\d{1,2}", date_str).group()
            return [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - float(int(num) * 1))), 1]
        if re.findall("分钟前", date_str):
            num = re.search("\\d{1,2}", date_str).group()
            return [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - float(int(num) * 60))), 1]
        if re.findall("小时前", date_str):
            num = re.search("\\d{1,2}", date_str).group()
            return [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - float(int(num) * 3600))), 1]
        if re.findall("昨天", date_str):
            day = time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(time.time() - 86400))
            date_time = day
            return [date_time, 1]
        if re.findall("前天", date_str):
            day = time.strftime("%Y-%m-%d %H:%M:%S",
                                time.localtime(time.time() - 2 * 86400))
            date_time = day
            return [date_time, 1]
        if re.findall("天前", date_str):
            num = re.search("\\d{1,2}", date_str).group()
            return [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - float(int(num) * 86400))), 1]

        date_str = date_str.strip()
        # date_str = date_str.replace('- ', '-')
        date_str = date_str.replace(', ', '-')
        date_str = date_str.replace('年', '-')
        date_str = date_str.replace('月', '-')
        date_str = date_str.replace(' 日', '')
        date_str = date_str.replace('日', '')
        date_str = date_str.replace('/n', '')
        date_str = date_str.replace('/', '-')
        date_str = date_str.replace('\\', '-')
        date_str = date_str.replace('.', '-')
        date_str = date_str.replace('时', ':')
        date_str = date_str.replace('分', ':')
        date_str = date_str.replace('秒', '')
        date_str = date_str.replace('\n', '')
        date_str = date_str.replace('- ', '-')
        date_str = date_str.replace(' -', '-')

        # date_str = date_str[0:10]
        if not date_str:
            format_date = '1970-01-01 00:00:00'
            return [format_date, 2]
        if date_str.count("-") == 1:
            if "02-29" in date_str:
                date_str = date_str.replace(
                    "02-29", str(datetime.now().year) + "-02-29")
            elif "2-29" in date_str:
                date_str = date_str.replace(
                    "2-29", str(datetime.now().year) + "-02-29")
        try:
            date_str = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
            format_date = date_str.strftime("%Y-%m-%d %H:%M") + ":00"
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%m-%d")
            now = datetime.now()
            year = now.year
            format_date = year + "-" + date_str.strftime("%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%m-%d-%Y")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%Y-%m-%d")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%B %d,%Y")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%A, %B %d, %Y")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%A, %b %d, %Y %I:%M%p")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%Y%m-%d%H:%M:%S")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%Y%m-%d")
            format_date = date_str.strftime("%Y-%m-%d")
            h = random.randint(10, 23)
            m = random.randint(10, 59)
            s = random.randint(10, 59)
            format_date = format_date + f" {h}:{m}:{s}"
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%A, %d %B %Y")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%B- %d-%Y %H:%M")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%H:%M %Y-%m-%d")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%d %b-%Y %H:%M")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%B %d,%Y")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%d-%b-%Y")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%a %d %b %Y // %H:%M UTC")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            return [format_date, 1]
        except:
            pass

        try:
            date_str = datetime.strptime(date_str, "%m-%d %H:%M")
            format_date = date_str.strftime("%Y-%m-%d %H:%M:%S")
            current_year = datetime.now().year
            format_date = (str(current_year) + format_date[4:])
            return [format_date, 1]
        except:
            pass

        return ['1970-01-01 00:00:00', 2]

    @staticmethod
    def selector_xpath_text(html, craw_rule):
        selector = parsel.Selector(text=html)
        xpath_obj = selector.xpath(f"{craw_rule}")
        craw_arr = re.findall(f"text\(\)", f"{craw_rule}")
        if craw_arr:
            str_arr = xpath_obj.getall()
        else:
            str_arr = xpath_obj.xpath(".//text()").getall()

        deal_arr = [tmp_str for tmp_str in str_arr if tmp_str.strip()]

        flag = "/n"
        str1 = flag.join(deal_arr)

        return str1

    @staticmethod
    def selector_css_text(html, craw_rule):
        selector = parsel.Selector(html)
        css_obj = selector.css(f"{craw_rule}")
        craw_arr = re.findall(f"text\(\)", f"{craw_rule}")
        if craw_arr:
            str_arr = css_obj.getall()
        else:
            str_arr = css_obj.xpath(".//text()").getall()

        deal_arr = [tmp_str for tmp_str in str_arr if tmp_str.strip()]

        flag = "/n"
        str1 = flag.join(deal_arr)

        return str1

    @staticmethod
    def get_inner_text(html: str):
        # 获取节点中的文字信息
        selector = parsel.Selector(html)
        l = selector.xpath(".//text()").getall()
        return "".join(l)

    @staticmethod
    def get_inner_text2(html: str):
        # 获取节点中的文字信息，以空格分隔
        selector = parsel.Selector(html)
        l = selector.xpath(".//text()").getall()
        return " ".join(l)

    # @staticmethod
    # def get_attribute(html: str, attr: str):
    #     # 获取节点中的属性内容
    #     if not html:
    #         return ""
    #     soup = BS(html, 'html.parser').select_one("*")
    #     res = soup.get(attr)
    #     if isinstance(res, list):
    #         return res[0]
    #     return res

    @staticmethod
    def fix_relative_url(baseurl: str, relative: str) -> str:
        # 处理相对路径
        baseurl = baseurl.strip()
        relative = relative.strip()
        if not baseurl.endswith('/'):
            baseurl += '/'
        if relative.startswith('/'):
            relative = relative[1:]
        elif relative.startswith('../'):
            while relative.startswith('../'):
                relative = relative[3:]
        elif relative.startswith('./'):
            while relative.startswith('./'):
                relative = relative[2:]
        return baseurl + relative

