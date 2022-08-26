'''
========================
test_demo
========================
Created on August.25, 2022
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide test cases for demo and performance analysis.
'''

import time
import logging
import argparse
import sys
import os

from utilities import DatetimeUtil, TypesUtil, FileUtil
from NFT_CapAC import NFT_CapAC
from NFT_Data import NFT_Data

logger = logging.getLogger(__name__)

## ------------------- global variable ----------------------------
httpProvider = NFT_CapAC.getAddress('HttpProvider')

contractAddr = NFT_CapAC.getAddress('NFT_CapAC')
contractConfig = '../build/contracts/NFT_CapAC.json'

## new NFT_CapAC instance
token_capAC = NFT_CapAC(httpProvider, contractAddr, contractConfig)

contractAddr = NFT_CapAC.getAddress('NFT_Data')
contractConfig = '../build/contracts/NFT_Data.json'

## new NFT_Data instance
token_dataAC = NFT_Data(httpProvider, contractAddr, contractConfig)

accounts = token_dataAC.getAccounts()
base_account = accounts[0]

def query_token(tokenId, op_status):
	if(op_status==1):
		base_URI = token_dataAC.get_baseURI()		
		owner = token_dataAC.ownerToken(tokenId)	
		if(owner!=None):
			token_URI = token_dataAC.get_tokenURI(tokenId)
			print("Token_id:{}  owner: {}   base_URI:{}   token_URI:{}".format(tokenId, owner, base_URI, token_URI))
		else:
			print("Token_id:{}  base_URI:{}".format(tokenId, base_URI))
		data_ac = token_dataAC.get_DataAC(tokenId)
		print("DataAC,  id:{}  ref_address:{}   data_mac:{}   access_rights:{}".format(data_ac[0], data_ac[1], data_ac[2], data_ac[3]))
	else:
		token_value = token_capAC.query_CapAC(tokenId)
		owner = token_capAC.ownerToken(tokenId)
		print("Token_id:{}   owner:{}  CapAC:{}".format(tokenId, owner, token_value))

def mint_token(tokenId, owner, op_status):
	_account = NFT_CapAC.getAddress(owner)
	if(op_status==1):
		receipt = token_dataAC.mint_Data(tokenId, _account)
		_owner = token_dataAC.ownerToken(tokenId)
	else:
		receipt = token_capAC.mint_CapAC(tokenId, _account)
		_owner = token_capAC.ownerToken(tokenId)
	if(receipt!=None):
		print('Token {} is mint by {}'.format(tokenId, _owner))
		print(receipt)
	else:
		print('Token {} has been mint by {}'.format(tokenId, _owner))

def burn_token(tokenId, op_status):
	if(op_status==1):
		_owner = token_dataAC.ownerToken(tokenId)
		receipt = token_dataAC.burn_Data(tokenId)
	else:
		_owner = token_capAC.ownerToken(tokenId)
		receipt = token_capAC.burn_CapAC(tokenId)
	if(receipt!=None):
		print('Token {} is burn by owner {}'.format(tokenId, _owner))
		print(receipt)
	else:
		print('Token {} is not existed'.format(tokenId))


def define_and_get_arguments(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(
	    description="Run test demo."
	)

	parser.add_argument("--tx_round", type=int, default=1, 
						help="tx evaluation round")

	parser.add_argument("--wait_interval", type=int, default=1, 
	                    help="break time between tx evaluate step.")

	parser.add_argument("--test_func", type=int, default=0, 
	                    help="Execute test function: \
	                    0-contract information, \
	                    1-query_token, \
	                    2-mint_token, \
	                    3-burn_token, \
	                    4-test_CapAC, \
	                    5-test_Data")

	parser.add_argument("--op_status", type=int, default=0, 
	                    help="operation status: based on app")

	parser.add_argument("--query_tx", type=int, default=0, 
	                    help="Query tx or commit tx: 0-Query, 1-Commit")

	parser.add_argument("--seed", type=int, default=1, 
						help="seed used for randomization")
	parser.add_argument("--id", type=int, default=1, 
	                    help="input token id (int)")
	parser.add_argument("--value", type=str, default="", 
	                    help="input token value (string)")
	parser.add_argument("--message", type=str, default="", 
						help="Test message text.")

	args = parser.parse_args(args=args)
	return args

if __name__ == "__main__":
	# Logging setup
	FORMAT = "%(asctime)s | %(message)s"
	logging.basicConfig(format=FORMAT)
	logger.setLevel(level=logging.DEBUG)

	args = define_and_get_arguments()

	## switch test cases
	if(args.test_func==1):
		query_token(args.id, args.op_status)
	elif(args.test_func==2):
		mint_token(args.id, args.value, args.op_status)
	elif(args.test_func==3):
		burn_token(args.id, args.op_status)
	else:
		balance = token_capAC.getBalance(base_account)
		print("coinbase account: {}   balance: {}".format(base_account, balance))