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
"""
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

# —————————————————————————常规功能版本———————————————————————————————————————————————————
"""

'''
# —————————————————————————优化功能版本V1.0———————————————————————————————————————————————————
import json
def getExcelData(excelDir, sheetName, caseName,*args):  # args：元组
    # 1- 定义excel路径
    # 2- 打开excel。formatting_info=True 保持excel样式
    workBook = xlrd.open_workbook(excelDir, formatting_info=True)  # workbook是一个xx.xls文件对象
    # 3- 具体操作excel文件中的某一个sheet
    # 通过sheetName获取所需的sheet表
    workSheet = workBook.sheet_by_name(sheetName)
    # 4- 读取第一行数据
    # print(workSheet.row_values(0))  # ===>['用例编号', '模块', '接口名称', '优先级', '标题', 'URL', '前置条件', '请求方式', '请求头', '请求参数', '预期结果', '响应预期结果', '实际结果']
    # 4- 读取第一列数据
    # print(workSheet.col_values(0))  # ['用例编号', 'Login001', 'Login002', 'Login003', 'Login004', 'Login005', 'Login006']
    colIdex =[]   # 存放用户需要获取列名称对应的列编号

    #—-----------------将用户输入列名称转化成列编号----------------------
    for i in args: # 遍历元组
        # 列名称在sheet中第0行
        # 通过列名称的值，获取对应的下标
        colIdex.append(workSheet.row_values(0).index(i))
    # print("列名称对应的下标>>>",colIdex)
    #-------------------将用户输入列名称转化成列编号---------------------

    idx=0 # 初始化行的值0
    resList=[]  # 定义一个列表，存放从sheet中逐行读取出的数据
    for one in workSheet.col_values(0):  # 对第一列数据进行遍历操作，筛选有效用例
        if caseName in one: # 说明用例有效
            getColData =[]
            # 读取sheet中某个单元格数据
            # workSheet.cell(行号，列号).value
            for num in colIdex:
                # res = workSheet.cell(idx, num).value
                res=json.loads(workSheet.cell(idx,num).value)  # 获取单元格数据（格式为字符串）。号外号外：如果不进行转化的话，test_login执行用例全部会报错哦
                # 漏洞：workSheet.cell(idx,num).value前提是json格式。否则无法转化
                getColData.append(res)  # 把用户需要读取的列数据，append至一个列表
            resList.append(getColData)
        idx += 1 # 行编号遍历递增
    return  resList
import pprint
if __name__ == '__main__':
    # res = getExcelData('../data/LoginInterfaceTestCase.xls','登录模块','Login','用例编号',"请求参数",'响应预期结果')
    res = getExcelData('../data/LoginInterfaceTestCase.xls', '登录模块', 'Login',  "请求参数", '响应预期结果')
    pprint.pprint(res)
'''


# —————————————————————————代码优化V1.1———————————————————————————————————————————————————
'''
优化需求：
    1- 如果我们需要获取数据不是json格式的列数据，代码会报错。（如登记接口URL的用例）
        json.loads(workSheet.cell(idx,num).value) 
    2- 数据驱动时候，一个登陆的接口用例sheet，全表用例数据读取。需求点：能否只执行某几条用例？连续用例编号？单个不连续用例
        方案：a. pytest数据驱动是靠一个@pytest.mark.parametrize('参数的变量名',实际需要传入的参数)
             b. 只需要把挑选的用例读取出来即可
             c. 分类： all 所有用例、001-004 连续一段、001 003 005 不连续
                       复杂的场景['001','005-008','010']
'''
# 判断是否是json格式的方法2 （注：方法1比较极端，判断左右两边是否有{ 、}。如请求参数、响应预期结果）
import json
def is_json(s):
    try:
        json.loads(s)  # json转化字典
    except ValueError:
        return False    # 不是json
    return  True     # 是jasn

def getExcelData(excelDir, sheetName, caseName,*args,runCase=['all']):
    '''
    :param excelDir:
    :param sheetName:
    :param caseName:
    :param args:元组
    :param runCase:挑选的运行用例，默认是all
    :return:
    '''

    workBook = xlrd.open_workbook(excelDir, formatting_info=True)  # workbook是一个xx.xls文件对象
    workSheet = workBook.sheet_by_name(sheetName)
    colIdex =[]   # 存放用户需要获取列名称对应的列编号

    #—-----------------将用户输入列名称转化成列编号----------------------
    for i in args: # 遍历元组
        # 列名称在sheet中第0行
        # 通过列名称的值，获取对应的下标
        colIdex.append(workSheet.row_values(0).index(i))
    # print("列名称对应的下标>>>",colIdex)
    #-------------------将用户输入列名称转化成列编号---------------------

    runList=[]  #最后的运行列表
    if runCase[0]=='all': # 全部运行  runCase是用户传进来的运行列表
        runList=workSheet.col_values(0)  # 第一列所有数据
    else:  # 如果不是all
        # 连续的  003-007
        # 不连续的  001  005  007
        for one  in runCase:
            if '-'  in  one:  # 连续的'003-007'
                start,end=one.split('-')  # 获取连续用例编号的头尾
                for i in range(int(start),int(end)+1):   # for 003 004 005 006 007
                    runList.append(caseName+f'{i:0>3}')
            else:
                runList.append(caseName+f'{i:0>3}')  # Login001

    idx=0 # 初始化行的值0
    resList=[]  # 定义一个列表，存放从sheet中逐行读取出的数据
    for one in workSheet.col_values(0):  # 对第一列数据进行遍历操作，筛选有效用例
        if caseName in one and one in runList: # 说明用例有效
            getColData =[]
            # 读取sheet中某个单元格数据
            # workSheet.cell(行号，列号).value
            for num in colIdex:
                # res = workSheet.cell(idx, num).value
                # 如果是json字符串，就转化成字典。不是json格式，就不转化
                res =workSheet.cell(idx,num).value  # excel读出来的都是字符串格式
                # if res[0]=='{' and res[-1]=='}':  判断json格式1
                if is_json(res):
                    res=json.loads(workSheet.cell(idx,num).value)
                getColData.append(res)  # 把用户需要读取的列数据，append至一个列表
            resList.append(getColData)
        idx += 1 # 行编号遍历递增
    return  resList

import pprint
if __name__ == '__main__':
    # res = getExcelData('../data/LoginInterfaceTestCase.xls','登录模块','Login','用例编号',"请求参数",'响应预期结果')
    res = getExcelData('../data/LoginInterfaceTestCase.xls', '登录模块', 'Login',  'URL','请求参数',runCase=['001','002-004','006'])
    pprint.pprint(res)
