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

    return "'" + str(stock_code) + "':" + str([stock_name, [(round(round(target_mean, 2) + 0.01, 2)),
                                                            (round(round(target_mean, 2) - 0.0, 2)),
                                                            (round(round(target_mean, 2) - 0.01, 2))],
                                               [1, int(product_num - 2), 1]]) + ',\n'


if __name__ == '__main__':
    price = 19.61

    target_price_num = '{'
    # 可编辑区域    # --####('688017', '绿的谐波',  ,
    zhongtai = [price, 0, 0]  # 中泰资管
    guosheng = [price, 0, 0]  # 国盛
    caitong0 = [0, 0, 0]  # 财通
    shenwan1 = [0, 0, 0]  # 申万林
    shenwan2 = [0, 0, 0]  # 申万胡
    zhaoshan = [0, 0, 0]  # 招商
    xingzhen = [0, 0, 0]  # 兴证资管
    xiangcai = [0, 0, 0]  # 湘财
    pingan00 = [0, 0, 0]  # 平安

    all_price_list = [zhongtai, guosheng, caitong0, xiangcai, xingzhen, zhaoshan, shenwan1, shenwan2, pingan00]
    target_price_num += generate_initial_price('688179', '阿拉丁: 34.37', [i[0] for i in all_price_list], 55)

    # ------------------------------------

    print('\n' + '-' * 50 + '\n')
    print(target_price_num[:-2] + '}')
