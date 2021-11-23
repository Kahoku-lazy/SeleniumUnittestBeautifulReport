# import smtplib
# from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from enum import Enum, unique

@unique
class BrowserDriver(Enum):
    '''定义支持的浏览器，支持Chrome、Firefox、Ie、Edge'''

    Chrome = 0
    Firefox = 1
    Ie = 2
    Edge = 3

class BoxDriver(object):
    ''' 封装 selenium 工具中的方法 '''

    _base_driver = None
    _browser_driver_path = None

    def __init__(self, brower_type=BrowserDriver.Chrome, by_char=",") -> None:
        ''' 选择浏览器 '''

        self._by_char = by_char             # 定位元素分隔符
        driver = None
        # 选择浏览器
        if brower_type == 0 or brower_type == BrowserDriver.Chrome:
            driver = webdriver.Chrome()
        elif brower_type == 1 or brower_type == BrowserDriver.Firefox:
            driver = webdriver.Firefox()
        elif brower_type == 2 or brower_type == BrowserDriver.Ie:
            driver = webdriver.Ie()
        elif brower_type == 3 or brower_type == BrowserDriver.Edge:
            driver = webdriver.Edge()
        # else:
        #     driver = webdriver.PhantomJS()

        # 浏览器未打开时，抛出异常
        # try:
        #     self._base_driver = driver
        # except Exception:
        #     raise NameError("浏览器{name}打开失败！！！".format(name=brower_type))
        if driver is not None:
            self._base_driver = driver
        else:
            raise NameError("浏览器{name}打开失败！！！".format(name=brower_type))

    
    '''  selenium 自定义定位元素的格式  '''
    def _concert_selector_to_locatot(self, selector):
        """ 自定义定位元素格式, 并将其转化为Selenium 支持的 locator 格式
        定位元素格式： 定位方式标志符,定位元素。
        例如: ID定位： i, xxxx
        """
        if self._by_char not in selector:           # 定位元素无标志符，默认为ID定位方式
            return By.ID, selector

        # 拆分"i, xxx"
        selector_by = selector.split(self._by_char)[0].strip()
        selector_value = selector.split(self._by_char)[1].strip()

        # 定位方法匹配
        if selector_by == "i" or selector_by == "id":
            locator = (By.ID, selector_value)
        elif selector_by == "n" or selector_by == "name":
            locator = (By.NAME, selector_value)
        elif selector_by == "c" or selector_by == "class_name":
            locator = (By.CLASS_NAME, selector_value)
        elif selector_by == "l" or selector_by == "link_text":
            locator = (By.LINK_TEXT, selector_value)
        elif selector_by == "p" or selector_by == "partial_link_text":
            locator = (By.PARTIAL_LINK_TEXT, selector_value)
        elif selector_by == "t" or selector_by == "tag_name":
            locator = (By.TAG_NAME, selector_value)
        elif selector_by == "x" or selector_by == "xpath":
            locator = (By.XPATH, selector_value)
        elif selector_by == "s" or selector_by == "css_selector":
            locator = (By.CSS_SELECTOR, selector_value)
        else:
            raise NameError("Please enter a valid selector of targeting elements.")

        return locator

    def _locator_element(self, selector):
        ''' 单个定位方式 '''

        locator = self._concert_selector_to_locatot(selector)

        if locator is not None:
            return self._base_driver.find_element(*locator)
        else:
            raise NameError("请按格式输入有效的定位元素。")

    def _locator_elements(self, selector):
        """ 复数定位方式"""
        locator = self._concert_selector_to_locatot(selector)

        if locator is not None:
            return self._base_driver.find_elements(*locator)
        else:
            raise NameError("请按格式输入有效的定位元素。")

    ''' 浏览器控制 '''
    def navigate(self,url):
        """ 打开制定的网站 """
        self._base_driver.get(url)

    def maximize_windows(self):
        """ 最大化窗口 """
        self._base_driver.maximize_window()

    def minximize_windows(self):
        """ 最小化窗口 """
        self._base_driver.minimize_window()

    def refresh(self, url=None):
        """ 默认刷新当前页面
        指定页面则以重打开的方式刷新页面。 
        """
        if url is None:
            self._base_driver.refresh()
        else:
            self._base_driver.get(url)

    def button_back(self):
        """ 浏览器后退按钮 """
        self._base_driver.back()

    def button_forward(self):
        """ 浏览器前进按钮 """
        self._base_driver.forward()

    def close_browser(self):
        """ 关闭窗口或者标签页 """
        self._base_driver.close()  

    def quit_driver(self):
        """ 退出驱动 """
        self._base_driver.quit()

    ''' 浏览器页面元素相关操作方法 '''
    def click(self, selector):
        """ 鼠标点击（默认左键） """
        self._locator_element(selector).click()

    # 重复方法, 待删除。
    def click_by_text(self, text):
        """ 通过链接文本点击元素 """
        self._locator_element('p%s' % self._by_char + text).click()

    def button_enter(self, selector):
        """ 敲击回车键 [Enter] """
        self._locator_element(selector).send_keys(Keys.ENTER)

    def type(self, selector, value):
        """ 输入文本 """
        el = self._locator_element(selector)
        el.clear()
        el.send_keys(value)

    def submit(self, selector):
        """ 递交指定表格 """
        self._locator_element(selector).submit()

    def move_to(self, selector):
        """ 将鼠标指针移动到指定元素地点 """
        el = self._locator_element(selector)
        ActionChains(self._base_driver).move_to_element(el).perform()

    def right_click(self, selector):
        """ 用鼠标右键点击 """
        el = self._locator_element(selector)
        ActionChains(self._base_driver).context_click(el).perform()
