"""
@Project（项目）: box
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/14
@License:   None
"""
import configparser
import logging
import sys
import time
# 枚举
from enum import Enum, unique
# selenium
import openpyxl as openpyxl
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
# 邮箱
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# 数据
import csv
import yaml
from yaml.loader import Loader

''' 公共方法 '''


@unique
class BrowserDriver(Enum):
    """ 定义支持的浏览器，支持Chrome、Firefox、Ie、Edge """

    Chrome = 0
    Firefox = 1
    Ie = 2
    Edge = 3


class SeleniumCommon(object):
    """封装 selenium 工具中的方法 """
    _base_driver = None
    _browser_driver_path = None

    def __init__(self, brower_type=0, by_char=",") -> None:
        """
        构造方法
        :param brower_type: 枚举浏览器参数
        :param by_char: 间隔符（用于定位元素）
        """

        driver = None
        self._by_char = by_char  # 定位元素分隔符
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

    '''  将自定义的selector转化为(By.ID, value)格式 '''

    def _concert_selector_to_locatot(self, selector):
        """
        自定义定位元素格式, 并将其转化为Selenium 支持的 (By.ID, value)格式
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        if self._by_char not in selector:  # 定位元素无标志符，默认为ID定位方式
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
        """
        选择单个元素
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """
        locator = self._concert_selector_to_locatot(selector)

        if locator is not None:
            return self._base_driver.find_element(*locator)
        else:
            raise NameError("请按格式输入有效的定位元素。")

    def _locator_elements(self, selector):
        """
        选择复数元素
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        locator = self._concert_selector_to_locatot(selector)

        if locator is not None:
            return self._base_driver.find_elements(*locator)
        else:
            raise NameError("请按格式输入有效的定位元素。")

    ''' 浏览器控制 '''

    def navigate(self, url):
        """
        打开网站
        :param url: 网站地址
        :return: None
        """
        self._base_driver.get(url)

    def maximize_windows(self):
        """
        窗口最大化
        :return: None
        """

        self._base_driver.maximize_window()

    def minximize_windows(self):
        """
        窗口最小化
        :return: None
        """

        """ 最小化窗口 """
        self._base_driver.minimize_window()

    def refresh(self, url=None):
        """
        刷新页面
        :param url: 页面网址
        :return: None
        """

        if url is None:
            self._base_driver.refresh()
        else:
            self._base_driver.get(url)

    def button_back(self):
        """
        浏览器 后退
        :return: None
        """

        self._base_driver.back()

    def button_forward(self):
        """
        浏览器 前进
        :return: None
        """

        self._base_driver.forward()

    def close_browser(self):
        """
        关闭窗口或者标签页
        :return: None
        """

        self._base_driver.close()

    def quit_driver(self):
        """
        退出 浏览器驱动
        :return: None
        """

        self._base_driver.quit()

    ''' 浏览器页面元素相关操作方法 '''

    def click(self, selector):
        """
        鼠标点击（默认左键）
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        self._locator_element(selector).click()

    def button_enter(self, selector):
        """
        敲击回车键 [Enter]
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        self._locator_element(selector).send_keys(Keys.ENTER)

    def type(self, selector, value):
        """
        选定输入框  输入文本
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param value: 输入内容
        :return: None
        """

        el = self._locator_element(selector)
        el.clear()
        el.send_keys(value)

    def submit(self, selector):
        """
        递交指定表格
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return:
        """

        self._locator_element(selector).submit()

    def move_to(self, selector):
        """
        将鼠标指针移动到指定元素地点
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        el = self._locator_element(selector)
        ActionChains(self._base_driver).move_to_element(el).perform()

    def right_click(self, selector):
        """
        鼠标右键点击
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        el = self._locator_element(selector)
        ActionChains(self._base_driver).context_click(el).perform()

    def count_elements(self, selector):
        """
        获取复数定位元素的个数
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: int
        """

        """ 数一下元素的个数 """
        els = self._locator_elements(selector)
        return len(els)

    """ 复选框、下拉框操作 """

    def select_by_index(self, selector, index):
        """
        index的方式 点击选择复选框，单选按钮，甚至下拉框
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param index: 标签 下标值（int number）
        :return: None
        """

        el = self._locator_element(selector)
        Select(el).select_by_index(index)

    def select_by_visible_text(self, selector, text):
        """
        text的方式 点击选择复选框，单选按钮，甚至下拉框
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param text: 标签 text 值
        :return: None
        """

        """ text的方式 点击选择复选框，单选按钮，甚至下拉框 """
        el = self._locator_element(selector)
        Select(el).select_by_visible_text(text)

    def select_by_value(self, selector, value):
        """
        value的方式 点击选择复选框，单选按钮，甚至下拉框
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param value: 标签 Value
        :return: None
        """

        el = self._locator_element(selector)
        Select(el).select_by_value(value)

    """ 获取数据 """

    def get_url(self):
        """
        获取当前页面的URL
        :return:  url (string)
        """

        return self._base_driver.current_url

    def get_title(self):
        """
        获取当前页面的标题
        :return:  页面窗口标题
        """

        return self._base_driver.title

    def get_handle(self):
        """
        获取当前窗口的窗口句柄
        :return:
        """

        return self._base_driver.current_window_handle

    def get_selected_text(self, selector):
        """
        获取 Select（下拉框元素）的文本， （不选择下拉框数据则为默认的内容）
        :param selector: 定位方式 （Select标签元素， 例如：ID定位： i, xxxx）
        :return: (string)
        """

        el = self._locator_element(selector)

        """ 不需要括号，加括号会报错:"object is not callable", 鬼知道我是怎么找出来的！！！！
        # selected_opt = Select(el).first_selected_option()
        """
        selected_opt = Select(el).first_selected_option

        return selected_opt.text

    def get_value(self, selector):
        """
        返回元素的 value
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return:
        """

        el = self._locator_element(selector)
        return el.get_attribute("value")

    def get_attribute(self, selector, attribute):
        """
        获取元素属性的值. ‘textContent’: 文本信息；
        'innerHTML'： 元素内全部 html信息； 'outerHTML'： 选择元素的html信息
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param attribute:
        :Usage:  driver.get_attribute("i,el","type")
        :return:
        """

        el = self._locator_element(selector)
        return el.get_attribute(attribute)

    def get_text(self, selector):
        """
        获取元素文本信息
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
         Usage:driver.get_text("i,el")
        :return:
        """

        el = self._locator_element(selector)
        return el.text

    def get_selected(self, selector):
        """
        返回一个元素的选定状态, (适用于 单选框 复选框)
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: True False
        """
        el = self._locator_element(selector)
        return el.is_selected()

    def get_text_list(self, selector):
        """
        根据selector 获取多个元素，取得元素的text 列表
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: list
        """

        el_list = self._locator_elements(selector)

        results = []
        for el in el_list:
            results.append(el.text)

        return results

    """ 判断页面元素"""

    def get_exist(self, selector):
        """
        该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: None
        """

        flag = True
        try:
            self._locator_element(selector)
            return flag
        except:
            flag = False
            return flag

    def get_enabled(self, selector):
        """
        判断页面元素是否可点击
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return: 布尔值 (bool)
        """

        if self._locator_element(selector).is_enabled():
            return True
        else:
            return False

    def get_displayed(self, selector):
        """
        获取要显示的元素，返回的结果为真或假
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        Usage:
        driver.get_display("i,el")
        :return:
        """
        el = self._locator_element(selector)
        return el.is_displayed()

    """ web页面alert警告框 相关处理方法 """

    def accept_alert(self):
        """
        接受 Alert 警告框
        :return: None
        """

        self._base_driver.switch_to.alert.accept()

    def dismiss_alert(self):
        """
        取消 Alert 警告框
        :return: None
        """

        self._base_driver.switch_to.alert.dismiss()

    def get_alert_text(self):
        """
        获取 Alert弹框的文本内容
        :return: None
        """
        text = self._base_driver.switch_to.alert.text
        return text

    """  等待方法 """

    def forced_wait(self, seconds):
        """  强制等待
        :param seconds: 秒 （s）
        :return: None
        """
        time.sleep(seconds)

    def implicitly_wait(self, seconds):
        """
        隐式等待
        :param seconds: 秒 (s)
        """
        self._base_driver.implicitly_wait(seconds)

    def explicitly_wait(self, selector, seconds):
        """
        显式等待（等待某一元素出现的最大时间）
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :param seconds: 最长等待时间，秒 （s）
        :return: None
        """
        locator = self._concert_selector_to_locatot(selector)

        WebDriverWait(self._base_driver, seconds).until(expected_conditions.presence_of_element_located(locator))

    """ 浏览器标签窗口 相关处理方法 """

    def switch_to_frame(self, selector):
        """
        进入 iframe 框架
        :param selector: 定位方式 （例如：ID定位： i, xxxx）
        :return:
        """

        el = self._locator_element(selector)
        self._base_driver.switch_to.frame(el)

    """ 屏幕截图 相关方法"""

    def save_window_snapshot(self, file_name):
        """
        屏幕截图
        :param file_name: 截图保存的路径
        :return: None
        """

        driver = self._base_driver
        driver.save_screenshot(file_name)


