
from tkinter.constants import S
from box import BoxDriver

class ExerciseBox:

    selector_qqEmial = {"qq登录": "i, qqLoginTab", "微信登录": "i, wxLoginTab",
                    "用户名": 'x, //*[@id="u"]',  # "i, u",
                     "密码": "i, p", "登录": "login_button",
                     "百度": "kw", "百度百科": "p, 百度百科"}

    def __init__(self) -> None:

        self.driver = BoxDriver()

        self.driver.navigate("https://www.baidu.com/")

    def click_page(self):
        
        # self.driver.implicitly_wait(3)
        # self.driver.click(self.selector_qqEmial["微信登录"])

        # self.driver.forced_wait(3)
        # self.driver.click(self.selector_qqEmial["qq登录"])

        self.driver.forced_wait(3)
        self.driver.type(self.selector_qqEmial["百度"], "otaku")

        self.driver.button_enter(self.selector_qqEmial["百度"])

        self.driver.forced_wait(3)
        self.driver.click(self.selector_qqEmial["百度百科"])

    def test(self):

        browser_data = self.driver.get_data()
        
        self.click_page()

        str_data = "当前URL地址为: {url}\n当前浏览器标签名称: {title}\n当前浏览器标签句柄：{handle}"
        print(str_data.format(url=browser_data[0], title=browser_data[1], handle=browser_data[2]))

        self.driver.forced_wait(10)

        self.driver.quit_driver()
        
import xlrd

exce_path = r"C:/Python/PythonCode/ReadExcelData/xls_exercise.xls"
# exce_path1 = r"C:/Python/PythonCode/ReadExcelData/xlsx_exercise.xlsx"

xls = xlrd.open_workbook(exce_path)

# xlsx = xlrd.open_workbook(exce_path1)
# print("All sheets: %s" % xlsx.sheet_names())

sheet1 = xls.sheets()[0]
sheet1_name = sheet1.name   
sheet1_cols = sheet1.ncols  
sheet1_nrows = sheet1.nrows
# print('Sheet1 Name: %s\nSheet1 cols: %s\nSheet1 rows: %s' % (sheet1_name, sheet1_cols, sheet1_nrows))

sheet1_nrows4 = sheet1.row_values(4)    # 行
sheet1_cols2 = sheet1.col_values(2)     # 列

cell42 = sheet1.row(2)[2].value         # 行 列 

# print('Row 4: %s\nCol 2: %s\nCell 1: %s\n' % (sheet1_nrows4, sheet1_cols2, cell42))

# 调试入口
if __name__=='__main__':

    eb = ExerciseBox()

    eb.test()

