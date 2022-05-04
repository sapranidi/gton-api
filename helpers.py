#!/usr/bin/python3
import requests
import yaml
import os
from dotenv import load_dotenv

load_dotenv()

with open('dao_contracts.yaml','r') as f:
    contracts = yaml.safe_load(f)

def get_token_price():
    payload = {
        'ids': 'gton-capital',
        'vs_currencies': 'usd'
    }
    r = requests.get('https://api.coingecko.com/api/v3/simple/price',params=payload).json()
    return float(r['gton-capital']['usd'])


def get_total_supply(chain):
    total_supply = 0
    k = contracts[chain]
    contractaddresses = k['TOKEN']
    key_name = k['KEY_NAME']
    apikey = (os.getenv(key_name))
    scanner_api = k['SCANNER_API']
    for contractaddress in contractaddresses:
        payload = {
            'module': 'stats',
            'action': 'tokensupply',
            'contractaddress': contractaddress,
            'apikey': apikey
        }
        r = requests.get(scanner_api,params=payload).json()
        chain_supply = int(r['result'])/(10**18)
        total_supply += chain_supply
    print("total_supply on", chain,"is",total_supply)
    return total_supply 

def get_dao_owned_supply(chain):
    dao_balance = 0
    k = contracts[chain]
    contractaddresses = k['TOKEN']
    key_name = k['KEY_NAME']
    apikey = (os.getenv(key_name))
    scanner_api = k['SCANNER_API']
    for contractaddress in contractaddresses:
        for address in k['DAO']:
            payload = {
                'module': 'account',
                'action': 'tokenbalance',
                'contractaddress': contractaddress,
                'address': address,
                'tag': 'latest',
                'apikey': apikey
            }
            r = requests.get(scanner_api,params=payload).json()
            dao_balance += int(r['result'])/(10**18)
    print("dao_balance on", chain,"is",dao_balance)
    return dao_balance

def get_csupply():
    ethereum_csupply = get_total_supply('ETHEREUM')-get_dao_owned_supply('ETHEREUM')-get_total_supply('FANTOM')-get_total_supply('POLYGON')-get_total_supply('BSC')
    fantom_csupply = get_total_supply('FANTOM_STAKING')-get_dao_owned_supply('FANTOM_STAKING')
    bsc_csupply = get_total_supply('BSC')-get_dao_owned_supply('BSC')
    polygon_csupply = get_total_supply('POLYGON')-get_dao_owned_supply('POLYGON')

    csupply = ethereum_csupply+fantom_csupply+bsc_csupply+polygon_csupply
    return csupply

def get_poa():
    return 3681550.9623108814

def get_floor_price():
    return get_poa()/get_csupply()


