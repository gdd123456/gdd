from configs.config import HOST
import hashlib
import requests
# 加密方式：规则加密（md5、base64、aes），直接调用自带模块、自定义加密（开发自定义，需要询问开发加密规则）
def get_md5(psw):
    # 1. 实例化一个md5对象
    md5=hashlib.md5()
    # 2. 调用加密方法update()
    md5.update(psw.encode("utf-8"))  # 调用encode()方法的目的是防止输入中文，出现乱码
    # 3. 返回值
    return  md5.hexdigest()    # 返回16进制的结果

# 构造接口请求
class Login:
    def login(self,inData,getToken=False):
        # 由于登录接口的账号、密码用例是多次输入（分批次），不能写死。因此通过形参来传值
        # 登录接口成功后，响应数据包含token。默认不单独获取响应数据中的token值
        # 1. URL
        url=f"{HOST}/account/sLogin"
        # 2. 参数
        # 由于密码在写用例时候，一般不进行加密。因此在进行post请求之前，要对密码密码进行加密
        # a.字典修改：字典名[键名]=新的值。 b.访问字典值：字典名[键名]
        inData['password']=  get_md5(inData['password'])
        payload=inData
        # 3. 发请求
        resp=requests.post(url,data=inData)
        # 4.查看响应结果
        # return resp.json()
        if getToken==True:  # 获取token值
            return resp.json()['data']['token']
        else:  # 获取登录接口的响应
            return resp.json()
if __name__ == '__main__':
    res = Login().login({"username": "th0336", "password": "53339"},getToken=False)
    print(res)