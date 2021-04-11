'''
需要自动化执行excel用例
流程：
    1. 从excel用例获取对应的接口数据
    2. 数据结合接口代码进行自动化执行
    3. 判断结果是否符合预期
'''


"""
from pprint import pprint
# 1- 从exce表获取对应接口数据
from libs.login import Login
from tools.excelControl import getExcelData
resList=getExcelData('../data/LoginInterfaceTestCase.xls', '登录模块', 'Login', "请求参数", '响应预期结果')
# pprint(resList)
# 2- 数据结合代码接口进行自动化执行
# login()封装的业务代码inData（字典类型）。
for one in resList:
    # print(one)  # ===>[请求参数，响应预期结果]
    res=Login().login(one[0])
    # print(res)   # 接口实际返回的响应数据
    if res['msg'] == one[1]['msg']:
        print('------pass-----')
    else:
        print('----fail-------')
"""


'''
pytest 运行结果里面：
1.    . 成功
2.    F 断言失败
3.    E 语法报错
'''
# 测试代码
from libs.login import Login
from tools.excelControl import getExcelData
import pytest
import os
import allure_pytest
import pytest_html
class TestLogin:  # 定义测试类
    # 测试方法
    # 数据驱动——参数化——读取用例数据
    # @pytest.mark.parametrize('参数的变量名',实际需要传入的参数)
    # @pytest.mark.parametrize('a,b',[(1,2),(3,4)])
    # @pytest.mark.parametrize('a,b,c', [(1,2,3), (3, 4,5)])
    @pytest.mark.parametrize('inBody,expData', getExcelData('../data/LoginInterfaceTestCase.xls','登录模块','Login','请求参数','响应预期结果'))
    def test_login(self, inBody,expData):
        # 调用接口代码
        res=Login().login(inBody)  # 请求体传入，调用登录接口
        # print(res)
        # 断言
        print('用例执行')
        assert res['msg'] == expData['msg']
        # 多个标识表示需要断言的操作
        # assert  res['msg'] == expData['msg'] and \
        #         res['code'] == expData['code']
if __name__ == '__main__':
    # pytest.main(['test_login.py'])
    # pytest.main(['test_login.py','-s'])   # -s 显示print打印信息

    # 遇到问题：运行了6个用例，但报告里面有12个用例。重复显示
    # 解决方案：
    #     1- 上一次运行有报告文件
    print(os.listdir('../report/tmp'))  # 列出这个路径下文件
    # for one in os.listdir('../report/tmp'): # one是每一个文件
        # print(one)
        # if '.json' in one: # 以后有环境配置文件在里面，所以做了判断
        #     os.remove(f'../report/tmp/{one}')

        
    

    # '--alluredir','../report/tmp'   报告需要的文件存放路径
    pytest.main(['test_login.py', '-s', '--alluredir', '../report/tmp'])
    # 转化成可视化报告  allure 指令
    # allure serve  给报告起一个服务
    # 注意事项：记得把火狐或者谷歌浏览器设置成默认浏览器
    os.system('allure serve ../report/tmp')
"""
allure工作流程
    1- 通过pytest运行测试用例。pytest.main() ,一定有结果。后面报告的数据来源
    2- 有了源数据后，需通过一个工具去读取转化源数据，得到allure可视化报告。 
"""

