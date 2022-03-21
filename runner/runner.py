import unittest
import time
from BeautifulReport import BeautifulReport
from SeleniumUnittestBeautifulReport.base.box import DataCommon, EmailCommon


# from SeleniumUnittestBeautifulReport.data.file_path import FilePath


class Runner(object):

    def run_test(self):
        """  运行测试 """

        test_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())
        # log日志保存路径
        # logger_file = "./runner/log/zentao_automate_log_%s.log" % test_time

        # 待执行用例
        csv_test = DataCommon().read_config_section("./runner/config/runner_config.ini", 'unit_case')  # 执行的用例路径、命名格式
        # csv_test = FilePath().runner_config()  # 待调试方案
        test_dir = csv_test[1][1]
        test_pattern = csv_test[2][1]
        print(csv_test)
        dis = unittest.defaultTestLoader.discover(test_dir, pattern=test_pattern)

        # 报告文件保存路径
        report_file = "./runner/report/mihoyo_automate_report_%s.html" % test_time
        # 执行用例生成报告
        runner = BeautifulReport(dis)
        runner.report(filename=report_file, description="具体测试报告内容如下: ")

        # 发送测试报告到指定邮箱
        EmailCommon().email_attachment(report_file)


if __name__ == '__main__':
    Runner().run_test()
