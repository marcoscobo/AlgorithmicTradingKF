""" IMPORT STRATEGY """                                                                             # TODO: MODIFY
from backtesting import BackTesting
from Utils.utils import preprocessed
from Utils.orders import connection
from warnings import filterwarnings
from datetime import datetime, timedelta
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

backtest_from = 'backtest_from'                                                                     # TODO: MODIFY
backtest_to = 'backtest_to'                                                                         # TODO: MODIFY
train_period = timedelta(days=0)                                                                    # TODO: MODIFY

df = preprocessed(symbol=symbol, timeframe=timeframe, date_from=backtest_from, date_to=backtest_to)
df['action'] = 0

for date_to in df['time']:

    print('Date: {}'.format(date_to))

    date_from = date_to - train_period
    df_iter = preprocessed(symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to)

    action = 'strategy_action'                                                                      # TODO: MODIFY
    df.loc[df['time'] == date_to, 'action'] = action

df['action'] = df['action'].shift(periods=1).fillna(value=0)
backtest = BackTesting(df_market=df, SL=SL, TP=TP, pip_value=pip, points_spread=spread, action_column='action', result_column='Trade_Result', just_one=False, save_df=df)
result_kf = backtest.execute(metrics=True, verbose=True)

plt.plot(result_kf['close'], c='b', label='market')
plt.plot(result_kf.loc[result_kf['action'] == 1, 'close'], '^g')
plt.plot(result_kf.loc[result_kf['action'] == -1, 'close'], 'vr')
plt.title('Strategy') ; plt.legend() ; plt.show()

plt.plot(result_kf['Profit'], c='b', label='Profit')
plt.axhline(y=0)
plt.title('Net Profit') ; plt.legend() ; plt.show()

plt.plot(result_kf['Profit_Factor'][400:], c='b', label='Profit Factor')
plt.axhline(y=1)
plt.title('Profit Factor') ; plt.legend() ; plt.show()

plt.plot(result_kf['Drawdown'], c='b', label='Drawdown')
plt.title('Drawdown') ; plt.legend() ; plt.show()