import pandas as pd
import numpy as np
import requests
import json
import time
import datetime

import sympy

from program.option.config import *

pd.set_option('display.max_rows', 1000)
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行

# ====计算单张期权合约的交易费用
def cal_trade_fee(premium, coin, fee_rate=2/10000, fee_limit=12.5/100):
    '''
    计算期权交易费用。行权交易费用另行计算
    :param premium: 权利金
    :param coin: btc eth eos
    :param fee_rate: 费率。挂单：0.02%；吃单：0.05%
    :param fee_limit: 交易费用上限，不超过权利金的12.5%
    :return:
    '''

    multiplier = coin_value_table[coin]
    fee = min(fee_rate * multiplier, premium * multiplier * fee_limit)

    return fee


# ====获取合约名称
def get_instrument(coin):
    url = 'https://www.okex.com/api/v5/public/instruments?instType=OPTION&uly={}-USD'.format(coin.upper())
    html = requests.get(url).text
    contents = json.loads(html)
    instrument_df = pd.DataFrame(contents['data'])

    # 转换日期格式
    for col in ['expTime', 'listTime']:
        instrument_df[col] = instrument_df[col].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x)/1000)))

    return instrument_df


# ====获取期权数据，比如greeks
def get_stat_data(symbol):
    '''
    获取期权数据，比如greeks
    https://www.okex.com/docs-v5/zh/#rest-api-public-data-get-option-market-data

    :param coin: BTC-USD-210409-60000-C
    :return:
    '''

    coin, expTime = symbol.split('-')[0], symbol.split('-')[2]
    url = 'https://www.okex.com/api/v5/public/opt-summary?expTime={}&uly={}-USD'.format(expTime, coin.upper())
    html = requests.get(url).text
    contents = json.loads(html)
    trade = pd.DataFrame(contents['data'])

    # 转换数据格式
    trade['ts'] = trade['ts'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x) / 1000)))
    trade = trade[trade['instId']==symbol]
    # trade = trade[['askVol','bidVol','delta','deltaBS','gamma','gammaBS','lever','markVol','realVol','theta','thetaBS', 'vega','vegaBS']]
    # trade = trade.astype('float')

    return trade


# ====期权多头greeks
def get_greeks(symbol):
    stat_data = get_stat_data(symbol)

    df_greeks = pd.DataFrame()
    for _ in ['delta','gamma','theta','vega']:
        df_greeks.loc[_, 'PA'] = float(stat_data[_].iloc[0])  # 币本位
        df_greeks.loc[_, 'BS'] = float(stat_data['%sBS' % _].iloc[0])  # U本位

    return df_greeks


# ====获取行情数据
def get_trade_data(instId):
    '''
    https://www.okex.com/docs-v5/zh/#rest-api-market-data-get-ticker
    :param coin: btc eth eos
    :return:
    '''
    url = 'https://www.okex.com/api/v5/market/ticker?instId={}'.format(instId)
    html = requests.get(url).text
    contents = json.loads(html)
    trade = pd.DataFrame(contents['data'])
    # 转换数据格式
    trade['ts'] = trade['ts'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x) / 1000)))

    return trade

def get_premium(symbol):
    '''
    https://www.okex.com/v3/option/pc/public/BTC-USD-210410-55000-P/depth?t=1617951141971
    :param coin:
    :return: 买一价，卖一价
    '''
    now = int(time.time() * 1000)  # okex需要13位时间戳
    url = 'https://www.okex.com/v3/option/pc/public/{}/depth?t={}'.format(symbol, now)
    html = requests.get(url).text
    contents = json.loads(html)
    # 买一
    best_bid = float(contents['data']['bids'][0][0])
    # 卖一
    best_ask = float(contents['data']['asks'][0][0])

    return best_bid, best_ask


