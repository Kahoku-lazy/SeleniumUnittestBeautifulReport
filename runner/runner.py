import unittest
from unittest import TestSuite
import time
from BeautifulReport import BeautifulReport

# from seleniumPython3.base.box import DataProcessing
# from seleniumPython3.case.mihoyo_case.mihoyo_test_main import MihoyoTest
from seleniumPython3.base.box import DataProcessing


class Runner(object):

    def run_test(self):
        """  运行测试 """

        test_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # log日志保存路径
        # logger_file = "./runner/log/zentao_automate_log_%s.log" % test_time

        # 执行的用例
        csv_test = DataProcessing().read_dict_csv("./runner/data/runner.csv")               # 执行的用例路径、命名格式
        test_dir = csv_test[0]["test_dir"]
        test_pattern = csv_test[0]["test_pattern"]
        dis = unittest.defaultTestLoader.discover(test_dir, pattern=test_pattern)

        # 报告文件保存路径
        report_file = "./runner/report/mihoyo_automate_report_%s.html" % test_time
        # 执行用例生成报告
        runner = BeautifulReport(dis)
        runner.report(filename=report_file,  description="具体测试报告内容如下: ")

        # 发送测试报告到指定邮箱
        # Email().email_attachment(report_file)

if __name__ == '__main__':
    csv_data = DataProcessing().read_dict_csv("./data/runner.csv")
    print(csv_data)