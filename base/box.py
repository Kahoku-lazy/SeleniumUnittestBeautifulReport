import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
# 枚举类型
from enum import Enum, unique
# 邮箱
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 数据处理
import csv
import xlrd
import yaml
from yaml.loader import Loader

''' 浏览器类型 '''
@unique
class BrowserDriver(Enum):
    '''定义支持的浏览器，支持Chrome、Firefox、Ie、Edge'''

    Chrome = 0
    Firefox = 1
    Ie = 2
    Edge = 3

''' 公共方法 '''
class BoxDriver(object):
    ''' 封装 selenium 工具中的方法 '''

    _base_driver = None
    _browser_driver_path = None

    def __init__(self, brower_type=3, by_char=",") -> None:
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

    # # 重复方法, 可删除。
    # def click_by_text(self, text):
    #     """ 通过链接文本点击元素 """
    #     self._locator_element('p%s' % self._by_char + text).click()

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

    def count_elements(self, selector):
        """ 数一下元素的个数 """
        els = self._locator_elements(selector)
        return len(els)

    def drag_element(self, source, target):
        """ 拖拽元素 
        将目标元素(source) 拖拽到 指定位置(target)"""
        el_source = self._locator_element(source)
        el_target = self._locator_element(target)

        if self._base_driver.w3c:
            ActionChains(self._base_driver).drag_and_drop(el_source, el_target).perform()
        else:
            ActionChains(self._base_driver).click_and_hold(el_source).perform()
            ActionChains(self._base_driver).move_to_element(el_target).perform()
            ActionChains(self._base_driver).release(el_target).perform()

    def lost_focus(self):
        """ 当前元素丢失焦点
        :return:
        """
        ActionChains(self._base_driver).key_down(Keys.TAB).key_up(Keys.TAB).perform()

    """ 复选框、下拉框操作 """
    def select_by_index(self, selector, index):
        """ index的方式 点击选择复选框，单选按钮，甚至下拉框 """
        el = self._locate_element(selector)
        Select(el).select_by_index(index)

    def select_by_visible_text(self, selector, text):
        """ text的方式 点击选择复选框，单选按钮，甚至下拉框 """
        el = self._locate_element(selector)
        Select(el).select_by_visible_text(text)

    def select_by_value(self, selector, value):
        """ value的方式 点击选择复选框，单选按钮，甚至下拉框 """
        el = self._locate_element(selector)
        Select(el).select_by_value(value)

    """ 获取数据 """
    def get_data(self):
        '''获取浏览器相应的数据'''
        # 获取当前页面的URL
        browser_url = self._base_driver.current_url
        # 获取当前页面的标题
        browser_title = self._base_driver.title
        # 获取当前窗口的窗口句柄
        browser_handle = self._base_driver.current_window_handle

        return (browser_url, browser_title, browser_handle)

    # # 功能重复 可删除    
    # def get_title(self):
    #     ''' 获取 窗口标题. '''
    #     return self._base_driver.title
    # # 功能重复 可删除  
    # def get_url(self):
    #     """获取当前页面的URL地址"""
    #     return self._base_driver.current_url

    def get_selected_text(self, selector):
        """ 获取 Select 元素的选择的内容
        :param selector: 选择字符 "i, xxx"
        :return: 字符串
        """
        el = self._locate_element(selector)
        selected_opt = Select(el).first_selected_option()
        return selected_opt.text

    def get_value(self, selector):
        """ 返回元素的 value
        :param selector: 定位字符串
        :return:
        """
        el = self._locate_element(selector)
        return el.get_attribute("value")

    def get_attribute(self, selector, attribute):
        """ 获取元素属性的值.
        Usage:
        driver.get_attribute("i,el","type")
        """
        el = self._locate_element(selector)
        return el.get_attribute(attribute)

    def get_text(self, selector):
        """ 获取元素文本信息
        Usage:
        driver.get_text("i,el")
        """
        el = self._locate_element(selector)
        return el.text

    def get_selected(self, selector):
        """ 返回一个网站的选定状态
        :param selector: selector to locate
        :return: True False
        """
        el = self._locate_element(selector)
        return el.is_selected()

    def get_text_list(self, selector):
        """ 根据selector 获取多个元素，取得元素的text 列表
        :param selector:
        :return: list
        """

        el_list = self._locate_elements(selector)

        results = []
        for el in el_list:
            results.append(el.text)

        return results

    """ 判断页面元素"""
    def get_exist(self, selector):
        ''' 该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
        :param self:
        :param selector: 元素定位，如'id,account'
        :return: 布尔值
        '''
        flag = True
        try:
            self._locate_element(selector)
            return flag
        except:
            flag = False
            return flag

    def get_enabled(self, selector):
        ''' 判断页面元素是否可点击
        :param selector: 元素定位
        :return: 布尔值
        '''
        if self._locate_element(selector).is_enabled():
            return True
        else:
            return False

    def get_displayed(self, selector):
        """ 获取要显示的元素，返回的结果为真或假
        Usage:
        driver.get_display("i,el")
        """
        el = self._locate_element(selector)
        return el.is_displayed()

    """ web页面alert警告框 相关处理方法 """

    def accept_alert(self):
        ''' 接受警告框. '''
        self._base_driver.switch_to.alert.accept()

    def dismiss_alert(self):
        ''' 取消可用的警报.'''
        self._base_driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        ''' 获取alert 弹框的文本'''
        text = self._base_driver.switch_to.alert.text
        return text

    """  等待方法 """
    def forced_wait(self, seconds):
        """  强制等待
        :param seconds:
        :return:
        """
        time.sleep(seconds)

    def implicitly_wait(self, seconds):
        """ 隐式等待
        :param seconds 等待时间 秒
        """
        self._base_driver.implicitly_wait(seconds)

    def explicitly_wait(self, selector, seconds):
        """ 显式等待
        :param selector: 定位字符
        :param seconds: 最长等待时间，秒
        :return:
        """
        locator = self._concert_selector_to_locator(selector)

        WebDriverWait(self._base_driver, seconds).until(expected_conditions.presence_of_element_located(locator))

    """ 浏览器标签窗口 相关处理方法 """

    def switch_to_frame(self, selector):
        """ 切换到指定的窗口."""
        el = self._locate_element(selector)
        self._base_driver.switch_to.frame(el)

    def switch_to_default(self):
        """
        Returns the current form machine form at the next higher level.
        """
        self._base_driver.switch_to.default_content()

    def switch_to_window_by_title(self, title):

        for handle in self._base_driver.window_handles:
            self._base_driver.switch_to.window(handle)
            if self._base_driver.title == title:
                break

            self._base_driver.switch_to.default_content()

    def open_new_window(self, selector):
        ''' 打开新窗口，并切换手柄到新打开的窗口  '''
        original_windows = self._base_driver.current_window_handle
        el = self._locate_element(selector)
        el.click()
        all_handles = self._base_driver.window_handles
        for handle in all_handles:
            if handle != original_windows:
                self._base_driver._switch_to.window(handle)


    """ 屏幕截图 相关方法"""
    def save_window_snapshot(self, file_name):
        """ 保存屏幕截图
        :param file_name: the image file name and path
        :return:
        """
        driver = self._base_driver
        driver.save_screenshot(file_name)

    def save_window_snapshot_by_io(self):
        """ 保存截图为文件流
        :return:
        """
        return self._base_driver.get_screenshot_as_base64()

    def save_element_snapshot_by_io(self, selector):
        """ 控件截图
        :param selector:
        :return:
        """
        el = self._locate_element(selector)
        return el.screenshot_as_base64

    """ cookies 相关方法 """

    def clear_all_cookies(self):
        """  驱动初始化后，清除浏览器所有的cookies。
        :return:  /
        """
        self._base_driver.delete_all_cookies()

    def add_dict_cookies(self, cookie_dict):
        """  按字典的格式添加cookie，如果cookie已存在，则先删除后添加。
        :param cookie_dict:
        :return:
        """
        cookie_name = cookie_dict["name"]
        cookie_value = self._base_driver.get_cookie(cookie_name)

        if cookie_value is not None:
            self._base_driver.delete_cookie(cookie_name)
        self._base_driver.add_cookie(cookie_dict)

    def remove_name_cookies(self, name):
        """  删除指定name的cookie。
        :param name:
        :return: /
        """
        old_cookies_value = self._base_driver.get_cookie(name)

        if old_cookies_value is not None:
            self._base_driver.delete_cookie(name)

