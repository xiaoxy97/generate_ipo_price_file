# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2020/8/13 16:36


import numpy as np
import pandas as pd
import logging


def get_logger(log_file, stream=False):
    """
    生成日志文件
    :param log_file: 日志文件路径
    :param stream: 是否在屏幕显示日志信息 True为显示
    :return:
    用法：
    logger = logger.get_logger(log_file='lr_loss.log')
    logger.info('Epoch {}/{}, loss:{:.4f}'.format(epoch + 1, num_epoches, loss.item()))
    """
    logger = logging.getLogger(name=log_file)
    logger.setLevel(level=logging.DEBUG)
    handler = logging.FileHandler(filename=log_file, encoding='utf-8')
    handler.setLevel(logging.DEBUG)
    format_str = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
    formatter = logging.Formatter(format_str)
    handler.setFormatter(fmt=formatter)
    logger.addHandler(hdlr=handler)

    if stream == True:
        console = logging.StreamHandler()
        console.setFormatter(fmt=formatter)
        console.setLevel(level=logging.INFO)
        logger.addHandler(hdlr=console)
    return logger


# 日志
logger = get_logger('历史报价.txt')


def generate_initial_price(stock_code, stock_name, price_list, product_num):
    """
    第一步：
    根据标准差、中位数、加权数、低均、高均，生成初始价格
    """
    price_list = [i for i in price_list if i != 0]  # 去掉为0的价格

    # 标准差
    price_std = np.std(price_list)
    # if price_std > 0.2:
    #     print('标准差：%s' % round(price_std, 2))

    # 中位数
    price_median = np.median(price_list)

    # 加权数
    # if price_weight:
    #     price_weight_mean = np.array(price_list) * np.array(price_weight) / np.sum(price_weight)
    # else:
    price_weight_mean = np.mean(price_list)

    # 低均
    low_price_mean = (np.sum(price_list) - np.min(price_list)) / (len(price_list) - 1)
    # 高均
    high_price_mean = (np.sum(price_list) - np.max(price_list)) / (len(price_list) - 1)
    # 低均、高均的均值
    custom_mean = (low_price_mean + high_price_mean) / 2

    # 3数平均数
    target_mean = np.mean([price_median, price_weight_mean, custom_mean])

    logger.info('%s, %s, %s, (%s), (%s), (%s)' % (
        stock_code, stock_name, (str(round(price_std, 2)) + ', 宽') if price_std > 0.2 else str(round(price_std, 2)),
        ','.join(str(i) for i in sorted(price_list, reverse=True)),
        ','.join(str(round(i, 2)) for i in [price_median, price_weight_mean, custom_mean]),
        round(target_mean, 2)
    ))

    print('%s, %s, %s, (%s), (%s), (%s)' % (
        stock_code, stock_name, (str(round(price_std, 2)) + ', 宽') if price_std > 0.2 else str(round(price_std, 2)),
        ','.join(str(i) for i in sorted(price_list, reverse=True)),
        ','.join(str(round(i, 2)) for i in [price_median, price_weight_mean, custom_mean]),
        round(target_mean, 2)
    ))

    return "'" + str(stock_code) + "':" + str([stock_name, [round(target_mean, 2)] * 3,
                                               [int(np.floor(product_num * 0.2)),
                                                int(product_num - np.floor(product_num * 0.2) * 2),
                                                int(np.floor(product_num * 0.2))]]) + ',\n'


if __name__ == '__main__':
    target_price_num = '{'

    # 可编辑区域
    # ------------------------------------####('688017', '绿的谐波', [     湘 财,  国盛, 中泰资,兴证,财通，招 商, 平 安 ,
    xiangcai = [120.5, 75, 28.02]  # 湘财
    guosheng = [120.55, 75.03, 28.02]  # 国盛
    zhongtai = [120.5, 75.03, 28.02]  # 中泰资
    xingzheng = [120.5, 75.10, 28.02]  # 兴证
    caitong = [120.65, 75.08, 27.95]  # 财通
    zhaoshang = [0, 75.08, 27.95]  # 招商
    pingan = [0, 0, 0]  # 平安

    all_price_list = [xiangcai, guosheng, zhongtai, xingzheng, caitong, zhaoshang, pingan]
    logger.info(all_price_list)
    target_price_num += generate_initial_price('688301', '奕瑞科技: 89.99', [i[0] for i in all_price_list], 48)
    target_price_num += generate_initial_price('300888', '稳健医疗: 55.55', [i[1] for i in all_price_list], 53)
    target_price_num += generate_initial_price('300889', '爱克股份: 27.82', [i[2] for i in all_price_list], 54)

    # target_price_num += generate_initial_price('688301', '奕瑞科技: 89.99', [120.5, 120.55, 120.5, 120.5, 120.65], 48)
    # target_price_num += generate_initial_price('300888', '稳健医疗: 55.55', [75, 75.03, 75.03, 75.10, 75.08, 75.08], 53)
    # target_price_num += generate_initial_price('300889', '爱克股份: 27.82',
    #                                            [28.02, 28.02, 28.02, 28.02, 27.95, 27.95], 54)

    # ------------------------------------

    print('\n' + '-' * 50 + '\n')
    print(target_price_num[:-2] + '}')
