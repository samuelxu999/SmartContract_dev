'''
========================
test_demo
========================
Created on August.25, 2022
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide test cases for demo and performance analysis.
'''

import datetime, time
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
	else:
		print('Token {} has been mint by {}'.format(tokenId, _owner))

	return receipt

def burn_token(tokenId, op_status):
	if(op_status==1):
		_owner = token_dataAC.ownerToken(tokenId)
		receipt = token_dataAC.burn_Data(tokenId)
	else:
		_owner = token_capAC.ownerToken(tokenId)
		receipt = token_capAC.burn_CapAC(tokenId)
	if(receipt!=None):
		print('Token {} is burn by owner {}'.format(tokenId, _owner))
	else:
		print('Token {} is not existed'.format(tokenId))

	return receipt

def test_CapAC(tokenId, op_status, ls_args):
	_owner = token_capAC.ownerToken(tokenId)
	if(_owner==None):
		print('Token {} is not existed'.format(tokenId))
		return

	if(op_status==1):
		print('Token {} CapAC_authorization.'.format(tokenId))
		receipt = token_capAC.CapAC_authorization(tokenId, ls_args[2])
	else:
		print('Token {} CapAC_expireddate.'.format(tokenId))
		receipt = token_capAC.CapAC_expireddate(tokenId, ls_args[0], ls_args[1])

	return receipt

def test_Data(tokenId, op_status, ls_args):
	_owner = token_dataAC.ownerToken(tokenId)
	if(_owner==None):
		print('Token {} is not existed'.format(tokenId))
		return

	if(op_status==1):
		print('Token {} DataAC_authorization.'.format(tokenId))
		receipt = token_dataAC.DataAC_authorization(tokenId, ls_args[2])
	else:
		print('Token {} DataAC_setup.'.format(tokenId))
		receipt = token_dataAC.DataAC_setup(tokenId, ls_args[0], ls_args[1])

	return receipt

def dummy_data(op_status):
	if(op_status==1):
		## get ref_address
		ref_address = TypesUtil.string_to_hex(os.urandom(64)) 

		## get hash value of data
		data_mac = TypesUtil.string_to_hex(os.urandom(128))

		## set ac right as json
		json_ac={}
		json_ac['action']="READ"
		json_ac['conditions']={}
		json_ac['conditions']['expired']="2022-09-10"
		ac_rights=TypesUtil.json_to_string(json_ac)

		parameters = [ref_address, data_mac, ac_rights]
	else:
		## set issue date and expired date
		nowtime = datetime.datetime.now()
		issue_time = DatetimeUtil.datetime_timestamp(nowtime)
		duration = DatetimeUtil.datetime_duration(0, 1, 0, 0)
		expire_time = DatetimeUtil.datetime_timestamp(nowtime + duration)

		## set ac right as json
		json_ac={}
		json_ac['resource']="/camera/api/viewer/"
		json_ac['action']="GET"
		json_ac['conditions']={}
		json_ac['conditions']['start']="9:12:32"
		json_ac['conditions']['end']="14:12:32"
		ac_rights=TypesUtil.json_to_string(json_ac)

		parameters = [issue_time, expire_time, ac_rights]

	return parameters

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
		ls_time_exec = []
		start_time=time.time()
		query_token(args.id, args.op_status) 
		logger.info("exec_time: {} ms".format( format( (time.time()-start_time)*1000, '.3f')  ))
		ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))
		str_time_exec=" ".join(ls_time_exec)
		if(args.op_status==1):
			FileUtil.save_testlog('test_results', 'query_tokenData.log', str_time_exec)
		else:
			FileUtil.save_testlog('test_results', 'query_tokenCapAC.log', str_time_exec)
	elif(args.test_func==2):
		ls_time_exec = []
		start_time=time.time()
		receipt = mint_token(args.id, args.value, args.op_status)
		if(receipt!=None):
			logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
			ls_time_exec.append( format( time.time()-start_time, '.3f') )
			str_time_exec=" ".join(ls_time_exec)
			if(args.op_status==1):
				FileUtil.save_testlog('test_results', 'mint_tokenData.log', str_time_exec)
			else:
				FileUtil.save_testlog('test_results', 'mint_tokenCapAC.log', str_time_exec)
	elif(args.test_func==3):
		ls_time_exec = []
		start_time=time.time()
		receipt = burn_token(args.id, args.op_status)
		if(receipt!=None):
			logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
			ls_time_exec.append( format( time.time()-start_time, '.3f') )
			str_time_exec=" ".join(ls_time_exec)
			if(args.op_status==1):
				FileUtil.save_testlog('test_results', 'burn_tokenData.log', str_time_exec)
			else:
				FileUtil.save_testlog('test_results', 'burn_tokenCapAC.log', str_time_exec)
	elif(args.test_func==4):
		## get dummy data for test
		ls_parameters = dummy_data(0)

		ls_time_exec = []
		start_time=time.time()
		receipt = test_CapAC(args.id, args.op_status, ls_parameters)
		if(receipt!=None):
			logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
			ls_time_exec.append( format( time.time()-start_time, '.3f') )
			str_time_exec=" ".join(ls_time_exec)
			FileUtil.save_testlog('test_results', 'update_CapAC.log', str_time_exec)
	elif(args.test_func==5):
		## get dummy data for test
		ls_parameters = dummy_data(1)

		ls_time_exec = []
		start_time=time.time()
		receipt = test_Data(args.id, args.op_status, ls_parameters)
		if(receipt!=None):
			logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
			ls_time_exec.append( format( time.time()-start_time, '.3f') )
			str_time_exec=" ".join(ls_time_exec)
			FileUtil.save_testlog('test_results', 'update_DataAC.log', str_time_exec)
	else:
		balance = token_capAC.getBalance(base_account)
		print("coinbase account: {}   balance: {}".format(base_account, balance))

		ls_token = []
		total_supply = token_capAC.query_totalSupply()
		print("CapAC total supply: %d" %(total_supply))
		for idx in range(total_supply):
			ls_token.append(token_capAC.query_tokenByIndex(idx))
		print(ls_token)

		ls_token = []
		total_supply = token_dataAC.query_totalSupply()
		print("DataAC total supply: %d" %(total_supply))
		for idx in range(total_supply):
			ls_token.append(token_dataAC.query_tokenByIndex(idx))
		print(ls_token)
