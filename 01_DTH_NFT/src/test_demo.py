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
import threading

from cryptolib.crypto_sym import Crypto_SYM
from utils.utilities import DatetimeUtil, TypesUtil, FileUtil
from utils.Swarm_RPC import Swarm_RPC
from NFT_CapAC import NFT_CapAC
from NFT_Data import NFT_Data
from NFT_Tracker import NFT_Tracker

logger = logging.getLogger(__name__)

## ------------------- global variable ----------------------------
httpProvider = NFT_CapAC.getAddress('HttpProvider')

## new NFT_CapAC instance
contractAddr = NFT_CapAC.getAddress('NFT_CapAC')
contractConfig = '../build/contracts/NFT_CapAC.json'
token_capAC = NFT_CapAC(httpProvider, contractAddr, contractConfig)

## new NFT_Data instance
contractAddr = NFT_CapAC.getAddress('NFT_Data')
contractConfig = '../build/contracts/NFT_Data.json'
token_dataAC = NFT_Data(httpProvider, contractAddr, contractConfig)

## new NFT_Tracker instance
contractAddr = NFT_Tracker.getAddress('NFT_Tracker')
contractConfig = '../build/contracts/NFT_Tracker.json'
token_dataTracker = NFT_Tracker(httpProvider, contractAddr, contractConfig)

accounts = token_dataAC.getAccounts()
base_account = accounts[0]

## ---------------------- Internal function and class -----------------------------
def random_file(file_name, data_size):
	_data = os.urandom(data_size*1024)
	fname = open(file_name, 'w')
	fname.write("%s" %(_data))
	fname.close()

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
	elif(op_status==2):
		owner = token_dataTracker.ownerToken(tokenId)
		if(owner!=None):	
			token_URI = token_dataTracker.get_tokenURI(tokenId)
		else:
			token_URI = ""
		tracker_length = token_dataTracker.get_totalTracker(tokenId)
		print("Token_id:{}  owner: {}   token_URI:{}   tracker num: {}".format(tokenId, owner, token_URI, tracker_length))
		for idx in range(tracker_length):
			tracker_data = token_dataTracker.get_DataTracker(tokenId, idx)
			print("sender:{}   receiver:{}".format(tracker_data[0], tracker_data[1]))
	else:
		token_value = token_capAC.query_CapAC(tokenId)
		owner = token_capAC.ownerToken(tokenId)
		print("Token_id:{}   owner:{}\nCapAC:{}".format(tokenId, owner, token_value))

def mint_token(tokenId, owner, op_status):
	_account = NFT_CapAC.getAddress(owner)
	if(op_status==1):
		receipt = token_dataAC.mint_Data(tokenId, _account)
		_owner = token_dataAC.ownerToken(tokenId)
	elif(op_status==2):
		receipt = token_dataTracker.mint_Tracker(tokenId, _account)
		_owner = token_dataTracker.ownerToken(tokenId)
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
	if(op_status==2):
		_owner = token_dataTracker.ownerToken(tokenId)
		receipt = token_dataTracker.burn_Tracker(tokenId)
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

def test_Tracker(tokenId, op_status, ls_args):
	_owner = token_dataTracker.ownerToken(tokenId)
	if(_owner==None):
		print('Token {} is not existed'.format(tokenId))
		return

	if(op_status==1):
		print('Token {} transfer.'.format(tokenId))
		sender = NFT_Tracker.getAddress(ls_args[0])
		receiver = NFT_Tracker.getAddress(ls_args[1])
		receipt = token_dataTracker.transfer_DataTracker(tokenId, sender, receiver)
	else:
		print('Token {} set_tokenURI.'.format(tokenId))
		receipt = token_dataTracker.set_tokenURI(tokenId, ls_args[0])

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

def test_sym(args):
	for i in range(args.tx_round):
		logger.info("Test run:{}".format(i+1))

		if(args.op_status==1):
			## set data file path
			data_name = "./data/20220818154623.csv"
			_data=FileUtil.csv_read(data_name)
			ls_Gyro = []
			ls_ts = []
			for line_data in _data:
				row = line_data[0].split(" ")
				if('Gyro' in row):
					ls_Gyro.append(row)
				else:
					ls_ts.append(row)

			# print(ls_Gyro)
			# print(ls_ts)

			# str_data = str(ls_Gyro)
			str_data = str(ls_ts)
		else:
			data_name = "random_bytes"
			bytes_data = os.urandom(args.data_size*1024)
			str_data = TypesUtil.string_to_hex(bytes_data)

		salt_file = 'sym_salt'
		## 1) generate salt
		Crypto_SYM.generate_salt(salt_file)
		logger.info('Generate salt and saved to {}.\n'.format(salt_file))

		## 2) reload salt
		random_salt = Crypto_SYM.reload_salt(salt_file)
		logger.info('Reload salt from {}.\n'.format(salt_file))

		ls_time_exec = []

		## 3) encrypt message
		start_time=time.time()
		toekn = Crypto_SYM.encrypt(random_salt, 'samuelxu999', str_data)
		ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' )) 
		logger.info('Encryped data: {}.\n'.format(data_name))

		## 4) decrypt message
		start_time=time.time()
		dec_msg = Crypto_SYM.decrypt(random_salt, 'samuelxu999', toekn)
		ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' )) 
		logger.info('Decryped to original data.\n')

		str_time_exec=" ".join(ls_time_exec)
		FileUtil.save_testlog('test_results', 'test_sym.log', str_time_exec)

		time.sleep(args.wait_interval)

