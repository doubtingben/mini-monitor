# Source: https://github.com/cdaly333/eth2-balance-logger/blob/main/balance-logger.py
from sys import argv, exit
from prometheus_client import start_http_server, Gauge
from time import sleep
import requests
import datetime
import os


URL = os.environ.get('VALIDATOR_URL') + os.environ.get('VALIDATOR_ADDRESS')
print('URL: {}'.format(URL))
UPDATE_INTERVAL = int(os.environ.get('VALIDATOR_INTERVAL_SECONDS'))
balance_guage = Gauge('eth_validator_balance', 'Validator balance, in ETH', ['pubkey'])
start_http_server(9010)

while (True):
  response = requests.get(URL)
  if response.ok:
    print('{} {} {} {}'.format(datetime.datetime.now(), response.status_code, os.environ['VALIDATOR_ADDRESS'], response.json()["data"]["balance"]))
    balance_guage.labels(pubkey=os.environ['VALIDATOR_ADDRESS']).set(float(response.json()["data"]["balance"])/10**9)
  sleep(UPDATE_INTERVAL)
