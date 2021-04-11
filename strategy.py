from program.option.functions import *
from program.option.config import *
import matplotlib.pyplot as plt


# ====单腿
# ==买call
def long_call(coin, strike, exptime, interval=100):

    # ==基础数据准备
    call_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, strike)
    multiplier = coin_value_table[coin]
    buy_c_pre = float(get_trade_data(call_symbol)['askPx'])  # 权利金，卖一
    buy_c_fee = cal_trade_fee(buy_c_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (- buy_c_pre * multiplier - buy_c_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = 'infinite'  # 最大盈利
    max_profit_price = 'infinite'  # 获取最大盈利价格
    max_loss = init_income
    max_loss_price = ' '
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([(x - strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(strike * 1.5), int(strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        buy_c_profit = call_profit(spot_price, strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = buy_c_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price
    # print(df)
    # ==greeks
    buy_greeks = get_greeks(call_symbol)
    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (buy_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (buy_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (buy_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (buy_greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, 'USDT')

# ==卖call
def short_call(coin, strike, exptime, interval=100):

    # ==基础数据准备
    call_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, strike)
    multiplier = coin_value_table[coin]
    c_pre = float(get_trade_data(call_symbol)['askPx'])  # 权利金，卖一
    c_fee = cal_trade_fee(c_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (c_pre * multiplier - c_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = init_income  # 最大盈利
    max_profit_price = ' '  # 获取最大盈利价格
    max_loss = 'infinite'
    max_loss_price = 'infinite'
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([- (x - strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(strike * 1.5), int(strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_c_profit = - call_profit(spot_price, strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = sell_c_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price
    # print(df)
    # ==greeks
    buy_greeks = get_greeks(call_symbol)
    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (-buy_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (-buy_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (-buy_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (-buy_greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, 'USDT')

# ==买put
def long_put(coin, strike, exptime, interval=100):

    # ==基础数据准备
    put_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, strike)
    multiplier = coin_value_table[coin]
    p_pre = float(get_trade_data(put_symbol)['askPx'])  # 权利金，卖一
    p_fee = cal_trade_fee(p_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (- p_pre * multiplier - p_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = 'infinite'  # 最大盈利
    max_profit_price = 'infinite'  # 获取最大盈利价格
    max_loss = init_income
    max_loss_price = ''
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([(strike - x) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(strike * 1.2), int(strike * 0.5)

    for spot_price in range(min_price, max_pice, interval):
        profit = put_profit(spot_price, strike, coin)
        df.loc[str(spot_price), '总收益(币本位)'] = profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price
    # print(df)
    # ==greeks
    greeks = get_greeks(put_symbol)
    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, 'USDT')

# ==卖put
def short_put(coin, strike, exptime, interval=100):

    # ==基础数据准备
    put_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, strike)
    multiplier = coin_value_table[coin]
    p_pre = float(get_trade_data(put_symbol)['askPx'])  # 权利金，卖一
    p_fee = cal_trade_fee(p_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (p_pre * multiplier - p_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = init_income  # 最大盈利
    max_profit_price = ''  # 获取最大盈利价格
    max_loss = 'infinite'
    max_loss_price = 'infinite'
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([- (strike - x) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(strike * 1.2), int(strike * 0.5)

    for spot_price in range(min_price, max_pice, interval):
        profit = - put_profit(spot_price, strike, coin)
        df.loc[str(spot_price), '总收益(币本位)'] = profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price
    # print(df)
    # ==greeks
    greeks = get_greeks(put_symbol)
    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (-greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (-greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (--greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (-greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, 'USDT')



# ====牛熊价差
def bull_put_spread(coin, high_strike, low_strike, exptime, interval=100, unit='USDT'):
    '''
    买入低行权价put，卖出高行权价put
    权利金净收入
    :param coin: btc小写
    :param high_strike: int   eos是float
    :param low_strike: int
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''

    # ==基础数据准备
    buy_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, low_strike)
    sell_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, high_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    sell_fee = cal_trade_fee(sell_pre, coin)  # 期权交易费用
    buy_fee = cal_trade_fee(buy_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * multiplier - buy_pre * multiplier - sell_fee - buy_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = init_income  # 最大盈利
    max_profit_price = high_strike  # 获取最大盈利价格
    max_loss = (high_strike - low_strike) * multiplier - init_income
    max_loss_price = low_strike
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([- (high_strike-x) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_profit = - put_profit(spot_price, high_strike, coin)
        buy_profit = put_profit(spot_price, low_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = buy_profit + sell_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    buy_greeks = get_greeks(buy_symbol)
    sell_greeks = get_greeks(sell_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (buy_greeks.loc['delta', 'PA'] - sell_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (buy_greeks.loc['gamma', 'PA'] - sell_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (buy_greeks.loc['vega', 'PA'] - sell_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (buy_greeks.loc['theta', 'PA'] - sell_greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, unit)

def bull_call_spread(coin, high_strike, low_strike, exptime, interval=100, unit='USDT'):
    '''
    买入低行权价call，卖出高行权价call
    权利金净支出
    :param coin: btc小写
    :param high_strike: int   eos是float
    :param low_strike: int
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''


    # ==基础数据准备
    buy_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, low_strike)
    sell_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, high_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    sell_fee = cal_trade_fee(sell_pre, coin)  # 期权交易费用
    buy_fee = cal_trade_fee(buy_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * multiplier - buy_pre * multiplier - sell_fee - buy_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = (high_strike - low_strike) * multiplier + init_income
    max_profit_price = high_strike
    max_loss = init_income
    max_loss_price = low_strike
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([(x - low_strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_profit = - call_profit(spot_price, high_strike, coin)
        buy_profit = call_profit(spot_price, low_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = buy_profit + sell_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    buy_greeks = get_greeks(buy_symbol)
    sell_greeks = get_greeks(sell_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (buy_greeks.loc['delta', 'PA'] - sell_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (buy_greeks.loc['gamma', 'PA'] - sell_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (buy_greeks.loc['vega', 'PA'] - sell_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (buy_greeks.loc['theta', 'PA'] - sell_greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, unit)

def bear_put_spread(coin, high_strike, low_strike, exptime, interval=100, unit='USDT'):
    '''
    买入高行权价put，卖出低行权价put
    :param coin: btc小写
    :param high_strike: int   eos是float
    :param low_strike: int
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''


    # ==基础数据准备
    buy_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, high_strike)
    sell_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, low_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    sell_fee = cal_trade_fee(sell_pre, coin)  # 期权交易费用
    buy_fee = cal_trade_fee(buy_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * multiplier - buy_pre * multiplier - sell_fee - buy_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = (high_strike - low_strike) * multiplier + init_income  # 最大盈利
    max_profit_price = low_strike  # 获取最大盈利价格
    max_loss = init_income
    max_loss_price = high_strike
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([(high_strike-x) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_profit = - put_profit(spot_price, low_strike, coin)
        buy_profit = put_profit(spot_price, high_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = buy_profit + sell_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    buy_greeks = get_greeks(buy_symbol)
    sell_greeks = get_greeks(sell_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (buy_greeks.loc['delta', 'PA'] - sell_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (buy_greeks.loc['gamma', 'PA'] - sell_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (buy_greeks.loc['vega', 'PA'] - sell_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (buy_greeks.loc['theta', 'PA'] - sell_greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, unit)

def bear_call_spread(coin, high_strike, low_strike, exptime, interval=100, unit='USDT'):
    '''
    买入高行权价call，卖出低行权价call
    :param coin: btc小写
    :param high_strike: int   eos是float
    :param low_strike: int
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''


    # ==基础数据准备
    buy_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, high_strike)
    sell_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, low_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    sell_fee = cal_trade_fee(sell_pre, coin)  # 期权交易费用
    buy_fee = cal_trade_fee(buy_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * multiplier - buy_pre * multiplier - sell_fee - buy_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = init_income
    max_profit_price = low_strike
    max_loss = (high_strike - low_strike) * multiplier - init_income
    max_loss_price = high_strike
    x = sympy.symbols('x')
    breakeven_price = cal_breakeven_price([- (x - low_strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_profit = - call_profit(spot_price, low_strike, coin)
        buy_profit = call_profit(spot_price, high_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = buy_profit + sell_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    buy_greeks = get_greeks(buy_symbol)
    sell_greeks = get_greeks(sell_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (buy_greeks.loc['delta', 'PA'] - sell_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (buy_greeks.loc['gamma', 'PA'] - sell_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (buy_greeks.loc['vega', 'PA'] - sell_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (buy_greeks.loc['theta', 'PA'] - sell_greeks.loc['theta', 'PA']))
    plot_PL_charts_1breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index, unit)



# ====跨式
def long_straddles(coin, strike, exptime, interval=100, unit='USDT'):
    '''
    同时买入相同行权价和到期日的call和put
    :param coin: btc小写
    :param strike: int   eos是float
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''

    # ==基础数据准备
    call_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, strike)
    put_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, strike)
    multiplier = coin_value_table[coin]

    call_pre = get_premium(call_symbol)[1]
    put_pre = get_premium(put_symbol)[1]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    call_fee = cal_trade_fee(call_pre, coin)  # 期权交易费用
    put_fee = cal_trade_fee(put_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (- call_pre * multiplier - put_pre * multiplier - call_fee - put_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = 'infinite'
    max_profit_price = 'infinite'
    max_loss = init_income
    max_loss_price = strike
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([(strike - x) * multiplier / x + init_income / spot_price_index])
    breakeven_price2 = cal_breakeven_price([(x - strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(strike * 1.2), int(strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        c_profit = call_profit(spot_price, strike, coin)
        p_profit = put_profit(spot_price, strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = c_profit + p_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    call_greeks = get_greeks(call_symbol)
    put_greeks = get_greeks(put_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (call_greeks.loc['delta', 'PA'] + put_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (call_greeks.loc['gamma', 'PA'] + put_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (call_greeks.loc['vega', 'PA'] + put_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (call_greeks.loc['theta', 'PA'] + put_greeks.loc['theta', 'PA']))
    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)

def short_straddles(coin, strike, exptime, interval=100, unit='USDT'):
    '''
    同时卖出相同行权价和到期日的call和put
    :param coin: btc小写
    :param strike: int   eos是float
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''

    # ==基础数据准备
    call_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, strike)
    put_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, strike)
    multiplier = coin_value_table[coin]

    call_pre = get_premium(call_symbol)[0]
    put_pre = get_premium(put_symbol)[0]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    call_fee = cal_trade_fee(call_pre, coin)  # 期权交易费用
    put_fee = cal_trade_fee(put_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (call_pre * multiplier + put_pre * multiplier - call_fee - put_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = init_income
    max_profit_price = strike
    max_loss = 'infinite'
    max_loss_price = 'infinite'
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([- (strike - x) * multiplier / x + init_income / spot_price_index])
    breakeven_price2 = cal_breakeven_price([- (x - strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(strike * 1.2), int(strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        c_profit = - call_profit(spot_price, strike, coin)
        p_profit = - put_profit(spot_price, strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = c_profit + p_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    call_greeks = get_greeks(call_symbol)
    put_greeks = get_greeks(put_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % - (call_greeks.loc['delta', 'PA'] + put_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % - (call_greeks.loc['gamma', 'PA'] + put_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % - (call_greeks.loc['vega', 'PA'] + put_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % - (call_greeks.loc['theta', 'PA'] + put_greeks.loc['theta', 'PA']))
    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)

def long_strangle(coin, c_strike, p_strike, exptime, interval=100, unit='USDT'):
    '''
    同时买入不同同行权价和到期日的call和put
    :param coin: btc小写
    :param c_strike: int   eos是float, call行权价
    :param p_strike: int   eos是float, put行权价
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''

    # ==基础数据准备
    call_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, c_strike)
    put_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, p_strike)
    multiplier = coin_value_table[coin]

    call_pre = get_premium(call_symbol)[1]
    put_pre = get_premium(put_symbol)[1]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    call_fee = cal_trade_fee(call_pre, coin)  # 期权交易费用
    put_fee = cal_trade_fee(put_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (- call_pre * multiplier - put_pre * multiplier - call_fee - put_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = 'infinite'
    max_profit_price = 'infinite'
    max_loss = init_income
    max_loss_price = '%s - %s' % (p_strike, c_strike)
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([(p_strike - x) * multiplier / x + init_income / spot_price_index])
    breakeven_price2 = cal_breakeven_price([(x - c_strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(c_strike * 1.2), int(p_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        c_profit = call_profit(spot_price, c_strike, coin)
        p_profit = put_profit(spot_price, p_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = c_profit + p_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    call_greeks = get_greeks(call_symbol)
    put_greeks = get_greeks(put_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (call_greeks.loc['delta', 'PA'] + put_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (call_greeks.loc['gamma', 'PA'] + put_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (call_greeks.loc['vega', 'PA'] + put_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (call_greeks.loc['theta', 'PA'] + put_greeks.loc['theta', 'PA']))
    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)

def short_strangle(coin, c_strike, p_strike, exptime, interval=100, unit='USDT'):
    '''
    同时卖出不同行权价和到期日的call和put
    :param coin: btc小写
    :param strike: int   eos是float
    :param exptime: 210410
    :param interval: 根据行权价纲量确定interval
    :param unit: USDT, 币本位
    :return:
    '''

    # ==基础数据准备
    call_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, c_strike)
    put_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, p_strike)
    multiplier = coin_value_table[coin]

    call_pre = get_premium(call_symbol)[0]
    put_pre = get_premium(put_symbol)[0]
    # buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    # sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    call_fee = cal_trade_fee(call_pre, coin)  # 期权交易费用
    put_fee = cal_trade_fee(put_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (call_pre * multiplier + put_pre * multiplier - call_fee - put_fee) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = init_income
    max_profit_price = '%s - %s' % (p_strike, c_strike)
    max_loss = 'infinite'
    max_loss_price = 'infinite'
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([- (p_strike - x) * multiplier / x + init_income / spot_price_index])
    breakeven_price2 = cal_breakeven_price([- (x - c_strike) * multiplier / x + init_income / spot_price_index])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(c_strike * 1.2), int(p_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        c_profit = - call_profit(spot_price, c_strike, coin)
        p_profit = - put_profit(spot_price, p_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '总收益(币本位)'] = c_profit + p_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    # ==greeks
    call_greeks = get_greeks(call_symbol)
    put_greeks = get_greeks(put_symbol)

    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % - (call_greeks.loc['delta', 'PA'] + put_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % - (call_greeks.loc['gamma', 'PA'] + put_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % - (call_greeks.loc['vega', 'PA'] + put_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % - (call_greeks.loc['theta', 'PA'] + put_greeks.loc['theta', 'PA']))
    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)



# ====比例价差
def long_call_ratio_spread(coin, high_strike, low_strike, exptime, ratio=2, interval=100, unit='USDT'):
    '''
    比例价差多头
    买入n份较高行权价/到期日相同的看涨期权，权利金低
    卖出1份较低行权价/到期日相同的看涨期权，权利金高
    初始交易可能为正或负
    :param coin: btc eth eos
    :param high_strike: int 较高行权价
    :param low_strike: int 较低行权价
    :param exptime: 到期日  210402
    :param ratio: n
    :param interval: Scenario analysis中，现货的间隔，btc取100，eth取10，eos取1.也可以自定义
    :return:
    '''

    # ==基础数据准备
    buy_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, high_strike)  # 买入n份较高行权价call
    sell_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, low_strike)  # 卖出1份较低行权价call
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # buy_c_pre = float(get_trade_data(buy_call_symbol)['askPx'])  # 权利金，卖一
    # sell_c_pre = float(get_trade_data(sell_call_symbol)['bidPx'])  # 权利金，买一
    sell_fee = cal_trade_fee(sell_pre, coin)  # 期权交易费用
    buy_fee = cal_trade_fee(buy_pre, coin)  # 期权交易费用
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * multiplier - buy_pre * ratio * multiplier - sell_fee - buy_fee * ratio) * spot_price_index  # 初始构建策略的收入，如果为正，则代表净权利金收入；为负权利金净流出
    max_profit = 'infinite'  # 最大盈利
    max_profit_price = 'infinite'  # 获取最大盈利价格
    max_loss = init_income - (high_strike - low_strike) * multiplier
    max_loss_price = high_strike
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([(x-high_strike) * ratio * multiplier / x + init_income / spot_price_index - (x-low_strike) * multiplier / x])
    breakeven_price2 = cal_breakeven_price([init_income / spot_price_index - (x-low_strike) * multiplier / x])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_c_profit = - call_profit(spot_price, low_strike, coin)
        buy_c_profit = call_profit(spot_price, high_strike, coin) * ratio
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '卖出call收益'] = sell_c_profit
        df.loc[str(spot_price), '买入call收益'] = buy_c_profit
        df.loc[str(spot_price), '总收益(币本位)'] = buy_c_profit + sell_c_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price
    # print('策略到期收益:')
    # print(df)
    # print()

    # ==greeks
    buy_greeks = get_greeks(buy_symbol)
    sell_greeks = get_greeks(sell_symbol)
    print('策略Greeks(PA)：')
    print('\tDelta: %.4f' % (buy_greeks.loc['delta', 'PA']*ratio - sell_greeks.loc['delta', 'PA']))
    print('\tGamma: %.4f' % (buy_greeks.loc['gamma', 'PA']*ratio - sell_greeks.loc['gamma', 'PA']))
    print('\tVega: %.4f' % (buy_greeks.loc['vega', 'PA']*ratio - sell_greeks.loc['vega', 'PA']))
    print('\tTheta: %.4f' % (buy_greeks.loc['theta', 'PA']*ratio - sell_greeks.loc['theta', 'PA']))
    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)
    # return df, init_cost, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index


def short_call_ratio_spread(coin, high_strike, low_strike, exptime, ratio=2, interval=100, unit='USDT'):
    '''
    比例价差空头
    卖出n份较高行权价/到期日相同的看涨期权，权利金低
    买入1份较低行权价/到期日相同的看涨期权，权利金高
    初始交易可能为正或负
    :param coin: btc eth eos
    :param high_strike: int 较高行权价
    :param low_strike: int 较低行权价
    :param exptime: 到期日  210402
    :param ratio: n
    :param interval: Scenario analysis中，现货的间隔，btc取100，eth取10，eos取1.也可以自定义
    :return:
    '''

    # ==基础数据准备
    sell_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, high_strike)
    buy_symbol = '%s-USD-%s-%s-C' % (coin.upper(), exptime, low_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # sell_c_pre = float(get_trade_data(sell_call_symbol)['bidPx'])  # 权利金，买一
    # buy_c_pre = float(get_trade_data(buy_call_symbol)['askPx'])  # 权利金，卖一
    sell_fee = cal_trade_fee(sell_pre, coin)
    buy_fee = cal_trade_fee(buy_pre, coin)
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * ratio * multiplier - buy_pre * multiplier - sell_fee * ratio - buy_fee) * spot_price_index  # 初始构建策略的成本，如果为正，则代表净权利金收入
    max_profit = (high_strike - low_strike) * multiplier + init_income  # 最大盈利
    max_profit_price = high_strike  # 获取最大盈利价格
    max_loss = 'infinite'
    max_loss_price = 'infinite'
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([init_income / spot_price_index + (x-low_strike) * multiplier / x])
    breakeven_price2 = cal_breakeven_price([init_income / spot_price_index + (x-low_strike)  *multiplier / x - (x-high_strike) * multiplier * ratio / x])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_pice, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_pice, interval):
        sell_c_profit = - call_profit(spot_price, high_strike, coin) * ratio
        buy_c_profit = call_profit(spot_price, low_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '卖出call收益'] = sell_c_profit
        df.loc[str(spot_price), '买入call收益'] = buy_c_profit
        df.loc[str(spot_price), '总收益(币本位)'] = buy_c_profit + sell_c_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price
    # print(df)
    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)
    # return df, init_cost, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index


def long_put_ratio_spread(coin, high_strike, low_strike, exptime, ratio=2, interval=100, unit='USDT'):
    '''
    比例价差多头
    买入n份较低行权价/到期日相同的看跌期权，权利金低
    卖出1份较高行权价/到期日相同的看跌期权，权利金高
    初始交易可能为正或负
    :param coin: btc eth eos
    :param high_strike: int 较高行权价
    :param low_strike: int 较低行权价
    :param exptime: 到期日  210402
    :param ratio: n
    :param interval: Scenario analysis中，现货的间隔，btc取100，eth取10，eos取1.也可以自定义
    :return:
    '''

    # ==基础数据准备
    sell_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, high_strike)
    buy_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, low_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    # sell_p_pre = float(get_trade_data(sell_put)['bidPx'])  # 权利金，买一
    # buy_p_pre = float(get_trade_data(buy_put_symbol)['askPx'])  # 权利金，卖一
    sell_fee = cal_trade_fee(sell_pre, coin)
    buy_fee = cal_trade_fee(buy_pre, coin)
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * multiplier - buy_pre * multiplier * ratio - sell_fee - buy_fee * ratio) * spot_price_index  # 初始构建策略的成本，如果为正，则代表净权利金收入
    max_profit = low_strike * multiplier * ratio - high_strike * multiplier + init_income  # 最大盈利
    max_profit_price = 0  # 获取最大盈利价格
    max_loss = init_income - (high_strike - low_strike) * multiplier
    max_loss_price = low_strike
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([init_income / spot_price_index - (high_strike - x) * multiplier / x])
    breakeven_price2 = cal_breakeven_price([init_income / spot_price_index + (low_strike - x) * multiplier * ratio / x - (high_strike - x) * multiplier / x])

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_price, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_price, interval):
        sell_p_profit = - put_profit(spot_price, high_strike, coin)
        buy_p_profit = put_profit(spot_price, low_strike, coin) * ratio
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '卖出put收益'] = sell_p_profit
        df.loc[str(spot_price), '买入put收益'] = buy_p_profit
        df.loc[str(spot_price), '总收益(币本位)'] = buy_p_profit + sell_p_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)
    # return df, init_cost, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index


def short_put_ratio_spread(coin, high_strike, low_strike, exptime, ratio=2, interval=100, unit='USDT'):
    '''
    比例价差空头
    卖出n份较低行权价/到期日相同的看跌期权，权利金低
    买入1份较高行权价/到期日相同的看跌期权，权利金高
    初始交易可能为正或负
    :param coin: btc eth eos
    :param high_strike: int 较高行权价
    :param low_strike: int 较低行权价
    :param exptime: 到期日  210402
    :param ratio: n
    :param interval: Scenario analysis中，现货的间隔，btc取100，eth取10，eos取1.也可以自定义
    :return:
    '''

    # ==基础数据准备
    sell_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, low_strike)
    buy_symbol = '%s-USD-%s-%s-P' % (coin.upper(), exptime, high_strike)
    multiplier = coin_value_table[coin]

    buy_pre = get_premium(buy_symbol)[1]
    sell_pre = get_premium(sell_symbol)[0]
    sell_pre = float(get_trade_data(sell_symbol)['bidPx'])  # 权利金，买一
    buy_pre = float(get_trade_data(buy_symbol)['askPx'])  # 权利金，卖一
    sell_fee = cal_trade_fee(sell_pre, coin)
    buy_fee = cal_trade_fee(buy_pre, coin)
    spot_price_index = float(get_index_price(coin)['idxPx'])  # 现货指数

    # ==计算策略指标
    init_income = (sell_pre * ratio * multiplier - buy_pre * multiplier - sell_fee * ratio - buy_fee) * spot_price_index  # 初始构建策略的成本，如果为正，则代表净权利金收入
    max_profit = (high_strike - low_strike) * multiplier + init_income  # 最大盈利
    max_profit_price = low_strike  # 获取最大盈利价格
    max_loss = high_strike * multiplier - low_strike * multiplier * ratio + init_income
    max_loss_price = 0
    x = sympy.symbols('x')
    breakeven_price1 = cal_breakeven_price([init_income / spot_price_index + (high_strike - x) * multiplier / x])
    breakeven_price2 = cal_breakeven_price([init_income / spot_price_index + (high_strike - x) * multiplier / x - (low_strike - x) * multiplier * ratio / x])
    # breakeven_price = low_strike - max_profit / (ratio-1) / multiplier # 当前的盈亏平衡价格

    # ==Scenario analysis
    # 生成多种价格
    df = pd.DataFrame()
    max_price, min_price = int(high_strike * 1.2), int(low_strike * 0.8)

    for spot_price in range(min_price, max_price, interval):
        sell_p_profit = - put_profit(spot_price, low_strike, coin) * ratio
        buy_p_profit = put_profit(spot_price, high_strike, coin)
        # print(spot_price, sell_c_profit, buy_c_profit)
        df.loc[str(spot_price), '卖出put收益'] = sell_p_profit
        df.loc[str(spot_price), '买入put收益'] = buy_p_profit
        df.loc[str(spot_price), '总收益(币本位)'] = buy_p_profit + sell_p_profit + init_income / spot_price_index
        df.loc[str(spot_price), '总收益(USDT)'] = df.loc[str(spot_price), '总收益(币本位)'] * spot_price

    plot_PL_charts_2breakeven_price(df, init_income, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price1, breakeven_price2, spot_price_index, unit)
    # return df, init_cost, max_profit, max_profit_price, max_loss, max_loss_price, breakeven_price, spot_price_index
















