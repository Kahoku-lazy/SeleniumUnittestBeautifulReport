"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
from SeleniumUnittestBeautifulReport.page.login_page import LoginPage


class MainPage(LoginPage):

    def main_iframe(self):
        """
        进入 主页菜单 iframe 框架
        :return: None
        """
        self.basePage_driver.explicitly_wait('appIframe-my', 10)  # 显式等待
        self.basePage_driver.switch_to_frame('appIframe-my')  # menu 框架

    def menu(self, menu):
        """
        选择主页侧面菜单
        :param menu: 菜单名
        :return: None
        """
        index = None
        if menu == "地盘":
            index = 1
        elif menu == "项目集":
            index = 2
        elif menu == "产品":
            index = 3
        elif menu == "项目":
            index = 4
        elif menu == "执行":
            index = 5
        elif menu == "测试":
            index = 6
        elif menu == "devOps":
            index = 7
        elif menu == "文档":
            index = 8
        elif menu == "组织":
            index = 9
        elif menu == "统计":
            index = 10
        elif menu == "后台":
            index = 11

        if index is not None:
            self.basePage_driver.click('x, //*[@id="menuMainNav"]/li[%d]/a' % index)
        else:
            raise "menu参数错误"


class DevOpsPage(MainPage):

    def devops_iframe(self):
        """
        进入 devOps iframe 框架
        :return:
        """
        self.basePage_driver.explicitly_wait('appIframe-devops', 10)  # 显式等待
        self.basePage_driver.switch_to_frame('appIframe-devops')  # devOps iframe

    def repository_type(self, type):
        """
        选择版本库类型
        :param type: 类型名
        :return: None
        """
        value = None
        if type == "Git":
            value = type
        elif type == "GitLab":
            value = type
        elif type == "Subversion":
            value = type

        if value is not None:
            self.basePage_driver.select_by_value('SCM', value)  # value
        else:
            raise "参数错误：版本库无此类型"

    def repository_group(self, group):
        """
        选择版本库分组
        :param group: 所属分组
        :return: None
        """
        index = None
        self.basePage_driver.click('x, //*[@id="aclgroups_chosen"]')  # 分组输入框
        if group == "管理员":
            index = 1
        elif group == "研发":
            index = 2
        elif group == "测试":
            index = 3
        elif group == "项目经理":
            index = 4
        elif group == "产品经理":
            index = 5
        elif group == "研发主管":
            index = 6
        elif group == "产品主管":
            index = 7
        elif group == "测试主管":
            index = 8
        elif group == "高层管理":
            index = 9
        elif group == "其他":
            index = 10

        if index is not None:
            self.basePage_driver.click('x, //*[@id="aclgroups_chosen"]/div/ul/li[%d]' % index)  # 选择
        else:
            raise "参数错误：无此分组！"

    def input_names(self, name):
        """
        输入名称
        :param name: 名称
        :return: None
        """
        self.basePage_driver.type('name', name)
