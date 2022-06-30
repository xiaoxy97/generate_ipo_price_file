# -*- coding: utf-8 -*-
# @author: xiaoxy
# @time: 2020/8/13 13.5:36


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
    if len(price_list) == 1:
        logger.info('%s, %s, %s, (%s), (%s), (%s)' % (
            stock_code, stock_name, 0, (round(price_list[0], 2)), (round(price_list[0], 2)), (round(price_list[0], 2))
        ))

        print('%s, %s, %s, (%s), (%s), (%s)' % (
            stock_code, stock_name, 0, (round(price_list[0], 2)), (round(price_list[0], 2)), (round(price_list[0], 2))
        ))

        return "'" + str(stock_code) + "':" + str([stock_name, [round(price_list[0], 2)], [int(product_num)]]) + ',\n'

    elif len(price_list) == 2:
        sorted_price_list = sorted(price_list, reverse=True)  # 价格由高到低排序
        # 标准差
        price_std = np.std(price_list)

        # 两数平均数
        target_mean = np.mean(price_list)

        logger.info('%s, %s, %s, (%s), (%s), (%s)' % (
            stock_code, stock_name, (str(round(price_std, 2)) + ', 宽') if price_std > 0.2 else str(round(price_std, 2)),
            ','.join(str(i) for i in sorted(price_list, reverse=True)),
            ','.join(str(round(i, 2)) for i in [target_mean, target_mean, sorted_price_list[0], sorted_price_list[1]]),
            round(target_mean, 2)
        ))

        print('%s, %s, %s, (%s), (%s), (%s)' % (
            stock_code, stock_name, (str(round(price_std, 2)) + ', 宽') if price_std > 0.2 else str(round(price_std, 2)),
            ','.join(str(i) for i in sorted(price_list, reverse=True)),
            ','.join(str(round(i, 2)) for i in [target_mean, target_mean, sorted_price_list[0], sorted_price_list[1]]),
            round(target_mean, 2)
        ))

        return "'" + str(stock_code) + "':" + str([stock_name, [(round(round(target_mean, 2) - 0.0, 2))],
                                                   [int(product_num)]]) + ',\n'

    else:
        sorted_price_list = sorted(price_list, reverse=True)  # 价格由高到低排序

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
        # low_price_mean = (np.sum(price_list)) / (len(price_list))
        # low_price_mean = (np.sum(price_list) - np.min(price_list)) / (len(price_list) - 1)
        # 高均
        high_price_mean = (np.sum(price_list) - np.max(price_list) - np.min(price_list)) / (len(price_list) - 2)
        # 低均、高均的均值
        custom_mean = (high_price_mean)
        # custom_mean = (6*low_price_mean + high_price_mean) /7

        # 3数平均数
        target_mean = np.mean([price_median, custom_mean, sorted_price_list[2], sorted_price_list[3]])
        # target_mean = np.mean([price_median, price_weight_mean, custom_mean])

        logger.info('%s, %s, %s, (%s), (%s), (%s)' % (
            stock_code, stock_name, (str(round(price_std, 2)) + ', 宽') if price_std > 0.2 else str(round(price_std, 2)),
            ','.join(str(i) for i in sorted(price_list, reverse=True)),
            ','.join(str(round(i, 3)) for i in [price_median, custom_mean, sorted_price_list[2], sorted_price_list[3]]),
            round(target_mean, 3)
        ))

        print('%s, %s, %s, (%s), (%s), (%s)' % (
            stock_code, stock_name, (str(round(price_std, 2)) + ', 宽') if price_std > 0.2 else str(round(price_std, 2)),
            ','.join(str(i) for i in sorted(price_list, reverse=True)),
            ','.join(str(round(i, 3)) for i in [price_median, custom_mean, sorted_price_list[2], sorted_price_list[3]]),
            round(target_mean, 3)
        ))

        return "'" + str(stock_code) + "':" + str([stock_name, [(round(round(target_mean, 2) - 0.0, 2))],
                                                   [int(product_num)]]) + ',\n'


if __name__ == '__main__':
    target_price_num = '{'
    # 可编辑区域    # --####('688017', '绿的谐波',  ,
    #a = [1南极光: 11.33 EPS: 0.65, 2聚石化学, 3海优新材, 4银河微电]  
    a1 = [12.79, 0, 0, 0]   # 国盛
    a2 = [12.78, 0, 0, 0]    # 九章
    a3 = [12.79, 0, 0, 0]  # 财通
    a4 = [12.79, 0, 0, 0]  # 东吴
    a5 = [12.78, 0, 0, 0]  # 华泰资管
    a6 = [12.78, 0, 0, 0]  # 源乐晟
    a7 = [12.78, 0, 0, 0]  # 兴证资管
    a8 = [0, 0, 0, 0]  # 湘财，申万
    a9 = [0, 0, 0, 0]  # 长江，平安，国泰君安
    b1 = [0, 0, 0, 0]  # 国联
    b2 = [0, 0, 0, 0]  # 乐瑞，华创，广发




    all_price_list = [a1, a2, a3, a4, a5, a6, a7, a8, a9, b1, b2]
    target_price_num += generate_initial_price('300940', '300940 南极光: 11.33 EPS: 0.65', [i[0] for i in all_price_list], 360)
    #target_price_num += generate_initial_price('688669', '聚石化学: 35 EPS: 1.95', [i[1] for i in all_price_list], 360)
    #target_price_num += generate_initial_price('688680', '海优新材: 70 EPS: 2.56', [i[2] for i in all_price_list], 360)
    #target_price_num += generate_initial_price('688689', '银河微电: 14.04 EPS: 0.47', [i[3] for i in all_price_list], 360)

    # ------------------------------------

    print('\n' + '-' * 50 + '\n')
    print(target_price_num[:-2] + '}')
