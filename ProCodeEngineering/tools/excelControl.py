'''
需求：定义一个excel用例读取函数
功能：
1-读取指定列数据
2-具备自动识别无效用例
具体操作流程：
1-先把磁盘的excel用例打开到内存里
2- 使用excel第三方库操作：xlrd(.xls)、pyopenxl(.xlsx)、pandas(处理大数据的csv)
'''
import xlrd
def getExcelData(excelDir):
    # 1- 定义excel路径
    # 2- 打开excel
    xlrd.open_workbook()


