# -*- coding: utf-8 -*-
#指数平滑算法
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
def exponential_smoothing(alpha, s):
    '''
    一次指数平滑
    :param alpha:  平滑系数
    :param s:      数据序列， list
    :return:       返回一次指数平滑模型参数， list
    '''
    s_temp = [0 for i in range(len(s))]
    s_temp[0] = ( s[0] + s[1] + s[2] ) / 3
    for i in range(1, len(s)):
        s_temp[i] = alpha * s[i] + (1 - alpha) * s_temp[i-1]
    return s_temp

def compute_single(alpha, s):
    '''
    一次指数平滑
    :param alpha:  平滑系数
    :param s:      数据序列， list
    :return:       返回一次指数平滑模型参数， list
    '''
    return exponential_smoothing(alpha, s)

def compute_double(alpha, s):
    '''
    二次指数平滑
    :param alpha:  平滑系数
    :param s:      数据序列， list
    :return:       返回二次指数平滑模型参数a, b， list
    '''
    s_single = compute_single(alpha, s)
    s_double = compute_single(alpha, s_single)

    a_double = [0 for i in range(len(s))]
    b_double = [0 for i in range(len(s))]

    for i in range(len(s)):
        a_double[i] = 2 * s_single[i] - s_double[i]                    #计算二次指数平滑的a
        b_double[i] = (alpha / (1 - alpha)) * (s_single[i] - s_double[i])  #计算二次指数平滑的b

    return a_double, b_double

def compute_triple(alpha, s):
    '''
    三次指数平滑
    :param alpha:  平滑系数
    :param s:      数据序列， list
    :return:       返回三次指数平滑模型参数a, b, c， list
    '''
    s_single = compute_single(alpha, s)
    s_double = compute_single(alpha, s_single)
    s_triple = exponential_smoothing(alpha, s_double)

    a_triple = [0 for i in range(len(s))]
    b_triple = [0 for i in range(len(s))]
    c_triple = [0 for i in range(len(s))]

    for i in range(len(s)):
        a_triple[i] = 3 * s_single[i] - 3 * s_double[i] + s_triple[i]
        b_triple[i] = (alpha / (2 * ((1 - alpha) ** 2))) * ((6 - 5 * alpha) * s_single[i] - 2 * ((5 - 4 * alpha) * s_double[i]) + (4 - 3 * alpha) * s_triple[i])
        c_triple[i] = ((alpha ** 2) / (2 * ((1 - alpha) ** 2))) * (s_single[i] - 2 * s_double[i] + s_triple[i])

    return a_triple, b_triple, c_triple

def show_data(date,true,s_pre_triple):

    plt.figure(figsize=(14, 6), dpi=80)#设置绘图区域的大小和像素
    plt.subplot(211)
    plt.plot(date[:-1], true, color='blue', label="actual value")#将实际值的折线设置为蓝色
    plt.title('true data')
    plt.ylabel('price')#y轴标签
    plt.subplot(212)
    plt.plot(date[1:], s_pre_triple,color='red', label="triple predicted value")#将三次指数平滑法计算的预测值的折线设置为绿色
    plt.title('predict data')
    plt.ylabel('price')#y轴标签
    plt.show()

if __name__ == "__main__":

    alpha = 0.8
    data = pd.read_csv("123.csv")
    price=data['price']
    date=data['date']
    datePlus=np.append(date.to_numpy(), "2020/6/5", axis=None)
    del date
    a_triple, b_triple, c_triple = compute_triple(alpha,price)
    triPrice=np.zeros(price.shape)
    for i in range(len(triPrice)):
        triPrice[i]=a_triple[i]+b_triple[i]+c_triple[i]
    show_data(datePlus,price,triPrice)