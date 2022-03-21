"""
@Project（项目）: None
@Author（作者）: 刘星宇
@Data（时间）: 2022/03/20
@License:   None
"""
import os

from SeleniumUnittestBeautifulReport.base.box import DataCommon


class FilePath:
    """ 文件 或数据 路径 """

    def __init__(self):
        """ 文件的绝对路径 """
        self.base_data = DataCommon()   # 实例化

        self.path = os.path.dirname(os.path.realpath(__file__))
        self.runner_path = os.path.dirname(os.path.realpath("../runner/config/runner_config.ini"))
        self.runner_path = os.path.join(self.path, "runner_config.ini")

    def runner_config(self):

        csv_test = DataCommon().read_config_section(self.runner_path, 'mihoyo_case')  # 执行的用例路径、命名格式

        return csv_test

    def test(self):
        print("当前路径：{path}\n指定文件路径：{runner_path}".format(path=self.path, runner_path=self.runner_path))

if __name__ == '__main__':
    FilePath().test()

