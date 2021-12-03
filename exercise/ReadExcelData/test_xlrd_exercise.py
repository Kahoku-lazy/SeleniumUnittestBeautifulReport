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