class DataCommon(object):

    def csv_read_list(self, file_path):
        """ 读取csV文件中数据，以列表的形式返回。
        :param file_path: 文件路径
        :return: data --  读取到的数据，列表类型。
        """
        data = []
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
        return data

    def csv_read_dict(self, file_path):
        """
        读取csV文件中数据，以字典的形式返回
        :param file_path: 文件路径
        :return: data --  读取到的数据，字典类型
        """
        data = []
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data

    def yaml_read_dict(self, file_path):
        """
        yaml文件读取
        :param file_path: 文件路径
        :return:
        """
        with open(file_path, 'r') as f:
            reader = yaml.load(f.read(), Loader=yaml.Loader)
        return reader

    def excel_read_values(self, excel_path, sheet_name):
        """
        获取表格指定标签页的数据，按行的方式读取。
        :param excel_path: 表格文件路径
        :param sheet_name: 标签名
        :return: 返回读取的时间，生成器类型。
        """
        excel_data = openpyxl.load_workbook(excel_path)[sheet_name]
        values = excel_data.values  # 获取当前工作表的数据（按行获取）

        return values

    def read_config_section(self, config_path, section):
        """
        读指定 section下 option
        :param config_path:  ini文件路径
        :param section: 标签名
        :return: 指定标签下数据（list）（[(key, value),(key, value)]）
        """
        conf = configparser.ConfigParser()  # 创建管理对象
        conf.read(config_path, encoding='utf-8')  # 读数据
        # 读指定 section下数据
        data = conf.items(section)

        return data

    def modify_config(self, config_path, section, value, option="test_path"):
        """
        修改config文件
        :param config_path: ini文件路径
        :param section: 标签名
        :param value: 需修改option的 value（list）（[(key, value),(key, value)]）
        :param option: 需修改的option的 key
        :return:    None
        """
        conf = configparser.ConfigParser()  # 创建管理对象
        conf.read(config_path, encoding='utf-8')  # 读数据

        conf.set(section, option, value)  # 默认只修改路径

        conf.write(open(config_path, "w"))  # 修改文件后需要写入保存


