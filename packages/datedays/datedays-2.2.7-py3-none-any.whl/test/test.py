"""

@productname：PyCharm
@projectname：datedays
@filename：datedays_test
@time: 2023/7/3 10:28
@author：liang1024
@desc：

"""
__author__ = 'JiuLiang'
__email__ = "jiuliange@foxmail.com"

import datedays

if __name__ == '__main__':
    print(datedays.getasctime())
    print(datedays.getasctime(4102329600))
    print(datedays.getnowtimestamp())
    print(datedays.getstr2timestamp('2099-12-31 00:00:00'))
    print(datedays.headers2dict('''
    Accept: application/json, text/javascript, */*; q=0.01
    Accept-Encoding: gzip, deflate, br
    Accept-Language: zh-CN,zh;q=0.9
    Cache-Control: no-cache
    Connection: keep-alive
    Content-Type: application/x-www-form-urlencoded; charset=UTF-8
    Pragma: no-cache
    Sec-Fetch-Mode: cors
    Sec-Fetch-Site: same-origin
    User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36
    X-Requested-With: XMLHttpRequest
    '''))
