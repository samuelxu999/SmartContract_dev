
'''
========================
NFT_Data module
========================
Created on April.20, 20252
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
		address_json = json.load(open('./config/addr_list.json'))
		return address_json[node_name]

	## mint a token
	def mint_Data(self, tokenId, owner):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(not token_existed):
			## Change account address to EIP checksum format
			checksumAddr = Web3.toChecksumAddress(owner)
			tx_hash = self.contract.functions.mint(checksumAddr, int(tokenId)).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## burn a token
	def burn_Data(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.burn(int(tokenId)).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## DataRef_setup
	def DataRef_setup(self, tokenId, prod_id, mkt_root, data_mac):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.setDataAC(int(tokenId), prod_id, mkt_root, data_mac).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	##get owner of a token id
	def ownerToken(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			return self.contract.functions.ownerOf(int(tokenId)).call({'from': self.web3.eth.coinbase})
		return None

	def get_DataRef(self, tokenId):
		return self.contract.functions.query_DataAC(int(tokenId)).call({'from': self.web3.eth.coinbase})

	## query totalSupply of tokens
	def query_totalSupply(self):
		return self.contract.functions.totalSupply().call({'from': self.web3.eth.coinbase})

	## query tokenId by index in totalSupply
	def query_tokenByIndex(self, index):
		return self.contract.functions.tokenByIndex(int(index)).call({'from': self.web3.eth.coinbase})

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
                        4-DataRef_setup")

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
		owner = myToken.ownerToken(tokenId)	

		## show current owner
		print("Token_id:{}  owner: {}".format(tokenId, owner))

		## show product and reference informaition
		data_ac = myToken.get_DataRef(tokenId)
		print("Product Reference,  id:{}  prod_id:{}   mkt_root:{}   data_mac:{}   total_mac:{}".format(data_ac[0], data_ac[1], data_ac[2], data_ac[3], data_ac[4]))

	elif(args.test_op==2):
		tokenId=NFT_Data.getAddress(args.id)
		other_account = NFT_Data.getAddress('other_account')
		if(args.op_status==1):
			receipt = myToken.mint_Data(tokenId, other_account)
			if(receipt!=None):
				print('Token {} is mint by {}'.format(tokenId,other_account))
				print(receipt)
			else:
				owner = myToken.ownerToken(tokenId)
				print('Token {} has been mint by {}'.format(tokenId, owner))
		else:
			receipt = myToken.mint_Data(tokenId, accounts[0])
			## print out receipt
			if(receipt!=None):
				print('Token {} is mint by {}'.format(tokenId,accounts[0]))
				print(receipt)
			else:
				owner = myToken.ownerToken(tokenId)
				print('Token {} has been mint by {}'.format(tokenId, owner))
	elif(args.test_op==3):
		tokenId=NFT_Data.getAddress(args.id)
		owner = myToken.ownerToken(tokenId)
		receipt = myToken.burn_Data(tokenId)
		if(receipt!=None):
			print('Token {} is burn by owner {}'.format(tokenId, owner))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))
	elif(args.test_op==4):
		tokenId=NFT_Data.getAddress(args.id)

		## parse test data
		[prod_id, mkt_root, str_data_mac] = args.value.split(',')

		## get ref data
		data_mac = str_data_mac.split(':')

		## invoke transaction to save reference data 
		receipt = myToken.DataRef_setup(tokenId, prod_id, mkt_root, data_mac)
		if(receipt!=None):
			print('Token {} setDataRef'.format(tokenId))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))	
	else:
		balance = myToken.getBalance(accounts[0])
		total_supply = myToken.query_totalSupply()
		print("Host accounts: %s" %(accounts))
		print("coinbase balance:%d" %(balance))
		print("total supply: %d" %(total_supply))
		ls_token = []
		for idx in range(total_supply):
			ls_token.append(myToken.query_tokenByIndex(idx))
		print(ls_token)