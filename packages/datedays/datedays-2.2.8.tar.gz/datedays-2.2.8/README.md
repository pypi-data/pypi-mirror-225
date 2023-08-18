## 它可以干什么？

* [1.获取常用日期数据](#datadays)
* [2.操作Excel报表](#excel)
* [3.进行常用加密签名](#hash)
* [4.获取文件的加密签名](#file)
* [5.其他](#other)

**pip安装使用**:

```console
$ pip install datedays
```

例子：

```python
import datedays

if __name__ == '__main__':
    print("现在时间：", datedays.getnow())  # format_=格式,比如：%Y-%m-%d %H:%M:%S
    print('-' * 30)
    print("明天：", datedays.gettomorrow())
    print("后天：", datedays.gettomorrow(days=2))  # days等于多少，就是多少天
    print("30天后是几号：", datedays.gettomorrow(days=30))
    print("180天后是几月几号：", datedays.gettomorrow(days=180))
    print("1000天后是几月几号：", datedays.gettomorrow(days=1000))
    print('-' * 30)
    print("昨天：", datedays.getyesterday())
    print("前天：", datedays.getyesterday(days=2))
    print("180天前：", datedays.getyesterday(days=180))
    print("1000天前是几月几号：", datedays.getyesterday(days=1000))
```

```
现在时间： 2022-08-19 15:06:33
------------------------------
明天： 2022-08-20
后天： 2022-08-21
30天后是几号： 2022-09-18
180天后是几月几号： 2023-02-15
1000天后是几月几号： 2025-05-15
------------------------------
昨天： 2022-08-18
前天： 2022-08-17
180天前： 2022-02-20
1000天前是几月几号： 2019-11-23
```

### 还在持续更新中...

## 1.获取常用日期数据

方法| 描述| 返回结果| 参数<a id="datadays"></a>
:---: | :---:| :---:| :---:
getnow() |获取今天日期|比如：2022-08-16 17:56:17|
gettomorrow() |明天|2022-08-17|参数1：可选未来第几天(传入想要的数字)
getyesterday()|昨天|2022-08-15|参数1：可选过去第几天(传入想要的数字)
getdays() |默认三个月内的日期列表|...(建议测试打印)|number=想要的月份数量
getasctime() |获取格式化时间|比如:Wed Aug 17 17:08:37 2022|参数1:指定时间戳
getnowtimestamp() |获取当前时间戳|1660644568238|默认毫秒(可选秒，毫秒，微秒)
gettodaydays() |默认获取本月剩余天数列表|...(建议测试打印)|可以指定某月份某一天，获取当月剩余天数
getnextdays() |默认获取下月总天数列表|...(建议测试打印)|可以指定月份，指定月份数量
getstr2timestamp() |日期字符串转时间戳|...(建议测试打印)|参数1：日期，参数2：日期的格式
gettimestamp2str() |时间戳转日期字符串|...(建议测试打印)|参数1：时间戳
getstartend() |计算日期之间的间隔天数|...(建议测试打印)|参数1：开始日期，参数2：结束日期（默认当天）参数3：返回日期列表

## 2.操作Excel报表

方法| 描述| 返回结果| 参数<a id="excel"></a>
:---: | :---:| :---:| :---:
excel_write_openpyxl() |写入Excel报表|...(建议测试)|filename:文件名，datas：要保存的数据,格式:[[第一行],[第二行],[第三行]...]
excel_read_openpyxl() |读取Excel报表|...(建议测试)|filename:文件名，sheet_index：sheet的下标
excel_read_xlrd() |读取Excel报表(支持xls)|...(建议测试)|filename:文件名，sheet_index：sheet的下标

## 3.进行常用加密签名

方法| 描述| 返回结果| 参数<a id="hash"></a>
:---: | :---:| :---:| :---:
md2() |MD2加密|...(建议测试)|body:加密内容，encode：编码格式
md5() |MD5加密|...(默认32位结果)|body:加密内容，encode：编码格式，length_：返回长度，可选16
sha1() |SHA1加密|...(建议测试)|body:加密内容，encode：编码格式
sha2_224() |SHA2_224加密|...(建议测试)|body:加密内容，encode：编码格式
sha2_256() |SHA2_256加密|...(建议测试)|body:加密内容，encode：编码格式
sha2_384() |SHA2_384加密|...(建议测试)|body:加密内容，encode：编码格式
sha2_512() |SHA2_512加密|...(建议测试)|body:加密内容，encode：编码格式
sha3_224() |SHA3_224加密|...(建议测试)|body:加密内容，encode：编码格式
sha3_256() |SHA3_256加密|...(建议测试)|body:加密内容，encode：编码格式
sha3_384() |SHA3_384加密|...(建议测试)|body:加密内容，encode：编码格式
sha3_512() |SHA3_512加密|...(建议测试)|body:加密内容，encode：编码格式

## 4.获取文件的加密签名

方法| 描述| 返回结果| 参数<a id="file"></a>
:---: | :---:| :---:| :---:
encrypt_smallfile() |加密小文件|...(建议测试)|filename:文件名，mode：默认md5(可选上面的加密)
encrypt_bigfile() |加密大文件|...(建议测试)|filename:文件名，mode：默认md5(可选上面的加密)

## 其他...

Method | description | return result | parameter <a id = "other"></a>
:---: | :---:| :---:| :---:
getuuid() | 获取uuid(支持1,3,4,5) |... (recommended test) | mode:默认 uuid4,merge:去掉'-'
getrandompassword() | 随机生成密码串 |... (recommended test) | k: 返回长度(默认12), more_characters: 拼接字符,推荐 !@#$%.*&+-、
headers2dict() |headers字符串转dict|...(建议测试打印)|参数1：headers字符串
getrandomphone() |获取随机手机号|...(建议测试打印)|
cookie_difference() |比较两个cookie的不同|...(建议测试打印)|

例子：

**获取2天后-10天之内的日期列表：**

```
import datedays
 
if __name__ == '__main__':
    print(datedays.getdays()[2:10])  # 2天之后，10天之内的日期列表
```

结果：

```
['2022-08-11', '2022-08-12', '2022-08-13', '2022-08-14', '2022-08-15', '2022-08-16', '2022-08-17', '2022-08-18']
```

希望它能帮到你 ！
[English Introduction Document](https://github.com/liang1024/datedays/blob/main/README-CN.md)

