import json
import sys
import time
import os
import string
import random
import pytz
import datetime
from django.utils import timezone
from dateutil.parser import parse
from dateutil.tz import tzlocal


# 获取当前时间
def get_current_time():
    # TODO USE_TZ = False 时会报错 如果USE_TZ设置为True时，Django会使用系统默认设置的时区，即America/Chicago，此时的TIME_ZONE不管有没有设置都不起作用。
    tz = pytz.timezone('Asia/Shanghai')
    # 返回datetime格式的时间
    now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
    # now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.strptime(now_time, "%Y-%m-%d %H:%M:%S")
    return now


# 数据key替换
def replace_dict_key(dictionary, old_key, new_key):
    if old_key in dictionary:
        dictionary[new_key] = dictionary.pop(old_key)
    return dictionary


# 字符串转列表
def parse_integers(value):
    if isinstance(value, str):
        if "," in value:
            lst = [int(num) for num in value.split(",")]
        else:
            lst = [int(value)]
    elif isinstance(value, int):
        lst = [value]
    else:
        raise TypeError("不支持的值类型。应为字符串或int")

    return lst


# 保留两位小数
def keep_two_decimal_places(str_num):
    result_num = format(float(str_num), "")

    if len(result_num.split(".")[-1]) < 2:
        result_num = result_num + "0"
    return result_num


# 生成一个长度为16的密码
def generate_password(length=16):
    # 合并所有可能的字符，包括大小写字母、数字和标点符号
    # all_chars = string.ascii_letters + string.digits + string.punctuation
    all_chars = string.ascii_letters + string.digits
    # length = random.randint(8, 12)
    # 随机选择指定数量的字符
    password = ''.join(random.choice(all_chars) for _ in range(length))

    return password


# 数字表示生成几位, True表示生成带有字母的 False不带字母的
def get_code(n=6, alpha=False):
    s = ''  # 创建字符串变量,存储生成的验证码
    for i in range(n):  # 通过for循环控制验证码位数
        num = random.randint(1, 9)  # 生成随机数字0-9
        if alpha:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
            upper_alpha = chr(random.randint(65, 90))
            lower_alpha = chr(random.randint(97, 122))
            num = random.choice([num, upper_alpha, lower_alpha])
        s = s + str(num)
    return s


# 检查列表字段是否存在
def find(list, keyword):
    try:
        list.index(keyword)
        return True
    except ValueError:
        return False


# 批量数据时间格式化
def format_dates(items, date_fields):
    for item in items:
        for field in date_fields:
            if field in item and item[field]:
                try:
                    # 如果字段已经是 datetime 对象，就无需解析
                    if isinstance(item[field], datetime):
                        date = item[field]
                    else:
                        # 尝试解析并格式化日期
                        date = parse(item[field])
                    # 使用 strftime 格式化日期
                    item[field] = date.astimezone(tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    # 如果解析失败，保留原来的值
                    pass
    return items
