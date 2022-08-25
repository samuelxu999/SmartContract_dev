
'''
========================
NFT_Data module
========================
Created on August.21, 2022
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with NFT_Data smart contract.
'''
from web3 import Web3, HTTPProvider, IPCProvider
import json, datetime, time
import sys
import argparse

class NFT_Data(object):
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
	def mint_Data(self, tokenId, owner):
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
	def burn_Data(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			owner = self.contract.functions.ownerOf(int(tokenId)).call({'from': self.web3.eth.coinbase})
			print('Token {} is burn by owner {}'.format(tokenId,owner))
			tx_hash = self.contract.functions.burn(int(tokenId)).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## set baseURI
	def set_baseURI(self, _baseURI):
		print('setBaseURI'.format())
		tx_hash = self.contract.functions.setBaseURI(_baseURI).transact({'from': self.web3.eth.coinbase})
		receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
		print(receipt)


	## set tokenURI
	def set_tokenURI(self, tokenId, _tokenURI):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			print('Token {} set_tokenURI'.format(tokenId))
			tx_hash = self.contract.functions.setTokenURI(int(tokenId), _tokenURI).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## DataAC_setup
	def DataAC_setup(self, tokenId, ref_address, data_mac):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			print('Token {} setDataAC'.format(tokenId))
			tx_hash = self.contract.functions.setDataAC(int(tokenId), ref_address, data_mac).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## DataAC_authorization
	def DataAC_authorization(self, tokenId, ac_right):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			print('Token {} setDataAC_authorization'.format(tokenId))
			tx_hash = self.contract.functions.setDataAC_authorization(int(tokenId), ac_right).transact({'from': self.web3.eth.coinbase})
			receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))

	## query data from a token, like baseURI and tokenURI
	def query_Data(self, tokenId):
		base_URI = self.contract.functions.baseURI().call({'from': self.web3.eth.coinbase})

		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			token_URI = self.contract.functions.tokenURI(int(tokenId)).call({'from': self.web3.eth.coinbase})
			print("Token_id:{}  base_URI:{}   token_URI:{}".format(tokenId, base_URI, token_URI))
		else:
			print("Token_id:{}  base_URI:{}".format(tokenId, base_URI))

		data_ac = self.contract.functions.query_DataAC(int(tokenId)).call({'from': self.web3.eth.coinbase})
		print("DataAC,  id:{}  ref_address:{}   data_mac:{}   access_rights:{}".format(data_ac[0], data_ac[1], data_ac[2], data_ac[3]))


def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run NFT_Data."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-contract information, \
                        1-query_Data, \
                        2-mint_Data, \
                        3-burn_Data, \
                        4-set_baseURI, \
                        5-set_tokenURI, \
                        6-DataAC_setup, \
                        7-DataAC_authorization")

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

	httpProvider = NFT_Data.getAddress('HttpProvider')
	contractAddr = NFT_Data.getAddress('NFT_Data')
	contractConfig = '../build/contracts/NFT_Data.json'

	## new NFT_Data instance
	myToken = NFT_Data(httpProvider, contractAddr, contractConfig)

	accounts = myToken.getAccounts()

	## switch test cases
	if(args.test_op==1):
		tokenId=NFT_Data.getAddress(args.id)
		myToken.query_Data(tokenId)
	elif(args.test_op==2):
		tokenId=NFT_Data.getAddress(args.id)
		other_account = NFT_Data.getAddress('other_account')
		if(args.op_status==1):
			myToken.mint_Data(tokenId, other_account)
		else:
			 myToken.mint_Data(tokenId, accounts[0])
	elif(args.test_op==3):
		tokenId=NFT_Data.getAddress(args.id)
		myToken.burn_Data(tokenId)
	elif(args.test_op==4):
		baseURI = args.value
		myToken.set_baseURI(baseURI)
	elif(args.test_op==5):
		tokenId=NFT_Data.getAddress(args.id)
		tokenURI = args.value
		myToken.set_tokenURI(tokenId, tokenURI)
	elif(args.test_op==6):
		tokenId=NFT_Data.getAddress(args.id)
		[ref_address, data_mac] = args.value.split(',')
		myToken.DataAC_setup(tokenId, ref_address, data_mac)
	elif(args.test_op==7):
		tokenId=NFT_Data.getAddress(args.id)
		myToken.DataAC_authorization(tokenId, args.value)		
	else:
		balance = myToken.getBalance(accounts[0])
		print("Host accounts: %s" %(accounts))
		print("coinbase balance:%d" %(balance))