class DataProcessing(object):

    def read_csv(self, file_path):
        """ 列表方式读取 """
        data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        return data

    def read_dict_csv(self, file_path):
        """ 字典方式读取, 以数组方式返回 """
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def read_yaml(self, file_path):
        """ yaml文件读取 """
        with open(file_path, 'r') as f:
            reader = yaml.load(f.read(), Loader=yaml.Loader)
        return reader

    # def read_xls(self, file_path):
    #     """ 只支持打开xls表格 """
    #     data_list = []
    #     data_dict = {}

    #     xls = xlrd.open_workbook(file_path)
    #     for i in range(len(xls.sheets())):
    #         data_list.append((xls.sheets()[i].name, xls.sheets()[i].ncols, xls.sheets()[i].nrows))          # 标签页
    #         # print("data_list: ", data_list)
    #         # sheet1_name = sheet.name   
    #         # sheet1_cols = sheet1.ncols  
    #         # sheet1_nrows = sheet1.nrows
    #         # print('Sheet1 Name: %s\nSheet1 cols: %s\nSheet1 rows: %s' % (sheet1_name, sheet1_cols, sheet1_nrows))
    #     # data_dict["label"] = data_list
    #     # sheet1_nrows4 = sheet1.row_values(4)    # 行
    #     # sheet1_cols2 = sheet1.col_values(2)     # 列
    #     # """del list[:]、 ls*= 0、 ls=[]"""
    #     # data_list.clear()
    #         cell = xls.sheets()[i].get_rows()
    #         for row in cell:
    #             pass

