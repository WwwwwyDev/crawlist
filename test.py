import crawlist as cl

if __name__ == '__main__':
    button_selector = cl.CssWebElementSelector(pattern='#kkpager > div:nth-child(1) > span.pageBtnWrap > a')
    pager = cl.DynamicPagerNumButton(uri="https://finance.china.com.cn/live.shtml",
                                      button_selector=button_selector)
    selector = cl.CssSelector(pattern='#gkajlb ul')
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()
