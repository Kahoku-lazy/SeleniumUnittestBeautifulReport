"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
from SeleniumUnittestBeautifulReport.base.box import BasePage


class LoginPage(BasePage):

    def input_username(self, username="admin"):
        """
        输入用户名
        :param username: 用户名
        :return: None
        """
        self.basePage_driver.type('i, account', username)

    def input_password(self, password="Admin123"):
        """
        输入密码
        :param password: 密码
        :return: None
        """
        self.basePage_driver.type('n, password', password)

    def login_submit(self):
        """
        点击登陆（登陆按钮）
        :return: None
        """
        self.basePage_driver.click('submit')

    def keep_login(self):
        """
         保持登陆选项
        :return: None
        """
        self.basePage_driver.click('n, keepLogin[]')

    def forget_password(self):
        """
        忘记密码
        :return: None
        """
        self.basePage_driver.click('x, //*[@id="loginPanel"]/div/div[2]/form/table/tbody/tr[4]/td[2]/a')

    def change_language(self, language):
        """
        选择界面语言
        :param language: 语言
        :return: None
        """
        index = None
        if language == "English" or language == "英语":
            index = 2
        elif language == "zh-hant" or language == "繁骵" or language == "繁体":
            index = 1
        elif language == "Chinese" or language == "简体":
            index = 0
        if index is not None:
            self.basePage_driver.select_by_index('langs', index)
        else:
            raise "language参数错误"

    def login_page(self):
        """
        登陆禅道
        :return: None
        """
        self.input_username()
        self.input_password()
        self.login_submit()
