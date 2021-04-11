from program.option.functions import *
from program.option.config import *
from program.option.strategy import *
import matplotlib.pyplot as plt


# ====单腿
# long_call('btc', 56000, '210416', interval=100)
# short_call('btc', 56000, '210416', interval=100)
# long_put('btc', 56000, '210416', interval=100)
# short_put('btc', 56000, '210416', interval=100)

# ====牛熊价差
# bull_put_spread(coin='btc', high_strike=58500, low_strike=56500, exptime='210411', interval=100, unit='USDT')
# bull_call_spread(coin='btc', high_strike=60000, low_strike=56500, exptime='210411', interval=100, unit='USDT')
# bear_put_spread(coin='btc', high_strike=59000, low_strike=58000, exptime='210411', interval=100, unit='USDT')
bear_call_spread(coin='eth', high_strike=2100, low_strike=2040, exptime='210410', interval=10, unit='USDT')

# ====跨式
# long_straddles(coin='btc', strike=58000, exptime='210410', interval=100, unit='币本位')
# short_straddles(coin='btc', strike=58000, exptime='210410', interval=100, unit='币本位')
# long_strangle(coin='btc', c_strike=58000, p_strike=57000, exptime='210410', interval=100, unit='USDT')
# short_strangle(coin='btc', c_strike=58000, p_strike=57000, exptime='210410', interval=100, unit='USDT')






# ====比例价差
# short_call_ratio_spread('btc', 58000, 56000, '210402', ratio=2, interval=100)
# short_put_ratio_spread('btc', 58000, 56000, '210402', ratio=2, interval=100)
# long_put_ratio_spread('btc', 58000, 56000, '210402', ratio=2, interval=100)
# long_call_ratio_spread(coin='eth', high_strike=2040, low_strike=1960, exptime='210409', ratio=2, interval=100)







