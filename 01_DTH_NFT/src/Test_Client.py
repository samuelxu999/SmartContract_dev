'''
========================
Test_Client module
========================
Created on August.11, 2020
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of TB SrvExchangeClient API that access to Web service.
'''

import logging
import argparse
import sys
import time
import threading
import requests
import json
from utils.utilities import DatetimeUtil, TypesUtil, FileUtil

logger = logging.getLogger(__name__)

## ---------------------- Internal function and class -----------------------------
class queryTxsThread(threading.Thread):
	'''
	Threading class to handle multiple txs threads pool
	'''
	def __init__(self, argv):
		threading.Thread.__init__(self)
		self.argv = argv

	#The run() method is the entry point for a thread.
	def run(self):
		## set parameters based on argv
		op_status = self.argv[0]
		_address = self.argv[1]
		_id = self.argv[2]

		if(op_status==1):
			ret_msg=queryDataAC(_address, _id)
			logger.info(ret_msg)
		else:
			ret_msg=queryCapAC(_address, _id)
			logger.info(ret_msg)

def query_txs(args):
	target_address = args.target_address
	tokenId = args.id
	op_status = args.op_status
	thread_count = args.thread_count
	## Create thread pool
	threads_pool = []

	## 1) build tx_thread for each task
	for idx in range(thread_count):
		## Create new threads for tx

		p_thread = queryTxsThread( [op_status, target_address, tokenId] )

		## append to threads pool
		threads_pool.append(p_thread)

		## The start() method starts a thread by calling the run method.
		p_thread.start()

	## 2) The join() waits for all threads to terminate.
	for p_thread in threads_pool:
		p_thread.join()

	logger.info('launch query_txs, number:{}'.format(thread_count))

def queryTokenInfo(target_address):

	api_url = "http://" + target_address + "/NFT/api/v1.0/getTokenInfo"
	headers = {'Content-Type' : 'application/json'}

	response = requests.get(api_url,data=json.dumps({}), headers=headers)

	json_response = response.json()

	return json_response

def queryCapAC(target_address, token_id):

	api_url = "http://" + target_address + "/NFT/api/v1.0/getCapAC"
	headers = {'Content-Type' : 'application/json'}

	data_json={}
	data_json['token_id']=token_id

	response = requests.get(api_url,data=json.dumps(data_json), headers=headers)

	json_response = response.json()

	return json_response

def queryDataAC(target_address, token_id):

	api_url = "http://" + target_address + "/NFT/api/v1.0/getDataAC"
	headers = {'Content-Type' : 'application/json'}

	data_json={}
	data_json['token_id']=token_id

	response = requests.get(api_url,data=json.dumps(data_json), headers=headers)

	json_response = response.json()

	return json_response

def define_and_get_arguments(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(
	    description="Run Test client."
	)

	parser.add_argument("--test_func", type=int, default=0, 
	                    help="Execute test function: 0-Services_demo, \
	                                                1-Services_test")

	parser.add_argument("--op_status", type=int, default=0, 
	                    help="operation status: based on app")

	parser.add_argument("--target_address", type=str, default="127.0.0.1:8380", 
						help="Test target address - ip:port.")
	
	parser.add_argument("--id", type=int, default=1, 
	                    help="input token id (int)")

	parser.add_argument("--tx_round", type=int, default=1, help="tx evaluation round")
	parser.add_argument("--thread_count", type=int, default=1, help="service threads count for test")
	parser.add_argument("--wait_interval", type=int, default=1, 
	                    help="break time between tx evaluate step.")
	args = parser.parse_args(args=args)
	return args

if __name__ == "__main__":
	# Logging setup
	FORMAT = "%(asctime)s | %(message)s"
	logging.basicConfig(format=FORMAT)
	logger.setLevel(level=logging.DEBUG)

	# serviceUtils_logger = logging.getLogger("service_utils")
	# serviceUtils_logger.setLevel(logging.INFO)

	args = define_and_get_arguments()

	if(args.test_func==1): 
		ret_msg=queryCapAC(args.target_address, args.id)
		logger.info(ret_msg)
	elif(args.test_func==2): 
		ret_msg=queryDataAC(args.target_address, args.id)
		logger.info(ret_msg)
	elif(args.test_func==3):
		ls_time_exec = []
		start_time=time.time()
		query_txs(args)
		logger.info("exec_time: {} sec".format( format( (time.time()-start_time), '.3f')  ))
		ls_time_exec.append(format( (time.time()-start_time), '.3f' ))
		str_time_exec=" ".join(ls_time_exec)
		if(args.op_status==1):
			FileUtil.save_testlog('test_results', 'getDataAC_client.log', str_time_exec)
		else:
			FileUtil.save_testlog('test_results', 'getCapAC_client.log', str_time_exec)
	else:
	    ret_msg=queryTokenInfo(args.target_address)
	    logger.info(ret_msg)
	