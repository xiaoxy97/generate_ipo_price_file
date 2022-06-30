# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2020/8/12 10:15


import os, datetime
import pandas as pd

import config


def get_sz_price(today, stock_code, up_limit):
    """
    生成深证（主板中小板）的excel
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

    # 给原始excel添加上席位
    tuoguan_dict = {}
    with open(config.tuoguan_file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            tuoguan_dict[line.split('	')[0]] = line.split('	')[1]
    # print(tuoguan_dict)

    raw_excel_df['托管单元（必填）'] = raw_excel_df['证券账号'].map(lambda x: tuoguan_dict[x])
    # print(raw_excel_df['托管单元（必填）'])

    raw_excel_df['拟申购数量（万股/万份）（必填）'] = up_limit

    # 保存
    raw_excel_df.to_excel(config.output_data_path + today + '/%s.xlsx' % stock_code, index=False)


if __name__ == '__main__':
    today = datetime.datetime.now().date().strftime('%Y%m%d')
    if not os.path.exists(config.output_data_path + today):
        os.mkdir(config.output_data_path + today)
    get_sz_price(today=today, stock_code='001313', up_limit=1200)
