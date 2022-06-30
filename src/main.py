# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2020/8/4 16:43


import os
import datetime, time

import config
from generate_baojiadan import generate_file
from sz_price import get_sz_price
from sh_price import get_sh_price


def generate_ipo_file(stock_code, low_limit, up_limit, chg_unit, asset_size_column, same_price=None, up_price=None,
                      price_dict=None):
    """
    生成IPO询价提交的excel文件
    :param stock_code: 股票代码
    :param low_limit: 拟申购数量下限   低于下限的产品剔除
    :param up_limit: 拟申购数量上限    高于上限的产品拟申购数量直接填为上限，该产品即为顶格申购产品
    :param asset_size_column: 资产规模的列名
    :param same_price: 所有产品一个价格
    :param up_price: 顶格申购价格，若same_price=None，可以设置up_price
    :param price_dict: 若up_price不为None，除顶格申购产品外其他产品按照price_dict给价格；若up_price=None，所有产品按price_dict给价格
    """
    if datetime.datetime.now().time() <= datetime.time(15, 00, 10):
        today = datetime.datetime.now().date().strftime('%Y%m%d')
        if not os.path.exists(config.output_data_path + today):
            os.mkdir(config.output_data_path + today)

        # t1 = time.time()
        generate_file(stock_code=stock_code, stock_name=generated_price_dict[stock_code][0],
                      price=generated_price_dict[stock_code][1], today=today)
        # print(time.time() - t1)

        # 科创板
        if stock_code[0] == '6':
            get_sh_price(today=today, stock_code=stock_code, low_limit=low_limit, up_limit=up_limit, chg_unit=chg_unit,
                         asset_size_column=asset_size_column, price_dict=price_dict)
        # 创业板
        elif stock_code[0] == '3':
            get_sz_price(today=today, stock_code=stock_code, low_limit=low_limit, up_limit=up_limit, chg_unit=chg_unit,
                         asset_size_column=asset_size_column, price_dict=price_dict)
    else:
        print('超过询价时间')


if __name__ == '__main__':
    """
    # 备份
    generated_price_dict = {'688728': ['格科微', [round(price1 + 0.08, 2), round(price1 + 0.04, 2), price1], [1, 2, 360]],
                            '301048': ['金鹰重工', [round(price2 + 0.02, 2), round(price2 + 0.01, 2), price2], [1, 2, 360]]}
                            {'688728':['格科微: 12.37   EPS: 0.63', [14.5, 14.46, 14.42], [1, 2, 360]],
                             '301048':['金鹰重工:3.46   EPS: 0.352', [4.16, 4.15, 4.14], [1, 2, 360]]}
    """

    # price1 = 8.09  # 金三江    8.5

    generated_price_dict = {'688353':['价格:98.16-117.56 PE:25.71-30.79 华盛锂电', [110.01], [500]]}

    print(generated_price_dict)

    # 688353 华盛锂电  第一次报价为测试能否有效报价   18819431628     91330206308979200J  98.16-117.56
    generate_ipo_file(stock_code='688353', low_limit=50, up_limit=800, chg_unit=10,
                      asset_size_column='总资产或资金规模（万元）',
                      price_dict={price: num for price, num in
                                  zip(generated_price_dict['688353'][1], generated_price_dict['688353'][2])})
