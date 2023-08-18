"""

@productname：PyCharm
@projectname：datedays
@filename：datedays
@time: 2022/8/5 15:00
@author：JiuLiang
@desc：

Python日期工具

能做什么？
1.获取常用日期数据
2.操作excel报表
3.执行通用加密签名
4.获取文件的加密签名

python date tools
what can it do?
1. Get common date data
2. Operating excel report
3. Perform common encryption signature
4. Obtain the encrypted signature of the file

"""

__author__ = 'JiuLiang'
__email__ = "jiuliange@foxmail.com"

import base64
import calendar
import datetime
import logging
import os
import random
import string
import sys
import time
import traceback
import uuid
from datetime import date
from urllib.parse import urlencode, quote, unquote

import openpyxl
import xlrd
from Cryptodome.Hash import MD5, SHA1, MD2, SHA224, SHA256, SHA384, SHA512, SHA3_224, SHA3_256, SHA3_384, SHA3_512
from dateutil.relativedelta import relativedelta
from openpyxl import Workbook


def getnow(format_='%Y-%m-%d %H:%M:%S'):
    '''
    获取当前时间
    get current time
    :param format_: format
    :return:
    '''
    return time.strftime(format_, time.localtime(time.time()))


def gettomorrow(days=1):
    '''
    获取明天的日期，可以指定往后几天
    get tomorrow date

    :param days: 今天+未来几天 today + future days
    :param mode:
    :return:
    '''
    return date.today() + relativedelta(days=days)


def getyesterday(days=1):
    '''
    获取昨天的日期，可以指定往前几天
    get yesterday date
    :param days: 往前第几天 today - past days
    :param mode:
    :return:
    '''
    return date.today() - relativedelta(days=days)


def getdays(number=3):
    '''
    获取所需的日期数量列表，默认在3个月内
    get the required date quantity list, within 3 months by default
    :param number: Number of months generated
    :return: list
    '''
    _days = gettodaydays()
    for _ in range(1, number + 1):
        _days += getnextdays(next_months=_)
    return _days


def getasctime(t=None):
    '''
    将时间元组转换为字符串，例如 such as Wed Aug 17 08:54:46 2022
    :param t: 指定时间戳 specify timestamp
    :return: such as Wed Aug 17 08:54:46 2022
    '''
    if t:
        return time.asctime(time.gmtime(t))
    return time.asctime()


def getnowtimestamp(t=1):
    '''
    获取当前时间戳，默认为秒级
    :param t:  1000
    t=1 秒级 second
    t=1000 毫秒 millisecond
    t=1000000 微秒 Microsecond

    :return: timestamp
    '''
    return int(round(time.time() * t))


def gettodaydays(today=None):
    '''
    获取指定月份的剩余天数，
    如果今天是空的，
    将获得当前月份剩余天数
    obtain the remaining days of the specified month,
    if today is empty,
    the current remaining days will be obtained

    :param today:'%Y-%m-%d'
    :return:_list
    '''
    _list = []
    if today:
        _today = today.split('-')
        _year = int(_today[0])
        _month = int(_today[1])
        __day = int(_today[2])
    else:
        _today = date.today()
        _year = _today.year
        _month = _today.month
        __day = _today.day
    if _month < 10:
        _month = f'0{_month}'
    for _day in [i for i in range(__day, calendar.monthrange(_year, int(_month))[1] + 1)]:
        if _day < 10:
            _day = f'0{_day}'
        _list.append(f'{_year}-{_month}-{_day}')
    return _list


def getnextdays(today=None, next_months=1):
    '''
    返回下个月日期列表（自动跨年）
    return to the next month date list (automatically cross year)

    :param today: specified month '%Y-%m-%d'
    :param next_months:  Specify the interval of the month
    :return:_list
    '''
    _list = []
    if today:
        _today = today.split('-')
        _year = int(_today[0])
        _month = int(_today[1])
        next_month = date(_year, _month, 1) + relativedelta(months=next_months)
    else:
        next_month = date.today() + relativedelta(months=next_months)
    _year = next_month.year
    _month = next_month.month
    if _month < 10:
        _month = f'0{_month}'
    for _day in [i for i in range(1, calendar.monthrange(_year, int(_month))[1] + 1)]:
        if _day < 10:
            _day = f'0{_day}'
        _list.append(f'{_year}-{_month}-{_day}')
    return _list


def getstr2timestamp(date_str, format_='%Y-%m-%d %H:%M:%S'):
    '''
    字符串转时间戳
    string to timestamp

    :param date_str: such as 2022-08-17 16:34:24
    :param format_: such as %Y-%m-%d %H:%M:%S
    :return: timestamp
    '''
    return int(time.mktime(time.strptime(date_str, format_)))


def getcurrent_days(current_date=None):
    return gettodaydays(current_date)


def getnext_days(current_date=None, next_months=1):
    return getnextdays(current_date, next_months)


