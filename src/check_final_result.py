# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2020/8/20 15:03


import os
import datetime
import pandas as pd

import config


def get_sh_result(today_result_file, stock_code):
    """
    获取沪市询价结果
    :param today_result_file:
    """
    df = pd.read_excel(today_result_file)
    price_list = df['拟申购价格(元)'].to_list()
    price_num_dict = {}
    for price in sorted(set(price_list)):
        price_num_dict[price] = price_list.count(price)
    print(stock_code, price_num_dict)


def get_sz_result(today_result_file, stock_code):
    """
    获取深市询价结果
    :param today_result_file:
    """
    df = pd.read_excel(today_result_file)
    price_list = df['申报价格（元）'].to_list()
    price_num_dict = {}
    for price in sorted(set(price_list)):
        price_num_dict[price] = price_list.count(price)
    print(stock_code, price_num_dict)


def check_today_result():
    """
    核对询价提交结果
    """
    today = datetime.datetime.now().date().strftime('%Y%m%d')
    today_result_path = config.final_result_path + today + '/'

    for file in os.listdir(today_result_path):
        stock_code = file[:6]

        # 科创板
        if stock_code[0] == '6':
            get_sh_result(today_result_file=today_result_path + file, stock_code=stock_code)
        # 创业板
        elif stock_code[0] == '3':
            get_sz_result(today_result_file=today_result_path + file, stock_code=stock_code)


if __name__ == '__main__':
    check_today_result()
