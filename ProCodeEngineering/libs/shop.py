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

    # 图片上传接口
    def file_upload(self,fileName,fileDir,fileType):
        # 对于动态变化的，可进行形参处理
        url=f"{HOST}/file"
        # 封装请求数据
        # {'变量名1':文件属性}——>{'变量名1':(文件名称,文件对象，文件类型)}
        # 多个文件上传：{'变量名1':(文件名称,文件对象，文件类型),'变量名2':(文件名称,文件对象，文件类型)}
        userFile={'file':(fileName,open(fileDir,'rb'),fileType)}
        resp=requests.post(url,files=userFile,headers=self.header)
        return resp.json()


    # 2. 编辑店铺
    """
    注意事项：
        1- 导入测试用例的店铺id目前是硬编码。——需要动态关联shop_list接口
        2- 导入测试用例的图片信息目前是硬编码。——需要动态关联file_upload接口
    """
    def shop_update(self,inData,shopId,imageInfo):
        url=f"{HOST}/shopping/updatemyshop"
        # 获取动态值——更新值







    # 3. 删除店铺  admin，系统的管理员平台操作
    # 4. 增加店铺  admin，系统的管理员平台操作




from libs.login import Login
import pprint
if __name__ == '__main__':
    # 1. 登录->获取token
    token = Login().login({"username": "th0336", "password": "53339"},getToken=True)
    # 创建示例   实例=类名()
    # 实例.实例方法
    shopObject=Shop(token)   # 店铺实例

    # 2. 列出店铺接口调用
    # shopRes=shopObject.shop_list({"page":1,"limit":20})
    # pprint.pprint(shopRes)

    # 文件上传接口验证
    fileRes=shopObject.file_upload('picture.png','../data/picture.png','image/png')
    print(fileRes)