class EmailCommon(object):
    """ 邮箱 发送"""

    def email_attachment(self, report_file):
        """
        配置发送附件测试报告到邮箱
        :param report_file:  报告文件路径
        :return: None
        """

        '''发件相关参数'''

        try:
            # 发件服务器
            smtpserver = 'smtp.qq.com'
            port = 25
            # 更改如下3项即可
            sender = "otaku.acgn@qq.com"  # 你的邮箱
            psw = 'kmafhmdxvwnodgcg'  # 授权码
            receiver = '1003596831@qq.com'  # 收件人邮箱
            msg = MIMEMultipart()
            msg['from'] = sender
            msg['to'] = ';'.join(receiver)
            msg['subject'] = '这个是自动化测试报告'

            '''读取测试报告内容'''
            with open(report_file, 'rb') as rp:
                report_value = rp.read()

            '''正文'''
            body = MIMEText("这是自动化测试报告\n测试邮箱发送", 'html', 'utf8')        # 报告内容，文本格式，编码
            msg.attach(body)

            '''附件'''
            att = MIMEText(report_value, 'base64', 'utf8')
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


class LogCommon(object):
    """ 日志文件 """

    def __init__(self, log_path, logger_level=logging.INFO):
        """
        日志文件配置
        :param log_path:  日志路径
        :param logger_level:  logger(记录器)的日志等级
        """
        self.log_path = log_path
        self.fmts = '[%(asctime)s]-[%(name)s]-[%(filename)s]-[%(lineno)d]-[%(levelname)s]: %(message)s'
        self.datefmts = "%Y/%m/%d %H:%M:%S"

        self.logger = logging.getLogger()
        self.logger.setLevel(logger_level)

    def _create_log_file(self, message, handler_level=logging.INFO):
        """
        新建日志文件， 默认等级 warning
        :param message:  信息
        :param handler_level:  等级
        :return: None
        """

        # 记录器
        fh = logging.FileHandler(filename=self.log_path, mode='a+', encoding='utf8')
        fh.setLevel(handler_level)
        formatter = logging.Formatter(fmt=self.fmts, datefmt=self.datefmts)
        fh.setFormatter(formatter)
        # 添加处理器
        self.logger.addHandler(fh)

        self.logger.info(message)

        self.logger.removeHandler(fh)

        # fh.close()

    def _create_log(self, message, handler_level=logging.INFO):
        """
        新建日志，输出控制台，默认等级 warning
        :param message:  信息
        :param handler_level:  等级
        :return:
        """

        # 记录器
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(handler_level)
        formatter = logging.Formatter(fmt=self.fmts, datefmt=self.datefmts)
        ch.setFormatter(formatter)
        # 添加处理器
        self.logger.addHandler(ch)

        self.logger.info(message)

        self.logger.removeHandler(ch)

    def info(self, message):
        """
        添加信息日志
        :param message: 信息内容
        :return: None
        """
        self._create_log_file(message)
        self._create_log(message)


