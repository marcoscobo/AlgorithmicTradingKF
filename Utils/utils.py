from Utils.orders import connection, info_account, info_positions
from pandas import DataFrame, to_datetime, Timestamp, concat
from datetime import datetime, timedelta
import MetaTrader5 as mt5


def preprocessed(symbol, timeframe, date_from=datetime.now(), date_to=datetime.now(), method='range', start_pos=0, count=0):

	if method == 'range':
		rates_frame = DataFrame(mt5.copy_rates_range(symbol, timeframe, date_from, date_to))
	elif method == 'pos':
		rates_frame = DataFrame(mt5.copy_rates_from_pos(symbol, timeframe, start_pos, count))
	else:
		raise Exception('Method not compatible.')

	rates_frame['time'] = to_datetime(rates_frame['time'], unit='s',utc=True)

	return rates_frame


def preprocessed_long(symbol, timeframe, date_from=datetime.now(), date_to=datetime.now()):

	df = DataFrame()
	date_to_iter = date_from + timedelta(days=1)

	while date_to_iter <= date_to:
		df_iter = preprocessed(symbol=symbol, timeframe=timeframe, date_from=date_to_iter - timedelta(days=1), date_to=date_to_iter)
		df = concat([df, df_iter], ignore_index=True)
		date_to_iter += timedelta(days=1)

	return df


def status():

	connection()
	print('-'*64)
	dt = Timestamp(datetime.now()).round('min')
	print(dt)
	print('-'*64)
	info_account(p=True)
	info_positions(p=True)
	print('-'*64)
	mt5.shutdown()