class Email(object):
    """ 邮箱 发送"""
    def email_attachment(self, report_file):
        '''配置发送附件测试报告到邮箱'''
        '''发件相关参数'''

        try:
            # 发件服务器
            smtpserver = 'smtp.163.com'
            port = 25
            # 更改如下3项即可
            sender = '你的邮箱'
            psw = '你的密码'
            receiver = '收件人'
            msg = MIMEMultipart()
            msg['from'] = sender
            msg['to'] = ';'.join(receiver)
            msg['subject'] = '这个是zentao项目自动化测试报告主题'

            '''读取测试报告内容'''
            with open(report_file, 'rb') as rp:
                zentao_mail_body = rp.read()

            '''正文'''
            body = MIMEText(zentao_mail_body, 'html', 'utf8')
            msg.attach(body)

            '''附件'''
            att = MIMEText(zentao_mail_body, 'base64', 'utf8')
            att['Content-Type'] = 'application/octet-stream'
            att['Content-Disposition'] = 'attachment;filename = "%s"' % report_file
            msg.attach(att)

            '''发送邮件'''
            smtp = smtplib.SMTP()
            smtp.connect(smtpserver, port)
            smtp.login(sender, psw)
            smtp.sendmail(sender, receiver.split(';'), msg.as_string())  # 发送
            smtp.close()
            print("邮件发送成功!")

        except Exception as e:
            print(e)
            print("邮件发送失败!")


''' 测试系统的最基础的页面类，是所有其他页面的基类 ''' 
class BasePage(object):

    base_driver = None

    def __init__(self, driver: BoxDriver):
        """  构造方法
        :param driver: 指定了参数类型，BoxDriver
        :param logger:
        """
        self.base_driver = driver

    def open(self, url):
        """   打开页面
        :param url: 页面链接地址
        """
        self.base_driver.navigate(url)
        # self.base_driver.maximize_window()
        self.base_driver.forced_wait(2)

# 调试入口
if __name__=='__main__':

    dt = DataProcessing()

    bp = BasePage()
    
    # print("读取的数据：", dt.read_xls("xls_exercise.xls"))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    pass