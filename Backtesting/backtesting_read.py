from backtesting import BackTesting
from pandas import read_csv
from Utils.orders import connection
from warnings import filterwarnings
import matplotlib.pyplot as plt
import MetaTrader5 as mt5


filterwarnings('ignore')
connection()

symbol = 'symbol'                                                                                   # TODO: MODIFY
timeframe = 'timeframe'                                                                             # TODO: MODIFY

TP = 'TP'                                                                                           # TODO: MODIFY
SL = 'SL'                                                                                           # TODO: MODIFY
pip = mt5.symbol_info(symbol).point * 10
spread = 'spread'                                                                                   # TODO: MODIFY
change_dir = False

df = read_csv('dir.csv', index_col=0)                                                               # TODO: MODIFY
if change_dir:
    df['action'] = -1 * df['action']

df['action'] = df['action'].shift(periods=1).fillna(value=0)
backtest = BackTesting(df_market=df, SL=SL, TP=TP, pip_value=pip, points_spread=spread, action_column='action', result_column='Trade_Result', just_one=True, save_df=df)
result_kf = backtest.execute(metrics=True, verbose=True)

plt.plot(result_kf['close'], c='b', label='market')
plt.plot(result_kf.loc[result_kf['action'] == 1, 'close'], '^g')
plt.plot(result_kf.loc[result_kf['action'] == -1, 'close'], 'vr')
plt.title('Strategy '+ symbol) ; plt.legend() ; plt.show()

plt.plot(result_kf['Profit'], c='b', label='Profit')
plt.axhline(y=0)
plt.title('Net Profit '+ symbol) ; plt.legend() ; plt.show()

plt.plot(result_kf['Profit_Factor'][400:], c='b', label='Profit Factor')
plt.axhline(y=1)
plt.title('Profit Factor '+ symbol) ; plt.legend() ; plt.show()

plt.plot(result_kf['Drawdown'], c='b', label='Drawdown')
plt.title('Drawdown '+ symbol) ; plt.legend() ; plt.show()