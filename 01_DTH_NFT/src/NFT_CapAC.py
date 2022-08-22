
'''
========================
NFT_CapAC module
========================
Created on August.21, 2022
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with NFT_CapAC smart contract.
'''
from web3 import Web3, HTTPProvider, IPCProvider
import json, datetime, time
import sys
import argparse

from utilities import DatetimeUtil, TypesUtil

class NFT_CapAC(object):
	def __init__(self, http_provider, contract_addr, contract_config):
		# configuration initialization
		self.web3 = Web3(HTTPProvider(http_provider))
		self.contract_address = Web3.toChecksumAddress(contract_addr)
		self.contract_config = json.load(open(contract_config))

		# new contract object
		self.contract = self.web3.eth.contract(address=self.contract_address, 
		                                    abi=self.contract_config['abi'])

	## return accounts address
	def getAccounts(self):
		return self.web3.eth.accounts

	##  return balance of account  
	def getBalance(self, account_addr = ''):
		if(account_addr == ''):
			checksumAddr = self.web3.eth.coinbase
		else:
			checksumAddr = Web3.toChecksumAddress(account_addr)
		return self.web3.fromWei(self.web3.eth.getBalance(checksumAddr), 'ether')

	## get address from json file, helper function
	@staticmethod
	def getAddress(node_name):
		address_json = json.load(open('./addr_list.json'))
		return address_json[node_name]

	## mint a token
	def mint_CapAC(self, tokenId, owner):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(not token_existed):
			#@Change account address to EIP checksum format
			checksumAddr = Web3.toChecksumAddress(owner)
			print('Token {} is mint by {}'.format(tokenId,checksumAddr))
			tx_hash = self.contract.functions.mint(checksumAddr, int(tokenId)).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} has been mint by {}'.format(tokenId, owner))

	## burn a token
	def burn_CapAC(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			owner = self.contract.functions.ownerOf(int(tokenId)).call({'from': self.web3.eth.coinbase})
			print('Token {} is burn by owner {}'.format(tokenId,owner))
			tx_hash = self.contract.functions.burn(int(tokenId)).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## setCapAC_expireddate
	def CapAC_expireddate(self, tokenId, ini_date, exp_date):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			print('Token {} setCapAC_expireddate'.format(tokenId))
			tx_hash = self.contract.functions.setCapAC_expireddate(int(tokenId), ini_date, exp_date).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## setCapAC_authorization
	def CapAC_authorization(self, tokenId, ac_right):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			print('Token {} setCapAC_authorization'.format(tokenId))
			tx_hash = self.contract.functions.setCapAC_authorization(int(tokenId), ac_right).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## query value from a token
	def query_CapAC(self, tokenId):
		#@Change account address to EIP checksum format
		# checksumAddr = Web3.toChecksumAddress(tokenId)

		## call getTokens()
		token_value = self.contract.functions.query_CapAC(int(tokenId)).call({'from': self.web3.eth.coinbase})
		print("Token_id:{}  CapAC:{}".format(tokenId, token_value))



def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run NFT_CapAC."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-contract information, \
                        1-get_token, \
                        2-deposit_value, \
                        3-withdraw_value")

    parser.add_argument("--op_status", type=int, default="0", 
                        help="input sub operation")

    parser.add_argument("--id", type=str, default="token1", 
                        help="input token id")

    parser.add_argument("--value", type=str, default="", 
                        help="input value")

    args = parser.parse_args(args=args)
    return args

if __name__ == "__main__":

	args = define_and_get_arguments()

	httpProvider = NFT_CapAC.getAddress('HttpProvider')
	contractAddr = NFT_CapAC.getAddress('NFT_CapAC')
	contractConfig = '../build/contracts/NFT_CapAC.json'

	## new NFT_CapAC instance
	myToken = NFT_CapAC(httpProvider, contractAddr, contractConfig)

	accounts = myToken.getAccounts()

	## switch test cases
	if(args.test_op==1):
		tokenId=NFT_CapAC.getAddress(args.id)
		myToken.query_CapAC(tokenId)
	elif(args.test_op==2):
		tokenId=NFT_CapAC.getAddress(args.id)
		other_account = NFT_CapAC.getAddress('other_account')
		if(args.op_status==1):
			myToken.mint_CapAC(tokenId, other_account)
		else:
			 myToken.mint_CapAC(tokenId, accounts[0])
	elif(args.test_op==3):
		tokenId=NFT_CapAC.getAddress(args.id)
		myToken.burn_CapAC(tokenId)
	elif(args.test_op==4):
		tokenId=NFT_CapAC.getAddress(args.id)

		#set issue date and expired date
		nowtime = datetime.datetime.now()
		#calculate issue_time and expire_time
		issue_time = DatetimeUtil.datetime_timestamp(nowtime)
		duration = DatetimeUtil.datetime_duration(0, 1, 0, 0)
		expire_time = DatetimeUtil.datetime_timestamp(nowtime + duration)

		myToken.CapAC_expireddate(tokenId, issue_time, expire_time)
	elif(args.test_op==5):
		tokenId=NFT_CapAC.getAddress(args.id)
		myToken.CapAC_authorization(tokenId, args.value)
	else:
		balance = myToken.getBalance(accounts[0])
		print("Host accounts: %s" %(accounts))
		print("coinbase balance:%d" %(balance))