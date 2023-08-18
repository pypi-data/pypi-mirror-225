#### pip安装
```
pip install -e git+ssh://git@git.tigerbrokers.net/libs/thanos-client-python.git@v1.0.2#egg=thanosclient==1.0.2

```
或者
```
# 需配置使用内部源 https://wiki.tigerbrokers.net/pages/viewpage.action?pageId=63905114
pip install thanosclient==1.0.2

```

#### 或本地安装
```
python setup.py install
```

#### 调用示例
```

推荐使用单例


from thanosclient.client import CipherClient
from thanos.v1 import cipher_pb2

# timeout, authority为可选参数
c = CipherClient(addr='abc.tigerfintech.com:3000', 
                 app_key='pjRznwighs82m', app_secret='OhxaibuyairaimaeL3queloo3bu9xoot',
                 timeout=0.5, authority='abc.tigerfintech.com:3000')

# ptyhon2 返回unicode, python3 str
c.encrypt("23423423", user_id="34", ip="127.0.0.1")

# mode默认为脱敏模式, text_type默认为手机号
# mode和text_type的枚举取值见proto文件
# ptyhon2 返回unicode, python3 str
c.decrypt("v3:58082929E10E74BB3031758A81E355BBA2EEDCE917729A6C20E182A16DFC2687", 
            user_id="324", ip='127.0.0.1', mode=cipher_pb2.PLAIN)
            
c.decrypt("v3:58082929E10E74BB3031758A81E355BBA2EEDCE917729A6C20E182A16DFC2687", 
            user_id="324", ip="127.0.0.1", mode=cipher_pb2.MASK, text_type=cipher_pb2.ID_NO)
            
# hash返回类型字符串列表，python2 元素类型为unicode, python3为str
# multi默认为False，返回列表只有一个元素, 最新版hash
result = c.hash("23452423",  user_id="324", ip="127.0.0.1")  # 返回列表


# multi为True, 新旧一起返回，排在越前面版本越新
result = c.hash("23452423",  user_id="324", ip="127.0.0.1", multi=True)  # 返回列表
```

#### 发布 Pypi

