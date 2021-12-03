from seleniumPython3.base.box import BasePage, DataProcessing, BoxDriver


class MihoyoMainPage(BasePage):
    
    # file_path = "./data/mihoyou_elements.yaml"
    # MAIN_ELEMENTS = DataProcessing().read_yaml(file_path)["MAIN_PAGE"]

    # def main_select_menu(self, menu):
    #     """ 米哈游官网主页菜单 """
    #     # python3.10 --> match-case
    #
    #     if menu == "首页":
    #         self.base_driver.click(self.MAIN_ELEMENTS["首页"])
    #     elif menu == "产品信息":
    #         self.base_driver.click(self.MAIN_ELEMENTS["首页"])
    #     elif menu == "了解我们":
    #         self.base_driver.click(self.MAIN_ELEMENTS["首页"])
    #     elif menu == "加入我们":
    #         self.base_driver.click(self.MAIN_ELEMENTS["首页"])
    #     elif menu == "新闻动态":
    #         self.base_driver.click(self.MAIN_ELEMENTS["首页"])

    def quit(self):
        """ 直接退出驱动 """
        self.base_driver.quit_driver()

    def test(self):

        self.open("https://www.mihoyo.com/?page=product")   # 米哈官网

        # self.main_select_menu("首页")

if __name__ == "__main__":

    MihoyoMainPage(BoxDriver(3)).test()

    pass
