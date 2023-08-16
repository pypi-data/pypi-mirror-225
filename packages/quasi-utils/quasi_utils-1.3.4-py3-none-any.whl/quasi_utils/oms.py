import contextlib
import json
from quasi_utils.utils import request, base, get_details
from datetime import datetime as dt


class OMS:
	def __init__(self, config=None, data_dir=None):
		self.base_url = 'https://api.kite.trade'
		self.timeout = 7
		self.api_key, self.api_secret, self.access_token = get_details(config, data_dir)
		self.headers = {'X-Kite-Version': '3', 'User-Agent': 'Kiteconnect-python/4.1.0',
						'Authorization': f'token {self.api_key}:{self.access_token}'}

	def place_gtt(self, buy_price, trade_type, qty, thresh=None, ticker=None, prefix=None, strike=None, exchange='NFO'):
		base_price, ticker = base(buy_price * thresh) if thresh else base(buy_price), ticker or f'{prefix}{strike}'

		condition = {'exchange': exchange, 'tradingsymbol': ticker, 'trigger_values': [base_price],
					 'last_price': self.ltp(f'{exchange}:{ticker}')[ticker]}
		orders = [{'exchange': exchange, 'tradingsymbol': ticker, 'transaction_type': 'SELL', 'quantity': qty,
				   'order_type': 'LIMIT', 'product': trade_type, 'price': base(base_price * 0.98)}]
		data = {'condition': json.dumps(condition), 'orders': json.dumps(orders), 'type': 'single'}

		return request('POST', f'{self.base_url}/gtt/triggers', data=data, headers=self.headers)

	def delete_gtt_orders(self, ids):
		if ids == 'all':
			for order in self.fetch_gtt_orders():
				request('DELETE', f'{self.base_url}/gtt/triggers/{order["id"]}', headers=self.headers, data=None)
		else:
			if not isinstance(ids, list):
				ids = [ids]
			for id_ in ids:
				request('DELETE', f'{self.base_url}/gtt/triggers/{id_}', headers=self.headers, data=None)

	def fetch_gtt_orders(self):
		res = request('GET', f'{self.base_url}/gtt/triggers', headers=self.headers, data=None)

		return res['data']

	def place_order(self, ticker, action, price, qty, price_type, trade_type='MIS', variety='regular', exchange='NFO',
					trigger_price=None, iceberg_legs=None, iceberg_quantity=None):
		data = {'tradingsymbol': ticker, 'exchange': exchange, 'transaction_type': action, 'price': price,
				'quantity': qty, 'variety': variety, 'order_type': price_type, 'product': trade_type,
				'trigger_price': trigger_price, 'iceberg_legs': iceberg_legs, 'iceberg_quantity': iceberg_quantity}

		return request('POST', f'{self.base_url}/orders/{variety}', data=data, headers=self.headers)

	def ltp(self, tickers):
		if not isinstance(tickers, list):
			tickers = [tickers]
		tickers_ = {'i': tickers}

		res = request('GET', f'{self.base_url}/quote/ltp', data=tickers_, params=tickers_, headers=self.headers)

		return {ticker_.split(':')[-1]: ltp['last_price'] for ticker_, ltp in res['data'].items()}

	def margin(self, verbose=False):
		res = request('GET', f'{self.base_url}/user/margins/equity',
					  data={'segment': 'equity'}, params={'segment': 'equity'}, headers=self.headers)
		data = res['data']

		return data if verbose else {'cash': round(data['net'], 1), 'pnl': data['utilised']['m2m_realised']}

	def orders(self, status=None, mould=False):
		res = request('GET', f'{self.base_url}/orders', data=None, headers=self.headers)
		orders, new_orders = res['data'], []

		rename = {'order_timestamp': 'Time', 'tradingsymbol': 'Ticker', 'transaction_type': 'Action',
				  'order_type': 'Type', 'quantity': 'Qty', 'price': 'Price', 'status': 'Status'}
		from_format, to_format = '%Y-%m-%d %H:%M:%S', '%d-%b-%Y %H:%M:%S'

		if status:
			orders = [order for order in orders if order['status'] == status]

		for order in orders:
			with contextlib.suppress(TypeError):
				order['order_timestamp'] = dt.strptime(order['order_timestamp'], from_format).strftime(to_format)
				order['exchange_timestamp'] = dt.strptime(order['exchange_timestamp'], from_format).strftime(to_format)

			if mould:
				temp_orders = {}

				for k in order.keys():
					if k in rename:
						if k == 'price' and order['price'] == 0:
							temp_orders['Price'] = round(order['average_price'], 2)
						else:
							temp_orders[rename[k]] = order[k]

				new_orders.append(temp_orders)

		return new_orders if mould else orders

	def positions(self, only_open=False):
		res = request('GET', f'{self.base_url}/portfolio/positions', data=None, headers=self.headers)
		positions = res['data']['net']

		return [position for position in positions if position['quantity']] if only_open else positions

	def get_ticker_tokens(self, tickers, exchange_='NSE'):
		res = request('GET', f'{self.base_url}/instruments/{exchange_}', data=None, headers=self.headers)
		data = res.decode('utf-8').strip()
		dump = {}

		for row in data.split('\n'):
			row = row.split(',')
			ticker_token, ticker = row[0], row[2]

			if ticker in tickers:
				dump[ticker] = ticker_token

		return dump


if __name__ == '__main__':
	# from utils import get_from_s3
	# ticker_ = get_from_s3('oms-session', 'nse_500.pickle')
	# print(obj.get_ticker_tokens(ticker_))
	obj = OMS(config='zerodha_me', data_dir=r'..\..\lambda\order')
	print(obj.ltp('NSE:NIFTY 50'))
	# print(obj.place_order('NIFTY23JAN17900PE', 'BUY', 13, 100, 'LIMIT'))
	print(obj.orders(mould=True))
