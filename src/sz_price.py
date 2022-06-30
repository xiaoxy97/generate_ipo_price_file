# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2020/8/4 16:44


import os, math, random
import numpy as np
import pandas as pd

import config


def get_sz_price(today, stock_code, low_limit, up_limit, chg_unit, asset_size_column, price_dict=None):
    """
    生成深证（创业板）的excel
    :param today: 当天日期
    :param stock_code:
    :param low_limit:
    :param up_limit:
    :param asset_size_column:
    :param price_dict:
    """
    print('-' * 100)
    print(stock_code)

    # 找到待填写的原始excel文件（从深交所网站上下载）
    for raw_excel in os.listdir(config.raw_excel_path + today):
        if raw_excel[:6] == stock_code:
            raw_excel_file = raw_excel
            break
    raw_excel_df = pd.read_excel(config.raw_excel_path + today + '/' + raw_excel_file, dtype=str)
    # print(raw_excel_df)

    # 去掉在黑名单内的产品
    limit_products = []
    with open('../data/黑名单.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            limit_products.append(line.strip())
    raw_excel_df = raw_excel_df[~raw_excel_df['配售对象名称'].isin(limit_products)]

    # 给原始excel添加上席位
    tuoguan_dict = {}
    with open(config.tuoguan_file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            tuoguan_dict[line.split('	')[0]] = line.split('	')[1]
    # print(tuoguan_dict)

    raw_excel_df['托管单元（必填）'] = raw_excel_df['证券账号'].map(lambda x: tuoguan_dict[x])
    # print(raw_excel_df['托管单元（必填）'])

    # 填入资产规模
    for assest_size_file in os.listdir(config.raw_asset_size_path + today):
        if assest_size_file[:6] == stock_code:
            raw_assest_size_file = assest_size_file
            break
    try:
        assest_size_df = pd.read_excel(config.raw_asset_size_path + today + '/' + raw_assest_size_file, dtype=str,
                                       index_col='配售对象全称')
    except:
        assest_size_df = pd.read_excel(config.raw_asset_size_path + today + '/' + raw_assest_size_file, dtype=str,
                                       index_col='配售对象名称')
    # print(assest_size_df.columns)

    raw_excel_df['资产规模（万元）'] = raw_excel_df['配售对象名称'].map(
        lambda x: assest_size_df[asset_size_column][x] if x in assest_size_df[asset_size_column] else
        assest_size_df[asset_size_column][x.replace('－', '-')] if x.replace('－', '-') in assest_size_df[
            asset_size_column] else np.nan)
    raw_excel_df.dropna(subset=['资产规模（万元）'], inplace=True)

    # 资产规模由高到低排序
    asset_size_df = raw_excel_df[['配售对象名称', '资产规模（万元）']]
    asset_size_df['资产规模（万元）'] = asset_size_df['资产规模（万元）'].astype('float')
    sorted_asset_size_df = asset_size_df.sort_values(by='资产规模（万元）', ascending=False)
    # print(sorted_asset_size_df)

    # 报价
    price = list(price_dict.keys())
    num = list(price_dict.values())
    # 产品列表，按资产规模由高到低排序
    sorted_product_list = sorted_asset_size_df['配售对象名称'].to_list()

    if len(price) == 1:
        raw_excel_df['申购价格（元）（必填）'] = raw_excel_df['配售对象名称'].map(
            lambda x: price[0] if x in sorted_product_list[:num[0]] else np.nan)
    elif len(price) == 2:
        raw_excel_df['申购价格（元）（必填）'] = raw_excel_df['配售对象名称'].map(
            lambda x: price[0] if x in sorted_product_list[:num[0]] else price[1] if x in sorted_product_list[
                                                                                          num[0]:(num[0] + num[1])] else np.nan)
    elif len(price) == 3:
        raw_excel_df['申购价格（元）（必填）'] = raw_excel_df['配售对象名称'].map(
            lambda x: price[0] if x in sorted_product_list[:num[0]] else price[1] if x in sorted_product_list[
                                                                                          num[0]:(num[0] + num[1])] else
            price[2] if x in sorted_product_list[(num[0] + num[1]):(num[0] + num[1] + num[2])] else np.nan)

    raw_excel_df.dropna(subset=['申购价格（元）（必填）'], inplace=True)

    # raw_excel_df.to_excel(config.output_data_path + today + '/%s.xlsx' % stock_code, index=False)
    raw_excel_df['拟申购数量（万股/万份）（必填）'] = raw_excel_df['资产规模（万元）'].astype('float') / raw_excel_df['申购价格（元）（必填）']

    raw_excel_df['拟申购数量（万股/万份）（必填）'] = raw_excel_df['拟申购数量（万股/万份）（必填）'].map(
        lambda x: up_limit if x >= up_limit else np.nan if x < low_limit else math.floor(x / chg_unit) * chg_unit)
    raw_excel_df['资产规模是否超过本次可申购金额上限（必填）'] = raw_excel_df['拟申购数量（万股/万份）（必填）'].map(
        lambda x: '是' if x == up_limit else '否')

    raw_excel_df.dropna(subset=['拟申购数量（万股/万份）（必填）'], inplace=True)

    # 保存
    raw_excel_df.to_excel(config.output_data_path + today + '/%s.xlsx' % stock_code, index=False)

    # 核对申购价格x拟申购数量是否超过资产规模
    raw_excel_df['状态'] = raw_excel_df['资产规模（万元）'].astype('float') - raw_excel_df['申购价格（元）（必填）'] * raw_excel_df[
        '拟申购数量（万股/万份）（必填）']
    print(raw_excel_df['配售对象名称'][raw_excel_df['状态'] < 0].to_list())
    print(len(raw_excel_df), len(raw_excel_df[raw_excel_df['资产规模是否超过本次可申购金额上限（必填）'] == '是']))
    price_num_dict = {}
    price_list = raw_excel_df['申购价格（元）（必填）'].to_list()
    for price in sorted(set(price_list)):
        price_num_dict[price] = price_list.count(price)
    print(price_num_dict)
