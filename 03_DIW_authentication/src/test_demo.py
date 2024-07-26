'''
========================
test_demo
========================
Created on July.22, 2024
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

import ipfshttpclient

from merklelib import MerkleTree, jsonify as merkle_jsonify

from cryptolib.crypto_sym import Crypto_SYM
from utils.utilities import DatetimeUtil, TypesUtil, FileUtil, FuncUtil
from NFT_Data import NFT_Data

logger = logging.getLogger(__name__)

## ------------------- global variable ----------------------------
httpProvider = NFT_Data.getAddress('HttpProvider')

## new NFT_Data instance
contractAddr = NFT_Data.getAddress('NFT_Data')
contractConfig = '../build/contracts/NFT_Data.json'
token_dataAC = NFT_Data(httpProvider, contractAddr, contractConfig)

accounts = token_dataAC.getAccounts()
base_account = accounts[0]

ipfs_client = ipfshttpclient.connect('/dns/localhost/tcp/10606/http') 

## ---------------------- Internal function and class -----------------------------
def random_file(file_name, data_size):
	_data = os.urandom(data_size*1024)
	fname = open(file_name, 'w')
	fname.write("%s" %(_data))
	fname.close()

def query_token(tokenId):
	base_URI = token_dataAC.get_baseURI()		
	owner = token_dataAC.ownerToken(tokenId)	
	if(owner!=None):
		token_URI = token_dataAC.get_tokenURI(tokenId)
		print("Token_id:{}  owner: {}   base_URI:{}   token_URI:{}".format(tokenId, owner, base_URI, token_URI))
	else:
		print("Token_id:{}  base_URI:{}".format(tokenId, base_URI))
	data_ac = token_dataAC.get_DataAC(tokenId)
	print("DataAC,  id:{}  mkt_root:{}   data_mac:{}   total_mac:{}".format(data_ac[0], data_ac[1], data_ac[2], data_ac[3]))
	return data_ac


def audit_data(token_id):
	ls_time_exec = []
	start_time=time.time()

	## query DataAC
	data_ac=query_token(token_id)
	# print(data_ac)

	ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))

	start_time=time.time()
	## build a Merkle tree from data_mac list
	mkt_root = data_ac[1]
	data_mac = data_ac[2]
	total_mac = data_ac[3]

	if(len(data_mac)!=total_mac):
		print("number of data_mac is not the same as total_mac!")
		return False

	## rebuild merkle tree
	tx_HMT = MerkleTree(data_mac, FuncUtil.hashfunc_sha256)
	tree_struct=merkle_jsonify(tx_HMT)
	json_tree = TypesUtil.string_to_json(tree_struct)
	re_mkt_root = json_tree['name']

	# print(mkt_root)
	# print(re_mkt_root)

	if(re_mkt_root!=mkt_root):
		print("verify merkle tree root fail!")
		return False

	ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))

	start_time=time.time()
	i=0
	for cid_file in data_mac:
		## download file from ipfs
		download_file = "./test_fig/dl_0000" + str(i) + '.jpg'

		## retrive file content from ipfs
		file_content = ipfs_client.cat(cid_file)
		# print(file_content.decode("utf-8"))

		if(file_content==''):
			print("verify data_config fail!")
			return False
		
		## save content to a download_file with prefix 'dl'
		text_file = open(download_file, "wb")
		text_file.write(file_content)
		text_file.close()

		i+=1

	ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))

	str_time_exec=" ".join(ls_time_exec)

	FileUtil.save_testlog('test_results', 'verify_tokenData.log', str_time_exec)

	return True	


def mint_token(tokenId, owner):
	_account = NFT_Data.getAddress(owner)

	receipt = token_dataAC.mint_Data(tokenId, _account)
	_owner = token_dataAC.ownerToken(tokenId)

	if(receipt!=None):
		print('Token {} is mint by {}'.format(tokenId, _owner))
	else:
		print('Token {} has been mint by {}'.format(tokenId, _owner))

	return receipt

def burn_token(tokenId):
	_owner = token_dataAC.ownerToken(tokenId)
	receipt = token_dataAC.burn_Data(tokenId)

	if(receipt!=None):
		print('Token {} is burn by owner {}'.format(tokenId, _owner))
	else:
		print('Token {} is not existed'.format(tokenId))

	return receipt

def test_Data(tokenId, ls_args):
	_owner = token_dataAC.ownerToken(tokenId)
	if(_owner==None):
		print('Token {} is not existed'.format(tokenId))
		return

	print('Token {} DataAC_setup.'.format(tokenId))
	receipt = token_dataAC.DataAC_setup(tokenId, ls_args[0], ls_args[1])

	return receipt

def dummy_data(value=1):

	# ## get mkt_root
	# mkt_root = TypesUtil.string_to_hex(os.urandom(64)) 

	## get hash value of data
	data_mac = []
	for i in range(value):
		data_mac.append( TypesUtil.string_to_hex(os.urandom(32)) )

	## build a Merkle tree from data_mac list
	tx_HMT = MerkleTree(data_mac, FuncUtil.hashfunc_sha256)

	## calculate merkle tree root hash
	if(len(tx_HMT)==0):
		mkt_root = 0
	else:
		tree_struct=merkle_jsonify(tx_HMT)
		json_tree = TypesUtil.string_to_json(tree_struct)
		mkt_root = json_tree['name']

	parameters = [mkt_root, data_mac]

	return parameters

def ipfs_data(value):
	## get hash value of data
	data_mac = []
	pre_figure_name = './test_fig/0000'
	for i in range(value):
		figure_name=pre_figure_name+str(i)+'.jpg'
		# print(figure_name)

		## upload file to IPFS
		receipt = ipfs_client.add(figure_name)

		# print(receipt)
		cid_file = receipt['Hash']
		data_mac.append(cid_file)


	## build a Merkle tree from data_mac list
	tx_HMT = MerkleTree(data_mac, FuncUtil.hashfunc_sha256)

	## calculate merkle tree root hash
	if(len(tx_HMT)==0):
		mkt_root = 0
	else:
		tree_struct=merkle_jsonify(tx_HMT)
		json_tree = TypesUtil.string_to_json(tree_struct)
		mkt_root = json_tree['name']

	parameters = [mkt_root, data_mac]

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
	                    4-test_Data, \
	                    5-audit_data")

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
			query_token(args.id) 
			logger.info("exec_time: {} ms".format( format( (time.time()-start_time)*1000, '.3f')  ))
			ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))
			str_time_exec=" ".join(ls_time_exec)
			FileUtil.save_testlog('test_results', 'query_tokenData.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==2):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i
			ls_time_exec = []
			start_time=time.time()
			receipt = mint_token(token_id, args.value)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				FileUtil.save_testlog('test_results', 'mint_tokenData.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==3):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i
			ls_time_exec = []
			start_time=time.time()
			receipt = burn_token(token_id)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				FileUtil.save_testlog('test_results', 'burn_tokenData.log', str_time_exec)

			time.sleep(args.wait_interval)
	elif(args.test_func==4):
		for i in range(args.tx_round):
			logger.info("Test run:{}".format(i+1))
			token_id = args.id + i
			
			ls_time_exec = []
			start_time=time.time()
			if(args.op_status==1):
				## get swarm data for test
				# ls_parameters = swarm_data(int(args.value))
				ls_parameters = ipfs_data(int(args.value))
				pass
			else:
				## get dummy data for test
				ls_parameters = dummy_data(int(args.value))				
			# print(ls_parameters)
			ls_time_exec.append( format( time.time()-start_time, '.3f') )
			
			start_time=time.time()
			receipt = test_Data(token_id, ls_parameters)
			if(receipt!=None):
				logger.info("exec_time: {} sec   gasUsed: {}".format( format( time.time()-start_time, '.3f'), receipt['gasUsed'] ))
				ls_time_exec.append( format( time.time()-start_time, '.3f') )
				str_time_exec=" ".join(ls_time_exec)
				FileUtil.save_testlog('test_results', 'update_DataAC.log', str_time_exec)
			time.sleep(args.wait_interval)
	elif(args.test_func==5):
		for i in range(args.tx_round):			
			logger.info("Test run:{}".format(i+1))

			# ## execute verify data
			# ls_time_exec = []
			# start_time=time.time()
			audit_data(i+1) 
			# logger.info("exec_time: {} ms".format( format( (time.time()-start_time)*1000, '.3f')  ))
			# ls_time_exec.append(format( (time.time()-start_time)*1000, '.3f' ))
			# str_time_exec=" ".join(ls_time_exec)

			# FileUtil.save_testlog('test_results', 'verify_tokenData.log', str_time_exec)

			time.sleep(args.wait_interval)
	else:
		balance = token_dataAC.getBalance(base_account)
		print("coinbase account: {}   balance: {}".format(base_account, balance))

		ls_token = []
		total_supply = token_dataAC.query_totalSupply()
		print("DataAC total supply: %d" %(total_supply))
		for idx in range(total_supply):
			ls_token.append(token_dataAC.query_tokenByIndex(idx))
		print(ls_token)