def test_swarm(args):
	for i in range(args.tx_round):
		logger.info("Test run:{}".format(i+1))
		## get swarm server node address
		target_address = Swarm_RPC.get_service_address()

		##==================== test upload file =========================
		tx_json = {}
		if(args.op_status==1):
			idx = i % 20
			file_name = "skeleton/" + str(idx+1)+".csv"
		elif(args.op_status==2):
			## generate randomdata file with data_size
			file_name = "random_file.txt"
			file_path = "./data/"+file_name
			random_file(file_path, args.data_size)
		else:
			file_name = "swarm_file.txt"
		
		file_download = "./data/download_file.txt"

		tx_json['upload_file']="./data/"+file_name


		ls_time_exec = []
		start_time=time.time()
		## send file to swarm server
		post_ret = Swarm_RPC.upload_file(target_address, tx_json)
		ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' )) 
		logger.info(post_ret)

		##==================== test download file =========================
		## get swarm hash from post_ret by upload_file
		swarm_hash = post_ret['data']

		start_time=time.time()
		## call smarm server to retrive file
		query_ret = Swarm_RPC.download_file(target_address, swarm_hash, file_name.split('/')[-1], file_download)
		ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' )) 
		logger.info(query_ret)

		str_time_exec=" ".join(ls_time_exec)
		FileUtil.save_testlog('test_results', 'test_swarm.log', str_time_exec)

		time.sleep(args.wait_interval)

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
	                    5-test_Data, \
	                    6-test_Tracker, \
	                    10-test_sym, \
	                    11-test_swarm")

	parser.add_argument("--op_status", type=int, default=0, 
	                    help="operation status: based on app")

	parser.add_argument("--tx_thread", type=int, default=1, 
						help="Transaction-threads count.")

	parser.add_argument("--seed", type=int, default=1, 
						help="seed used for randomization")
	parser.add_argument("--id", type=int, default=1, 
	                    help="input token id (int)")
	parser.add_argument("--value", type=str, default="", 
	                    help="input token value (string)")
	parser.add_argument("--message", type=str, default="", 
						help="Test message text.")

	parser.add_argument("--data_size", type=int, default=128, 
						help="Size (KB) of randome data for test.")

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
		for i in range(args.tx_round):			
			logger.info("Test run:{}".format(i+1))
			ls_time_exec = []
			start_time=time.time()
			query_token(args.id, args.op_status) 
			logger.info("exec_time: {} ms".format( format( (time.time()-start_time)*1000, '.3f')  ))
			ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))
			str_time_exec=" ".join(ls_time_exec)
			if(args.op_status==1):
				FileUtil.save_testlog('test_results', 'query_tokenData.log', str_time_exec)
			elif(args.op_status==2):
				FileUtil.save_testlog('test_results', 'query_tokenTracker.log', str_time_exec)
			else:
				FileUtil.save_testlog('test_results', 'query_tokenCapAC.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==2):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i
			ls_time_exec = []
			start_time=time.time()
			receipt = mint_token(token_id, args.value, args.op_status)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				if(args.op_status==1):
					FileUtil.save_testlog('test_results', 'mint_tokenData.log', str_time_exec)
				elif(args.op_status==2):
					FileUtil.save_testlog('test_results', 'mint_tokenTracker.log', str_time_exec)
				else:
					FileUtil.save_testlog('test_results', 'mint_tokenCapAC.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==3):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i
			ls_time_exec = []
			start_time=time.time()
			receipt = burn_token(token_id, args.op_status)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				if(args.op_status==1):
					FileUtil.save_testlog('test_results', 'burn_tokenData.log', str_time_exec)
				elif(args.op_status==2):
					FileUtil.save_testlog('test_results', 'burn_tokenTracker.log', str_time_exec)
				else:
					FileUtil.save_testlog('test_results', 'burn_tokenCapAC.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==4):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i

			## get dummy data for test
			ls_parameters = dummy_data(0)

			ls_time_exec = []
			start_time=time.time()
			receipt = test_CapAC(token_id, args.op_status, ls_parameters)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				FileUtil.save_testlog('test_results', 'update_CapAC.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==5):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i
			
			## get dummy data for test
			ls_parameters = dummy_data(1)

			ls_time_exec = []
			start_time=time.time()
			receipt = test_Data(token_id, args.op_status, ls_parameters)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				FileUtil.save_testlog('test_results', 'update_DataAC.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==6):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i

			ls_time_exec = []
			start_time=time.time()
			ls_parameters = args.value.split(',')
			receipt = test_Tracker(token_id, args.op_status, ls_parameters)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				FileUtil.save_testlog('test_results', 'update_DataTracker.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==10):
		test_sym(args)
	elif(args.test_func==11):
		test_swarm(args)
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

		ls_token = []
		total_supply = token_dataTracker.query_totalSupply()
		print("DataTracker total supply: %d" %(total_supply))
		for idx in range(total_supply):
			ls_token.append(token_dataTracker.query_tokenByIndex(idx))
		print(ls_token)
