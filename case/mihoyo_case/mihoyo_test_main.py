from unittest import TestCase
from seleniumPython3.base.box import BoxDriver
from seleniumPython3.page.mihoyo_page.mihoyo_main_page import MihoyoMainPage

class MihoyoTest(TestCase):

    base_driver = None
    main_page = None

    def setUp(self) -> None:
        # 选择浏览器
        self.base_driver = BoxDriver(3)
        # 调用Page方法
        self.main_page = MihoyoMainPage(self.base_driver)
        # self.main_page.open("https://www.mihoyo.com/?page=product")

    def tearDown(self) -> None:
        self.main_page.quit()

    def test_main(self):

        pass