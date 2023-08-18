'''

Python日期工具

能做什么？
1.获取常用日期数据
2.操作excel报表
3.执行通用加密签名
4.获取文件的加密签名

python date tools
what can it do?
*  1.Get common date data]
*  2.Operating excel report
*  3.Perform common encryption signature
*  4.Obtain the encrypted signature of the file

'''

__author__ = 'JiuLiang'
__email__ = "jiuliange@foxmail.com"

name = "datedays"

from .datedays import getnow, gettomorrow, getyesterday, getdays, getasctime, getnowtimestamp, \
    gettodaydays, getnextdays, getstr2timestamp, getcurrent_days, getnext_days, excel_write_openpyxl, \
    excel_read_openpyxl, excel_read_xlrd, md2, md5, sha1, sha2_224, sha2_256, sha2_384, sha2_512, sha3_224, sha3_256, \
    sha3_384, sha3_512, encrypt_smallfile, encrypt_bigfile, sleep, getuuid, getrandompassword, gettimestamp2str, \
    base64_encode, base64_decode, urlencodes, urldecodes, getstartend, headers2dict, logger, getrandomphone, \
    cookie_difference