def excel_write_openpyxl(filename, datas):
    '''
    写入excel报表，支持xls,xlsx
    openpyxl write excel
    support xls,xlsx...

    :param filename:
    :param datas: [[],[],[]]
    :return:
    '''
    try:
        openpyxl_wb = Workbook()
        openpyxl_ws = openpyxl_wb.active
        for i in datas:
            openpyxl_ws.append(i)
        openpyxl_wb.save(filename)
    except Exception:
        print(traceback.format_exc())
        return False
    return True


def excel_read_openpyxl(filename, sheet_index=0):
    '''
    读取excel报表，支持xlsx，不支持xls
    openpyxl read excel
    not support xls

    :param filename:
    :param sheet_index:
    :return:
    '''
    datas = []
    try:
        wb = openpyxl.load_workbook(filename=filename)
        for item in [i for i in wb[wb.get_sheet_names()[sheet_index]].rows]:
            datas.append([str(i.value).replace("None", "") for i in item])
    except Exception:
        print(traceback.format_exc())
    return datas


def excel_read_xlrd(filename, sheet_index=0):
    '''
    读取excel报表，支持xls,xlsx
     xlrd read excel
     support xls,xlsx

    :param filename:
    :param sheet_index:
    :return:
    '''
    datas = []
    try:
        sh = xlrd.open_workbook(filename).sheet_by_index(sheet_index)
        for rx in range(sh.nrows):
            datas.append([str(i.value).replace("None", "") for i in sh.row(rx)])
    except Exception:
        print(traceback.format_exc())
    return datas


def md2(body, encode='utf-8'):
    '''
    MD2加密
    :param body:
    :param encode:
    :return:
    '''
    m = MD2.new()
    m.update(str(body).encode(encode))
    return m.hexdigest()


def md5(body, encode='utf-8', length_=32):
    '''
    MD5加密

    :param body:
    :param encode:
    :param length_:
    :return:
    '''
    m = MD5.new()
    m.update(str(body).encode(encode))
    if length_ == 16:
        return m.hexdigest()[8:-8]
    else:
        return m.hexdigest()


def sha1(body, encode='utf-8'):
    '''
    SHA1加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA1.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha2_224(body, encode='utf-8'):
    '''
    SHA2_224加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA224.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha2_256(body, encode='utf-8'):
    '''
    SHA2_256加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA256.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha2_384(body, encode='utf-8'):
    '''
    SHA2_384加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA384.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha2_512(body, encode='utf-8'):
    '''
    SHA2_512加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA512.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha3_224(body, encode='utf-8'):
    '''
    SHA3_224加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA3_224.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha3_256(body, encode='utf-8'):
    '''
    SHA3_256加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA3_256.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha3_384(body, encode='utf-8'):
    '''
    SHA3_384加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA3_384.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def sha3_512(body, encode='utf-8'):
    '''
    SHA3_512加密
    :param body:
    :param encode:
    :return:
    '''
    h = SHA3_512.new()
    h.update(str(body).encode(encode))
    return h.hexdigest()


def __encrypt_getmode__(mode):
    '''
    get encrypt mode

    :param mode:
    :return:
    '''
    mode = str(mode).upper()
    if 'SHA1' in mode:
        m = SHA1.new()
    elif 'SHA224' in mode:
        m = SHA224.new()
    elif 'SHA256' in mode:
        m = SHA256.new()
    elif 'SHA384' in mode:
        m = SHA384.new()
    elif 'SHA512' in mode:
        m = SHA512.new()
    elif 'SHA3_224' in mode:
        m = SHA3_224.new()
    elif 'SHA3_256' in mode:
        m = SHA3_256.new()
    elif 'SHA3_384' in mode:
        m = SHA3_384.new()
    elif 'SHA3_512' in mode:
        m = SHA3_512.new()
    else:
        m = MD5.new()
    return m


def encrypt_smallfile(filename, mode='MD5'):
    '''
    加密小文件，默认MD5，
    支付SHA1，SHA224，SHA256，SHA384，SHA512，SHA3_224，SHA3_256，SHA3_384，SHA3_512
    encrypt smallfile
    default MD5 encrypt

    :param filename:
    :param mode:
    :return:
    '''
    m = __encrypt_getmode__(mode)
    with open(filename, 'rb') as f:
        m.update(f.read())
    return m.hexdigest()


def encrypt_bigfile(filename, mode='MD5', buffer=8192):
    '''
    加密大文件，默认MD5，
    支付SHA1，SHA224，SHA256，SHA384，SHA512，SHA3_224，SHA3_256，SHA3_384，SHA3_512
    encrypt bigfile
    default MD5 encrypt
    :param filename:
    :param mode:
    :param buffer:
    :return:
    '''
    m = __encrypt_getmode__(mode)
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(buffer)
            if not chunk:
                break
            m.update(chunk)
    return m.hexdigest()


def sleep(seconds=1, max_=None):
    '''
    随机休眠
    random sleep
    :param seconds:default 1 seconds
    :param max_:
    :return:
    '''
    if max_:
        seconds = random.random() * max_

    print(f" random sleep：{seconds} seconds!")
    time.sleep(seconds)


