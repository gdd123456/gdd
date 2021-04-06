'''
需要自动化执行excel用例
流程：
    1. 从excel用例获取对应的接口数据
    2. 数据结合接口代码进行自动化执行
    3. 判断结果是否符合预期
'''
from pprint import pprint
# 1- 从exce表获取对应接口数据
from libs.login import Login
from tools.excelControl import getExcelData
resList=getExcelData('../data/LoginInterfaceTestCase.xls', '登录模块', 'Login', "请求参数", '响应预期结果')
pprint(resList)
# 2- 数据结合代码接口进行自动化执行
for one in resList:
    # print(one)  # ===>[]
    Login().login(one[0])