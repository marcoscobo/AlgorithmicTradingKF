""" IMPORT STRATEGY """                                                                             # TODO: MODIFY
from Utils.utils import preprocessed
from Utils.orders import connection
from warnings import filterwarnings
from datetime import datetime, timedelta
import MetaTrader5 as mt5


filterwarnings('ignore')
connection()

symbol = 'symbol'                                                                                   # TODO: MODIFY
timeframe = 'timeframe'                                                                             # TODO: MODIFY

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

df.to_csv(str(symbol) + 'timeframe' + '.csv')                                                       # TODO: MODIFY