def getuuid(mode=4, merge=False, **kwargs):
    '''
    获取uuid
    get uuid
    :param mode:
    :param merge: replace('-', '')
    :param kwargs:
    :return:
    '''
    if mode == 1:
        u = uuid.uuid1(**kwargs)
    elif mode == 3:
        u = uuid.uuid3(**kwargs)
    elif mode == 5:
        u = uuid.uuid5(**kwargs)
    else:
        u = uuid.uuid4()
    if merge:
        return str(u).replace('-', '')
    return u


def getrandompassword(k=12, more_characters=None, _=string.ascii_letters + string.digits):
    '''
    生成随机密码，默认12位长度
    randomly generated password
    default 12 bits
    recommended more_characters !@#$%.*&+-

    :param k: length
    :param more_characters: recommended   !@#$%.*&+-
    :param _: ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz+0123456789
    :return:
    '''
    if more_characters:
        _ += more_characters
    if k > len(_):
        k = len(_)
    return ''.join(random.sample(_, k))


def gettimestamp2str(timestamp):
    '''
    时间戳转字符串
    timestamp to string
    :param timestamp:  such as 1660726667690
    :return: %Y-%m-%d %H:%M:%S
    '''
    return datetime.datetime.fromtimestamp(float(timestamp))


def base64_encode(s, urlsafe=False, encoding='utf-8'):
    if urlsafe:
        return base64.urlsafe_b64encode(s.encode(encoding)).decode()
    return base64.b64encode(s.encode(encoding)).decode()


def base64_decode(s, urlsafe=False, encoding='utf-8'):
    if urlsafe:
        return base64.urlsafe_b64decode(s).decode(encoding)
    return base64.b64decode(s).decode(encoding)


def urlencodes(body):
    '''
    将dict或者字符转码为URL
    :param body:
    :return:
    '''
    if isinstance(body, dict):
        return urlencode(body)
    return quote(str(body))


def urldecodes(body):
    '''
    解码url
    :param body:
    :return:
    '''
    return unquote(body)


def getstartend(start_date, end_date=date.today(), list_=False):
    '''
    获取间隔天数或天数列表
    get interval days or days list
    :param start_date: %Y-%m-%d
    :param end_date: %Y-%m-%d , default today
    :param list_: datelist
    :return:
    '''

    s_ = [int(_) for _ in str(start_date).split('-')]
    e_ = [int(_) for _ in str(end_date).split('-')]
    s_d = date(s_[0], s_[1], s_[2])
    days = (date(e_[0], e_[1], e_[2]) - s_d).days
    if list_:
        return [(s_d + datetime.timedelta(days=_)).strftime('%Y-%m-%d') for _ in range(days + 1)]
    return days


def headers2dict(headers_string):
    '''
    格式化headers
    copy headers string convert dict
    :param headers_string:
    :return:
    '''
    _dict = {}
    if headers_string:
        for h in [h if len(h) == 2 else None for h in [h.split(':', 1) for h in headers_string.splitlines()]]:
            if h:
                _dict[h[0].strip()] = h[1].strip()
    return _dict


def logger(txt=None, base_name=None, file_name='log.txt', log_base=None,
           fmt=f'%(asctime)s - %(name)s - %(levelname)s - %(message)s',
           mode='a',
           encoding='utf-8', log_dir='/'.join(datetime.date.today().strftime('%Y-%m-%d').split('-'))):
    '''
    logger日志
    '''
    if not base_name:
        base_name = os.path.basename(sys.argv[0]).split('.')[0]

    if not log_base:
        arg = sys.argv[0]
        log_base = arg[:arg.rfind('/')]

    date_dir = f"{log_base}/log/{base_name}/{log_dir}"

    logger = logging.getLogger(base_name + datetime.date.today().strftime('%Y%m%d'))

    if not os.path.exists(date_dir):
        print(f'logger create dir:{date_dir}')
        os.makedirs(date_dir)

        logger.handlers.clear()

    if not logger.handlers:

        # new day,new handler
        formatter = logging.Formatter(fmt)

        # file handler
        fh = logging.FileHandler(f'{date_dir}/{file_name}', mode=mode, encoding=encoding)
        fh.setFormatter(formatter)

        # console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)

        # add handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # set level=debug
        logger.setLevel(logging.DEBUG)

        if txt:
            logger.debug(txt)

    return logger


def getrandomphone(start=None, end=random.randint(10000000, 99999999)):
    '''
    随机手机号，可以指定开头，指定结尾
    :param start:
    :param end:
    :return:
    '''
    if not start:
        start = [130, 131, 132, 133, 134, 150, 151, 155, 158, 166, 180, 181, 184, 185, 188]
    return f'{random.choice(start)}{end}'


def cookie_difference(cookie_str1, cookie_str2):
    '''
    比较cookie之间的差异
    :param cookie_str1:
    :param cookie_str2:
    :return:
    '''
    keys1 = []
    for items in [item.split('=') for item in str(cookie_str1).split('; ')]:
        keys1.append(items[0])
    keys2 = []
    for items in [item.split('=') for item in str(cookie_str2).split('; ')]:
        keys2.append(items[0])
    return [list(set(keys1) - set(keys2)), list(set(keys2) - set(keys1))]
