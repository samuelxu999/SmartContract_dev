'''
========================
NFT_Server module
========================
Created on April.20, 2025
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of NFT-Token Microservices API that handle and response client's request.
'''

import datetime, time
import logging
from argparse import ArgumentParser
import sys
import os
from flask import Flask, jsonify
from flask import abort,make_response,request

from utils.utilities import DatetimeUtil, TypesUtil, FileUtil
from NFT_Data import NFT_Data

logger = logging.getLogger(__name__)

app = Flask(__name__)

## ------------------- global variable ----------------------------
httpProvider = NFT_Data.getAddress('HttpProvider')

## new NFT_Data instance
contractAddr = NFT_Data.getAddress('NFT_Data')
contractConfig = '../build/contracts/NFT_Data.json'
token_dataAC = NFT_Data(httpProvider, contractAddr, contractConfig)

accounts = token_dataAC.getAccounts()
base_account = accounts[0]

#================================ Error handler ======================================
#Error handler for abort(404) 
@app.errorhandler(404)
def not_found(error):
    #return make_response(jsonify({'error': 'Not found'}), 404)
	response = jsonify({'result': 'Failed', 'message':  error.description['message']})
	response.status_code = 404
	return response

#Error handler for abort(400) 
@app.errorhandler(400)
def type_error(error):
    #return make_response(jsonify({'error': 'type error'}), 400)
    response = jsonify({'result': 'Failed', 'message':  error.description['message']})
    response.status_code = 400
    return response
	
#Error handler for abort(401) 
@app.errorhandler(401)
def access_deny(error):
    response = jsonify({'result': 'Failed', 'message':  error.description['message']})
    response.status_code = 401
    return response

#====================== Request handler ===============================================
@app.route('/NFT/api/v1.0/getTokenInfo', methods=['GET'])
def getTokenInfo():
	## parse data from request.data
	req_data=TypesUtil.bytes_to_string(request.data)
	json_data = TypesUtil.string_to_json(req_data)

	start_time=time.time()
	balance = token_dataAC.getBalance(base_account)
	
	## get token_dataAC
	json_DataAC = {}
	ls_token = []
	total_supply = token_dataAC.query_totalSupply()
	json_DataAC['total']=total_supply
	for idx in range(total_supply):
		ls_token.append(token_dataAC.query_tokenByIndex(idx))
	json_DataAC['ids']=ls_token

	exec_time=time.time()-start_time
	FileUtil.save_testlog('test_results', 'getTokenInfo.log', format(exec_time*1000, '.3f'))
	
	json_ret={}

	json_ret['account']=base_account
	json_ret['balance']=balance
	json_ret['NFT_DataRef']=TypesUtil.json_to_string(json_DataAC)

	return jsonify({'result': 'Succeed', 'data': json_ret}), 201

@app.route('/NFT/api/v1.0/getDataRef', methods=['GET'])
def getDataRef():
	## parse data from request.data
	req_data=TypesUtil.bytes_to_string(request.data)
	json_data = TypesUtil.string_to_json(req_data)

	tokenId = json_data['token_id']

	start_time=time.time()
	owner = token_dataAC.ownerToken(tokenId)
	token_value = token_dataAC.get_DataRef(tokenId)	
	exec_time=time.time()-start_time
	FileUtil.save_testlog('test_results', 'getDataRef.log', format(exec_time*1000, '.3f'))
	
	json_ret={}

	json_ret['token_id']=tokenId
	json_ret['type']='NFT-DataRef'
	json_ret['owner']=owner
	json_ret['token_value']=TypesUtil.json_to_string(token_value)

	return jsonify({'result': 'Succeed', 'data': json_ret}), 201

def define_and_get_arguments(args=sys.argv[1:]):
	parser = ArgumentParser(description="Run NFT_Server websocket server.")

	parser.add_argument('-p', '--port', default=8180, type=int, 
						help="port to listen on.")

	args = parser.parse_args()

	return args

if __name__ == '__main__':
	FORMAT = "%(asctime)s %(levelname)s %(filename)s(l:%(lineno)d) - %(message)s"
	# FORMAT = "%(asctime)s %(levelname)s | %(message)s"
	LOG_LEVEL = logging.INFO
	logging.basicConfig(format=FORMAT, level=LOG_LEVEL)

	## get arguments
	args = define_and_get_arguments()

	app.run(host='0.0.0.0', port=args.port, debug=True, threaded=True)