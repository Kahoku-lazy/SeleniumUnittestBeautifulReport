from runner.runner import Runner


class Main(object):
    """ 自动化测试方案的唯一执行入口 """

    @staticmethod
    def running():
        """ 静态的执行方法 """
        Runner().run_test()


if __name__ == "__main__":
    Main.running()
