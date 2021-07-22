from pandas import DataFrame, to_datetime
from numpy import abs
import MetaTrader5 as mt5


def connection(server='server', login=12345678, password='********'):                     # TODO: MODIFY

    if not mt5.initialize(server=server, login=login, password=password):
        print('Login error.')
        mt5.shutdown()
        exit()


def info_account(p=False):

    info = mt5.account_info()
    if p:
        print('Server: {}'.format(info.server))
        print('Account: {}'.format(info.login))
        print('Balance: {} {}'.format(info.balance, info.currency))
        print('Free margin: {} {}'.format(info.margin_free, info.currency))

    return info


def info_orders(symbol=None, p=False):

    if symbol is None:
        orders = mt5.orders_get()
    else:
        if mt5.symbol_info(symbol) is None:
            raise Exception('{} not found'.format(symbol))
        orders = mt5.orders_get(symbol=symbol)

    df = DataFrame()
    if orders is not None and orders != ():
        df = DataFrame(list(orders), columns=orders[0]._asdict().keys())
        df['time'] = to_datetime(df['time'], unit='s')

    if p:
        print('Total orders: {}'.format(len(df)))
        if len(df) > 0: print('\n',df)

    return df


def info_positions(symbol=None, p=False):

    if symbol is None:
        positions = mt5.positions_get()
    else:
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            raise Exception('{} not found'.format(symbol))
        if not symbol_info.visible:
            raise Exception('{} not visible'.format(symbol))
        positions = mt5.positions_get(symbol=symbol)

    df = DataFrame()
    if positions is not None and positions != ():
        df = DataFrame(list(positions), columns=positions[0]._asdict().keys())
        df['time'] = to_datetime(df['time'], unit='s')

    if p:
        print('Total positions: {}'.format(len(df)))
        if len(df) > 0: print('\n',df)

    return df


def margin(symbol, action, size, p=False):

    symbol_info = mt5.symbol_info(symbol)
    account_info = mt5.account_info()

    if symbol_info is None:
        raise Exception('{} not found'.format(symbol))
    if not symbol_info.visible:
        raise Exception('{} not visible'.format(symbol))
    if abs(action) != 1:
        raise Exception('Action not suported. Select between 1 and -1.')
    if size <= 0:
        raise Exception('Invalid lot.')

    if action == 1:
        price = mt5.symbol_info_tick(symbol).ask
        type = mt5.ORDER_TYPE_BUY ; print_type = 'buy'
    if action == -1:
        price = mt5.symbol_info_tick(symbol).bid
        type = mt5.ORDER_TYPE_SELL ; print_type = 'sell'

    margin = mt5.order_calc_margin(type, symbol, size, price)

    if p and margin != None:
        print('{} {} {} lot margin: {} {}'.format(symbol, print_type, size, margin, account_info.currency))

    if margin > account_info.margin_free:
        return False
    return True


def open_position(symbol, action, size=0.01, tp=None, sl=None):

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise Exception('{} not found'.format(symbol))
    if not symbol_info.visible:
        raise Exception('{} not visible'.format(symbol))
    if abs(action) != 1:
        raise Exception('Action not suported. Select between 1 and -1.')
    if size <= 0:
        raise Exception('Invalid lot.')
    if tp < 0 or sl < 0:
        raise Exception('Invalid take profit and stop loss.')

    pip = symbol_info.point * 10

    if action == 1:
        order = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask
        if sl is not None:
            sl = price - sl * pip
        if tp is not None:
            tp = price + tp * pip

    if action == -1:
        order = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
        if sl is not None:
            sl = price + sl * pip
        if tp is not None:
            tp = price - tp * pip

    request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': float(size),
        'type': order,
        'price': price,
        'sl': sl,
        'tp': tp,
        'magic': 123456,
        'comment': 'Open trade',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception('Failed to send order. Retcode: {}'.format(result.retcode))

    if action == 1: print('Buy order successfully placed!')
    if action == -1: print('Sell order successfully placed!')


def close_position(position_ticket):

    open_positions = info_positions()
    try:
        open_positions = open_positions[open_positions['ticket'] == position_ticket]
    except:
        raise Exception('Invalid position ticket.')
    order_type = open_positions['type'][0]
    symbol = open_positions['symbol'][0]
    volume = open_positions['volume'][0]

    if order_type == mt5.ORDER_TYPE_BUY:
        order_type = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(symbol).bid
    else:
        order_type = mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(symbol).ask

    close_request = {
        'action': mt5.TRADE_ACTION_DEAL,
        'symbol': symbol,
        'volume': float(volume),
        'type': order_type,
        'position': position_ticket,
        'price': price,
        'magic': 123456,
        'comment': 'Close trade',
        'type_time': mt5.ORDER_TIME_GTC,
        'type_filling': mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(close_request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise Exception('Failed to close order. Retcode: {}'.format(result.retcode))

    print('Order successfully closed!')


def close_symbol_positions(symbol):

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise Exception('{} not found'.format(symbol))
    if not symbol_info.visible:
        raise Exception('{} not visible'.format(symbol))

    open_positions = info_positions(symbol)
    open_positions['ticket'].apply(lambda x: close_position(x))