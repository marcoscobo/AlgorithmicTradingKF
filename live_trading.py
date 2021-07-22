""" IMPORT STRATEGY """                                                                             # TODO: MODIFY
from Utils.orders import connection, margin, info_positions, open_position
from Utils.utils import preprocessed, status
from datetime import datetime, timedelta
from numpy import abs
from time import sleep
import schedule
import MetaTrader5 as mt5


def get_action(symbol):

    timeframe = 'TIMEFRAME'                                                                         # TODO: MODIFY
    date_to = datetime.now()
    date_from = 'TRAINING INTERVAL'                                                                 # TODO: MODIFY

    df = preprocessed(symbol=symbol, timeframe=timeframe, date_from=date_from, date_to=date_to)
    action = 'STRATEGY ACTION'                                                                      # TODO: MODIFY

    return action


def run_trade(symbol, just_one):

    connection()
    action = get_action(symbol=symbol) ; print('Market analized. Action: {}'.format(action))

    if abs(action) == 1:
        op_margin = margin(symbol=symbol, action=action, size='LOT')                                # TODO: MODIFY
        if op_margin:
            if just_one:
                s_positions = info_positions(symbol=symbol)
                if len(s_positions) == 0:
                    open_position(symbol=symbol, action=action, size='LOT', tp='TP', sl='SL')       # TODO: MODIFY
            else:
                open_position(symbol=symbol, action=action, size='LOT', tp='TP', sl='SL')           # TODO: MODIFY

    mt5.shutdown()


def live_trading(symbol, just_one):

    schedule.every(1).minutes.at(":00").do(run_trade, symbol, just_one)                             # TODO: MODIFY

    schedule.every().day.at(':00').do(status)

    while True:
        schedule.run_pending()
        sleep(1)


live_trading(symbol='SYMBOL', just_one='JUST_ONE')                                                  # TODO: MODIFY