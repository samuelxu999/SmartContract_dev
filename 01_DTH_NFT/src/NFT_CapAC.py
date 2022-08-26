
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
			## Change account address to EIP checksum format
			checksumAddr = Web3.toChecksumAddress(owner)
			tx_hash = self.contract.functions.mint(checksumAddr, int(tokenId)).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## burn a token
	def burn_CapAC(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.burn(int(tokenId)).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## setCapAC_expireddate
	def CapAC_expireddate(self, tokenId, ini_date, exp_date):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.setCapAC_expireddate(int(tokenId), ini_date, exp_date).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## setCapAC_authorization
	def CapAC_authorization(self, tokenId, ac_right):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.setCapAC_authorization(int(tokenId), ac_right).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	##get owner of a token id
	def ownerToken(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			return self.contract.functions.ownerOf(int(tokenId)).call({'from': self.web3.eth.coinbase})
		return None

	## query value from a token
	def query_CapAC(self, tokenId):
		return self.contract.functions.query_CapAC(int(tokenId)).call({'from': self.web3.eth.coinbase})

	## query totalSupply of tokens
	def query_totalSupply(self):
		return self.contract.functions.totalSupply().call({'from': self.web3.eth.coinbase})

	## query tokenId by index in totalSupply
	def query_tokenByIndex(self, index):
		return self.contract.functions.tokenByIndex(int(index)).call({'from': self.web3.eth.coinbase})

def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run NFT_CapAC."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-contract information, \
                        1-query_CapAC, \
                        2-mint_CapAC, \
                        3-burn_CapAC, \
                        4-CapAC_expireddate, \
                        5-CapAC_authorization")

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
		token_value = myToken.query_CapAC(tokenId)
		owner = myToken.ownerToken(tokenId)
		print("Token_id:{}   owner:{}  CapAC:{}".format(tokenId, owner, token_value))
	elif(args.test_op==2):
		tokenId=NFT_CapAC.getAddress(args.id)
		other_account = NFT_CapAC.getAddress('other_account')
		if(args.op_status==1):
			receipt = myToken.mint_CapAC(tokenId, other_account)
			## print out receipt
			if(receipt!=None):
				print('Token {} is mint by {}'.format(tokenId,other_account))
				print(receipt)
			else:
				owner = myToken.ownerToken(tokenId)
				print('Token {} has been mint by {}'.format(tokenId, owner))
		else:
			receipt = myToken.mint_CapAC(tokenId, accounts[0])
			## print out receipt
			if(receipt!=None):
				print('Token {} is mint by {}'.format(tokenId,accounts[0]))
				print(receipt)
			else:
				owner = myToken.ownerToken(tokenId)
				print('Token {} has been mint by {}'.format(tokenId, owner))

	elif(args.test_op==3):
		tokenId = NFT_CapAC.getAddress(args.id)
		owner = myToken.ownerToken(tokenId)
		receipt = myToken.burn_CapAC(tokenId)
		if(receipt!=None):
			print('Token {} is burn by owner {}'.format(tokenId, owner))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))
	elif(args.test_op==4):
		tokenId=NFT_CapAC.getAddress(args.id)

		#set issue date and expired date
		issue_time = 1661530882369
		expire_time = 1661617282369

		receipt = myToken.CapAC_expireddate(tokenId, issue_time, expire_time)
		if(receipt!=None):
			print('Token {} setCapAC_expireddate'.format(tokenId))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))
	elif(args.test_op==5):
		tokenId=NFT_CapAC.getAddress(args.id)
		receipt = myToken.CapAC_authorization(tokenId, args.value)
		if(receipt!=None):
			print('Token {} setCapAC_authorization'.format(tokenId))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))		
	else:
		balance = myToken.getBalance(accounts[0])
		total_supply = myToken.query_totalSupply()
		print("host accounts: %s" %(accounts))
		print("coinbase balance:%d" %(balance))
		print("total supply: %d" %(total_supply))
		ls_token = []
		for idx in range(total_supply):
			ls_token.append(myToken.query_tokenByIndex(idx))
		print(ls_token)