''' 测试系统的最基础的页面类，是所有其他页面的基类 '''


class BasePage(object):
    """
    Page基类
    """

    basePage_driver = None
    basePage_data = None
    basePage_log = None

    def __init__(self, brower_type=0, by_char=","):
        """
        实例化
        :param brower_type: 浏览器类型
        :param by_char: 间隔符
        """
        self.basePage_driver = SeleniumCommon(brower_type, by_char)
        self.basePage_data = DataCommon()
        # self.basePage_log = LogCommon()

    def open(self, url):
        """
        打开网页后自动最大化窗口
        :param url: 网站地址
        :return: None
        """
        self.basePage_driver.navigate(url)
        self.basePage_driver.maximize_windows()

    def test_login(self):
        """
        登陆 测试代码 （此网站为本地搭建的网站，测试时请更新自己的信息，否则提示错误！
        提示错误！
        提示错误！！！）
        :return: None
        """
        self.basePage_driver.type('i, account', "admin")
        self.basePage_driver.type('n, password', "Admin123")
        self.basePage_driver.click('submit')

    def test_basepage_01(self):
        """
        代码调试  浏览器控件模块代码测试 （此网站为本地搭建的网站，测试时请更新自己的信息，不修改运行绝对会提示错误！
        提示错误！
        提示错误！！！）
        :return: None
        """

        ''' zentaopms_login_url:  禅道URL, 此网站为本人自己搭建的网站， 测试请按需求自己更新其它网站 
        '''
        zentaopms_login_url = r"http://localhost:8081/zentaopms/www/user-login-L3plbnRhb3Btcy93d3cv.html"
        self.open(zentaopms_login_url)

        """ 浏览器控件模块代码测试 """

        # 最小化窗口
        self.basePage_driver.minximize_windows()
        # 等待
        self.basePage_driver.forced_wait(1)
        # 最大化窗口
        self.basePage_driver.maximize_windows()

        # 登陆
        self.basePage_driver.explicitly_wait('account', 10)  # 显式等待
        self.test_login()
        self.basePage_driver.forced_wait(3)

        # 浏览器后退   （新页面标记： 'panel-heading'）
        while True:
            self.basePage_driver.button_back()
            if self.basePage_driver.get_exist('account'):  # get_exist(selector): 判断元素是否存在，存在即返回 True
                break
        self.basePage_driver.forced_wait(3)

        # 刷新页面
        self.basePage_driver.refresh()
        self.basePage_driver.forced_wait(3)

        # 浏览器 前进
        self.basePage_driver.button_forward()
        self.basePage_driver.forced_wait(3)

        # 退出驱动
        self.basePage_driver.forced_wait(5)
        self.basePage_driver.quit_driver()

    def test_basepage_02(self):
        """
        测试代码  ”浏览器页面元素相关操作方法“ 模块代码测试 （此网站为本地搭建的网站，测试时请更新自己的信息，
        不修改运行绝对会提示错误！
        提示错误！！
        提示错误！！！）
        :return:  None
        """

        ''' zentaopms_login_url:  禅道URL, 此网站为本人自己搭建的网站， 测试请按需求自己更新其它网站 
        
        不修改 运行会报错！
        不修改 运行会报错！！
        不修改 运行会报错！！！
                '''
        zentaopms_login_url = r"http://localhost:8081/zentaopms/www/user-login-L3plbnRhb3Btcy93d3cv.html"
        self.open(zentaopms_login_url)

        # 登陆
        self.basePage_driver.explicitly_wait('account', 10)  # 显式等待
        self.test_login()
        self.basePage_driver.forced_wait(3)

        # menu - iframe 框架
        self.basePage_driver.explicitly_wait('appIframe-my', 10)  # 显式等待
        self.basePage_driver.switch_to_frame('appIframe-my')

        # 点击头像
        self.basePage_driver.click('x, //*[@id="userNav"]/li[1]')
        self.basePage_driver.forced_wait(3)
        # 修改主题
        self.basePage_driver.click('x, //*[@id="userNav"]/li[1]/ul/li[8]/a')
        self.basePage_driver.forced_wait(3)
        # 选择主题颜色(赤诚红)
        self.basePage_driver.click('x, //*[@id="userNav"]/li[1]/ul/li[8]/ul/li[4]/a')

        # 搜索框输入文本
        self.basePage_driver.explicitly_wait('globalSearchInput', 10)
        self.basePage_driver.type('globalSearchInput', "Nezuko most lovely")
        self.basePage_driver.forced_wait(3)
        # 回车【enter】
        self.basePage_driver.button_enter('globalSearchInput')

        # iframe
        self.basePage_driver.switch_to_frame("appIframe-search")
        # 鼠标右击
        self.basePage_driver.explicitly_wait('words', 10)
        self.basePage_driver.right_click('words')
        self.basePage_driver.forced_wait(3)

        # 退出驱动
        self.basePage_driver.forced_wait(5)
        self.basePage_driver.quit_driver()

    def test_basepage_03(self):
        """
        测试代码  ” 复选框、下拉框操作“ 模块代码测试 （此网站为本地搭建的网站，测试时请更新自己的信息，
        不修改运行绝对会提示错误！
        提示错误！！
        提示错误！！！）
        :return:  None
        """
        ''' zentaopms_login_url:  禅道URL, 此网站为本人自己搭建的网站， 测试请按需求自己更新其它网站 

                不修改 运行会报错！
                不修改 运行会报错！！
                不修改 运行会报错！！！
                        '''
        zentaopms_login_url = r"http://localhost:8081/zentaopms/www/user-login-L3plbnRhb3Btcy93d3cv.html"
        self.open(zentaopms_login_url)

        # 登陆
        self.basePage_driver.explicitly_wait('account', 10)  # 显式等待
        self.test_login()
        self.basePage_driver.forced_wait(3)

        # 选择模块
        self.basePage_driver.explicitly_wait('x, //*[@id="menuMainNav"]/li[7]/a', 10)  # 显式等待
        self.basePage_driver.click('x, //*[@id="menuMainNav"]/li[7]/a')

        # DevOPs -- iframe
        self.basePage_driver.explicitly_wait('appIframe-devops', 10)  # 显式等待
        self.basePage_driver.switch_to_frame('appIframe-devops')

        # 点击下拉列表
        self.basePage_driver.explicitly_wait('x, //*[@id="aclgroups_chosen"]/div/ul', 10)  # 显式等待

        # DevOPs - 类型 （下拉框操作）  案例一 正确示范
        self.basePage_driver.explicitly_wait('SCM', 10)

        select_text = self.basePage_driver.get_selected_text('SCM')  # 获取下拉框内显示的文本(默认值、或已选定值)
        print("获取下拉框内显示的文本，select_text = ", select_text)

        self.basePage_driver.select_by_value('SCM', 'Git')  # value

        self.basePage_driver.forced_wait(3)
        self.basePage_driver.select_by_visible_text('SCM', 'GitLab')  # text

        self.basePage_driver.forced_wait(3)
        self.basePage_driver.select_by_index('SCM', 0)  # index 从 0 开始计数

        # DevOPs - 分组
        self.basePage_driver.click('x, //*[@id="aclgroups_chosen"]')  # 分组输入框
        self.basePage_driver.click('x, //*[@id="aclgroups_chosen"]/div/ul/li[%d]' % 5)  # 选择

        '''  下拉列表错误示范 ，案例参考 doc - 案例一 '''
        self.basePage_driver.explicitly_wait('c, chosen-results', 10)
        count = self.basePage_driver.count_elements('c, chosen-results')  # 计数
        count_text = self.basePage_driver.get_text_list('c, chosen-results')  # 获取多个元素的 text 内容
        print("分组元素有{}个\n元素文本{}".format(count, count_text))
        # # 下拉选数据
        # self.basePage_driver.select_by_index('c, chosen-results', 1)

        # 退出驱动
        self.basePage_driver.forced_wait(5)
        self.basePage_driver.quit_driver()

    def test_basepage_04(self):
        """
                测试代码  ” 获取数据 、判断数据、屏幕截图“ 等模块代码测试 （此网站为本地搭建的网站，测试时请更新自己的信息，
                不修改运行绝对会提示错误！
                提示错误！！
                提示错误！！！）
                :return:  None
                """
        init_url = self.basePage_driver.get_url()  # 获取 打开浏览器时 网址

        init_handle = self.basePage_driver.get_handle()  # 获取 打开浏览器时 窗口句柄

        ''' zentaopms_login_url:  禅道URL, 此网站为本人自己搭建的网站， 测试请按需求自己更新其它网站 

                不修改 运行会报错！
                不修改 运行会报错！！
                不修改 运行会报错！！！
                        '''
        zentaopms_login_url = r"http://localhost:8081/zentaopms/www/user-login-L3plbnRhb3Btcy93d3cv.html"
        self.open(zentaopms_login_url)

        pms_url = self.basePage_driver.get_url()  # 获取禅道页面 网址

        pms_title = self.basePage_driver.get_title()  # 获取登陆页面的 标签页名称

        pms_handle = self.basePage_driver.get_handle()  # 获取 窗口句柄

        # 嫌弃元素定位太长
        password = 'x, //*[@id="loginPanel"]/div/div[2]/form/table/tbody/tr[2]/th'
        username = 'x, //*[@id="loginPanel"]/div/div[2]/form/table/tbody/tr[1]/th'

        pms_password_text = self.basePage_driver.get_text(password)  # 密码
        self.basePage_driver.click('account')
        if self.basePage_driver.get_selected('account'):
            # ‘textContent’: 文本信息； 'innerHTML'： 元素内全部 html信息； 'outerHTML'： 选择元素的html信息
            pms_password_type = self.basePage_driver.get_attribute(password, 'textContent')

        """   定位标签，应该需要选择 select标签（未验证结论，但不选用会报错）
        # 正确用法 在 test_basePage_03 中 下拉框元素获取 （以下为错误示范）
        # pms_password_selectend_text = self.basePage_driver.get_selected_text(password)
        """

        # pms_username_text = self.basePage_driver.get_text(username)  # 用户名

        if self.basePage_driver.get_exist(password):  # 判断元素是否存在
            self.test_login()
            self.basePage_driver.forced_wait(3)

        try:
            if self.basePage_driver.get_enabled('submit'):  # 判断元素是否可点击
                self.basePage_driver.click('submit')
                self.basePage_driver.forced_wait(3)

            alert_text = self.basePage_driver.get_alert_text()  # 获取弹窗文本
            # self.basePage_driver.accept_alert()                         # 确认
            self.basePage_driver.dismiss_alert()  # 取消
        except:
            alert_text = "None"
            self.basePage_driver.save_window_snapshot("../../doc/img.png")

        # 打印信息
        get_data = f"""\000打开浏览器时：\n\t网址：{init_url}\n\t窗口句柄：{init_handle}\n\000打开禅道登陆页面时：\
                            \n\t网址：{pms_url}\n\t页面窗口标签名：{pms_title}\n\t窗口句柄：{pms_handle}\n\t获取指定元素文本：\
                            {pms_password_text}\n\tattribute(属性值-- type): {pms_password_type}\n\000 获取alert弹窗文本：\
                            {alert_text}"""
        print(get_data.format(init_url=init_url, init_handle=init_handle,
                              pms_url=pms_url, pms_title=pms_title, pms_handle=pms_handle,
                              pms_password_text=pms_password_text, pms_password_type=pms_password_type,
                              alert_text=alert_text))

        # 退出驱动
        self.basePage_driver.forced_wait(5)
        self.basePage_driver.quit_driver()

    def test_is_selected(self):
        """
                测试代码  ” 获取数据 、判断数据、屏幕截图“ 等模块代码测试 （此网站为本地搭建的网站，测试时请更新自己的信息，
                不修改运行绝对会提示错误！
                提示错误！！
                提示错误！！！）
                :return:  None
                """
        ''' zentaopms_login_url:  禅道URL, 此网站为本人自己搭建的网站， 测试请按需求自己更新其它网站 

                不修改 运行会报错！
                不修改 运行会报错！！
                不修改 运行会报错！！！
                        '''
        zentaopms_login_url = r"http://localhost:8081/zentaopms/www/user-login-L3plbnRhb3Btcy93d3cv.html"
        self.open(zentaopms_login_url)

        self.basePage_driver.explicitly_wait('n, keepLogin[]', 10)
        if not self.basePage_driver.get_selected('n, keepLogin[]'):  # 判断 保持登陆单选框是否勾选
            print("未选中")
            self.basePage_driver.click('n, keepLogin[]')
            self.basePage_driver.forced_wait(6)

        if self.basePage_driver.get_selected('n, keepLogin[]'):
            print("已选中")

        self.basePage_driver.move_to('c, btn')

        # 退出驱动
        self.basePage_driver.forced_wait(5)
        self.basePage_driver.quit_driver()


# 调试入口
if __name__ == '__main__':
    """ 测试代码： 为什么要测试？
        自己写的bug？自己写的BUG! 自己写的BUg!!!
        才多少代码，找bug累死………………（心塞）"""
    # BasePage().test_basepage_03()
    BasePage().test_is_selected()
