import os

from libs.login import Login
from libs.shop import Shop
import pytest
from tools.excelControl import getExcelData
# 封装测试类
class TestShop:
    def setup_class(self):  # 初始化
        # setup_class：类级别，这个类开始时候只运行一次
        '''
        该初始化是干什么？1.获取token、2.获取headers、3.登录操作、4.创建一个店铺实例（更适合）
        '''
        self.token=Login().login({"username": "th0336", "password": "53339"},getToken=False)
        self.shopObject=Shop(self.token)
        print('---------初始化操作----------')
    def teardown_class(self):
        print('------数据清除操作------')

    # 1- 列表店铺测试方法
    @pytest.mark.parametrize('inBoday,expData',getExcelData('../data/LoginInterfaceTestCase.xls',
                                                            '我的商铺','listshopping','请求参数','响应预期结果'))
    def test_shoplist(self,inBoday,expData):
        # 调用列出接口
        res=self.shopObject.shop_list(inBoday)
        if 'code' in res:
            assert res['code'] == expData['code']
        else:
            assert res['msg'] == expData['msg']


    if __name__ == '__main__':
        try:
            for one in os.listdir('../report/tmp'):  # one是每一个文件
                if '.json' in one:  # 以后有环境配置文件在里面，所以做了判断
                    os.remove(f'../report/tmp/{one}')
        except:
            print('第一次运行pytest.main()')

        pytest.main(['test_shop.py', '-s', '--alluredir', '../report/tmp'])
        os.system('allure serve ../report/tmp')



