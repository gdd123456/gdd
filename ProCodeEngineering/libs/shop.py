from configs.config import HOST
import requests

class Shop:
    '''
    # 店铺模块下涉及如下多个模块
    # 1. 列出店铺
    # 2. 编辑店铺
    # 3. 删除店铺
    # 4. 增加店铺
    '''
    # 注：上述1、2、3、4,不管哪个接口，都需要完成“登录”操作。即登录是公共的。因此可直接实例化登录。封装类，在类中实例化登录，只要创建店铺，就直接给token值
    # 所以请求消息头中，均包含：Authorization 必填 token 值
    def __init__(self,inToken):
        # 定义一个实例属性
        self.header={"Authorization":inToken}
    # 1.列出店铺
    def shop_list(self,inData):
        # 1. URL
        URL=f"{HOST}/shopping/myShop"
        # 2. 参数
        payload=inData
        # 3. 请求
        resp=requests.get(URL,params=inData,headers=self.header)
        # 4. 响应结果
        return resp.json()
from libs.login import Login
import pprint
if __name__ == '__main__':
    # 1. 登录->获取token
    token = Login().login({"username": "th0336", "password": "53339"},getToken=True)
    # 2. 列出店铺接口调用
    res=Shop(token).shop_list({"page":1,"limit":20})
    pprint.pprint(res)