# ==获取期权标记价格
def get_mark_price(instId):
    url = 'https://www.okex.com/api/v5/public/mark-price?instType=OPTION&instId={}'.format(instId)
    html = requests.get(url).text
    contents = json.loads(html)
    trade = pd.DataFrame(contents['data'])
    # 转换数据格式
    trade['ts'] = trade['ts'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x) / 1000)))

    return trade


# ==获取现货指数
def get_index_price(coin):
    url = 'https://www.okex.com/api/v5/market/index-tickers?instId={}-USD'.format(coin.upper())
    html = requests.get(url).text
    contents = json.loads(html)
    trade = pd.DataFrame(contents['data'])
    # 转换数据格式
    trade['ts'] = trade['ts'].apply(lambda x: time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(x) / 1000)))

    return trade



# ====计算期权到期收益
# ==计算call回报（不算权利金）
def call_profit(spot_price, strike_price, coin):
    multiplier = coin_value_table[coin]
    return max(spot_price - strike_price, 0) * multiplier / spot_price

# ==计算put回报（不算权利金）
def put_profit(spot_price, strike_price, coin):
    multiplier = coin_value_table[coin]
    return max(strike_price - spot_price, 0) * multiplier / spot_price


# ====画到期损益图
def plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, col='USDT'):
    import matplotlib.pyplot as plt
    import matplotlib
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    x = df.index.astype('int')
    y1 = df['总收益(%s)' % col]

    fig = plt.figure(figsize=[16, 8])
    plt.plot(x, y1, label=col)
    plt.scatter(breakeven_price, 0, color='', marker='o', edgecolors='r', s=100)  # 盈亏平衡价格
    plt.text(breakeven_price, 10, '%.2f' % breakeven_price)
    plt.vlines(spot_price_index, ymin=min(y1), ymax=max(y1), colors='orange', linestyles='-', label='spot')
    plt.text(spot_price_index, max(y1), '%.2f' % spot_price_index)
    plt.hlines(0, xmin=min(x), xmax=max(x), colors='black', linestyles='--')
    plt.title('构建收益：%s\n最大收益：%s  最大收益价格：%s\n最大损失：%s  最大损失价格：%s' % (init_income, max_profit, max_profit_price, max_loss, max_loss_price))
    plt.legend()
    plt.grid()
    plt.show()

def plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, col='USDT'):
    import matplotlib.pyplot as plt
    import matplotlib
    # 设置matplotlib正常显示中文和负号
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    matplotlib.rcParams['axes.unicode_minus'] = False  # 正常显示负号

    x = df.index.astype('int')
    y1 = df['总收益(%s)' % col]

    fig = plt.figure(figsize=[16, 8])
    plt.plot(x, y1, label=col)
    plt.scatter(breakeven_price1, 0, color='', marker='o', edgecolors='r', s=100)  # 盈亏平衡价格
    plt.text(breakeven_price1, 10, '%.2f' % breakeven_price1)
    plt.scatter(breakeven_price2, 0, color='', marker='o', edgecolors='r', s=100, label='breakeven')  # 盈亏平衡价格
    plt.text(breakeven_price2, 10, '%.2f' % breakeven_price2)
    plt.vlines(spot_price_index, ymin=min(y1), ymax=max(y1), colors='orange', linestyles='-', label='spot')
    plt.text(spot_price_index, max(y1), '%.2f' % spot_price_index)
    plt.hlines(0, xmin=min(x), xmax=max(x), colors='black', linestyles='--')
    plt.title('构建收益：%s\n最大收益：%s  最大收益价格：%s\n最大损失：%s  最大损失价格：%s' % (init_income, max_profit, max_profit_price, max_loss, max_loss_price))
    plt.legend()
    plt.grid()
    plt.show()


# ====求一元一次方程，主要用来计算盈亏平衡
def cal_breakeven_price(equation, x=sympy.symbols('x')):
    '''

    :param equation: [5*sympy.symbols('x')+1]
    :param x:
    :return:
    '''
    rtn = sympy.solve(equation, [x])[x]

    return float(rtn)
