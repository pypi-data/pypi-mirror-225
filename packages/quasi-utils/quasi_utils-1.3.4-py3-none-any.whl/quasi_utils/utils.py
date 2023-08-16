import os
import json
from base64 import b64encode, b64decode
from configparser import ConfigParser
import boto3
import requests as r
import pickle


def request(method, url, headers, data, params=None, timeout=7, verify=True, allow_redirects=True):
	res = r.request(method, url, data=data, headers=headers, verify=verify, allow_redirects=allow_redirects,
					timeout=timeout, proxies=None, params=params)

	try:
		return json.loads(res.content.decode('utf8'))
	except json.decoder.JSONDecodeError:
		return res.content


def base(price, rounder=0.05, precision=2):
	return round(rounder * round(float(price) / rounder), precision)


def get_details(config_name, data_dir):
	config = ConfigParser()
	config.read(os.path.join(data_dir, 'config.ini'))
	z = config[config_name]
	api_key, api_secret, access_token = decrypt(z['api_key']), decrypt(z['api_secret']), decrypt(z['access_token'])

	return api_key, api_secret, access_token


def decrypt(text, key_id='alias/kite_api_key'):
	kms = boto3.client('kms')
	return kms.decrypt(KeyId=key_id, CiphertextBlob=bytes(b64decode(text)))['Plaintext'].decode('utf8')


def encrypt(text, key_id='alias/kite_api_key'):
	kms = boto3.client('kms')
	return b64encode(kms.encrypt(KeyId=key_id, Plaintext=bytes(text, encoding='utf8'))['CiphertextBlob']).decode('utf8')


def get_trade_number(orders):
	trade_num = 0

	if not orders:
		return trade_num

	for order in orders:
		if order['transaction_type'] == 'SELL':
			trade_num += 1

	return trade_num


def check_global_loss(o, global_stop_loss):
	margin = o.margin(verbose=True)
	pnl = margin['utilised']['m2m_realised']

	if pnl < 0:
		cash = margin['available']
		total_cash = cash['opening_balance'] + cash['intraday_payin'] + cash['collateral']

		return False if abs(pnl) > (total_cash * global_stop_loss) else margin['net']

	return margin['net']


def get_total_cash(o):
	margin = o.margin(verbose=True)
	cash = margin['available']

	return cash['opening_balance'] + cash['intraday_payin'] + cash['collateral']


def get_oms_session():
	s3 = boto3.client('s3')
	file_obj = s3.get_object(Bucket=os.environ['SESSION_BUCKET'], Key='session.json')

	return file_obj['Body'].read().decode('utf-8')


def round_down(x, nearest_num=50):
	return x if x % nearest_num == 0 else x - (x % nearest_num)


def round_up(x, nearest_num=50):
	return x if x % nearest_num == 0 else x + (nearest_num - (x % nearest_num))


def get_s3_object(bucket, file_path):
	s3 = boto3.client('s3')
	file_obj = s3.get_object(Bucket=bucket, Key=file_path)

	return file_obj['Body'].read().decode('utf-8')


def upload_to_s3(bucket, file, key):
	s3 = boto3.resource('s3')
	s3.Object(bucket, key).put(Body=file)


def get_from_s3(bucket, key):
	s3 = boto3.resource('s3')

	return pickle.loads(s3.Bucket(bucket).Object(key).get()['Body'].read())


def colourise(text, colour, decorate=None, end_='\n'):
	_c = {'pink': '\033[95m', 'blue': '\033[94m', 'green': '\033[92m', 'yellow': '\033[93m', 'grey': '\033[97m',
		  'cyan': '\033[96m', 'end': '\033[0m', 'red': '\033[91m', 'underline': '\033[4m', 'bold': '\033[1m'}
	colour, end = _c[colour], _c['end']

	if decorate is not None:
		print(f'{_c[decorate]}{colour}{text}{end}', end=end_)
	else:
		print(f'{colour}{text}{end}', end=end_)
