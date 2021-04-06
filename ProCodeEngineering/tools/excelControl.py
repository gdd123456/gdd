'''
需求：定义一个excel用例读取函数
常规功能：
    1-读取指定行、列数据
    2-具备自动识别无效用例
        a.通过某一个字段（列）去筛选需执行的用例
优化功能：
    1- 在常规版本中，我们是指定读取固定列，不合理。如果需要随机读取用户所要求指定的列，代码需优化
        a. 解决方案：定义参数时候，可以数量不定。——>可变数量参数：*args
        b. 在sheet用例所有列中，用户一般习惯传递什么标识。
            b1:列编号（如9、11，代码维护起来不直观）、b2：列名称。列名称一般较清晰直观
            b2：用户输入的是列名称（即单元格中数据。如：用例编号、接口名称、URL、请求参数、响应结果等），但是代码获取单元格数据是通过cell(行编号，列编号)
             ->用户输入数据与代码读取方式有差异时，需进行转化思维。
具体操作流程：
    1-先把磁盘的excel用例打开到内存里
    2- 使用excel第三方库操作：xlrd(.xls)、pyopenxl(.xlsx)、pandas(处理大数据的csv)
        a.获取workbook对象  b.从表中对应对应的worksheet对象(某个子sheet)  c.获取某个sheet中的行/列、单元数据
'''
import  xlrd

# —————————————————————————常规功能版本———————————————————————————————————————————————————

def getExcelData(excelDir, sheetName, caseName):
    # 1- 定义excel路径
    # 2- 打开excel。formatting_info=True 保持excel样式
    workBook=xlrd.open_workbook(excelDir, formatting_info=True ) # workbook是一个xx.xls文件对象
    # 3- 具体操作excel文件中的某一个sheet
    # workSheet=workBook.sheet_names()  # 获取所有的sheet表。
    # print(workSheet) ===>['登录模块', '我的商铺', '食品管理', '我的订单', '修改密码']
    # 通过sheetName获取所需的sheet表
    workSheet = workBook.sheet_by_name(sheetName)
    # 4- 读取第一行数据
    print(workSheet.row_values(0))  # ===>['用例编号', '模块', '接口名称', '优先级', '标题', 'URL', '前置条件', '请求方式', '请求头', '请求参数', '预期结果', '响应预期结果', '实际结果']
    # 4- 读取第一列数据
    print(workSheet.col_values(0))  # ['用例编号', 'Login001', 'Login002', 'Login003', 'Login004', 'Login005', 'Login006']
    # 5- 筛选用例
    idx=0 # 初始化行的值0  注：excel文件中行数从0开始
    resList=[]  # 定义一个列表，存放从sheet中逐行读取出的数据
    for one in workSheet.col_values(0):  # 对第一列数据进行遍历操作，筛选有效用例
        if caseName in one: # 说明用例有效
            # 读取sheet中某个单元格数据。workSheet.cell(行号，列号).value
            reqbody=workSheet.cell(idx,9).value  # 读取“请求参数”
            expData=workSheet.cell(idx,11).value # 读取“响应预期结果”
            resList.append((reqbody,expData))
        idx += 1 # 行编号遍历递增
    return  resList
if __name__ == '__main__':
    res = getExcelData('../data/LoginInterfaceTestCase.xls','登录模块','Login')
    # print(res)
    for i in res:
        print(i)
