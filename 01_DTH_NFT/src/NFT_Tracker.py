
'''
========================
NFT_Tracker module
========================
Created on August.21, 2022
@author: Xu Ronghua
@Email:  rxu22@binghamton.edu
@TaskDescription: This module provide encapsulation of web3.py API to interact with NFT_Tracker smart contract.
'''
from web3 import Web3, HTTPProvider, IPCProvider
import json, datetime, time
import sys
import argparse

class NFT_Tracker(object):
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
	def mint_Tracker(self, tokenId, owner):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(not token_existed):
			## Change account address to EIP checksum format
			checksumAddr = Web3.toChecksumAddress(owner)
			tx_hash = self.contract.functions.mint(checksumAddr, int(tokenId)).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## burn a token
	def burn_Tracker(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.burn(int(tokenId)).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	## set tokenURI
	def set_tokenURI(self, tokenId, _tokenURI):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			tx_hash = self.contract.functions.setTokenURI(int(tokenId), _tokenURI).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	##get owner of a token id
	def ownerToken(self, tokenId):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		if(token_existed):
			return self.contract.functions.ownerOf(int(tokenId)).call({'from': self.web3.eth.coinbase})
		return None

	def get_tokenURI(self, tokenId):
		return self.contract.functions.tokenURI(int(tokenId)).call({'from': self.web3.eth.coinbase})

	## send transfer()
	def transfer_DataTracker(self, tokenId, sender, receiver):
		token_existed = self.contract.functions.exists(int(tokenId)).call({'from': self.web3.eth.coinbase})
		_sender = Web3.toChecksumAddress(sender)
		_receiver = Web3.toChecksumAddress(receiver)
		if(token_existed):
			tx_hash = self.contract.functions.transfer(int(tokenId), _sender, _receiver).transact({'from': self.web3.eth.coinbase})
			return self.web3.eth.wait_for_transaction_receipt(tx_hash)
		else:
			return None

	def get_DataTracker(self, tokenId, index):
		return self.contract.functions.query_DataTracker(int(tokenId), int(index)).call({'from': self.web3.eth.coinbase})

	def get_totalTracker(self, tokenId):
		return self.contract.functions.total(int(tokenId)).call({'from': self.web3.eth.coinbase})

	## query totalSupply of tokens
	def query_totalSupply(self):
		return self.contract.functions.totalSupply().call({'from': self.web3.eth.coinbase})

	## query tokenId by index in totalSupply
	def query_tokenByIndex(self, index):
		return self.contract.functions.tokenByIndex(int(index)).call({'from': self.web3.eth.coinbase})

def define_and_get_arguments(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Run NFT_Tracker."
    )
    parser.add_argument("--test_op", type=int, default=0, 
                        help="Execute test operation: \
                        0-contract information, \
                        1-query_DataTracker, \
                        2-mint_Tracker, \
                        3-burn_Tracker, \
                        4-set_tokenURI, \
                        5-transfer_DataTracker")

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

	httpProvider = NFT_Tracker.getAddress('HttpProvider')
	contractAddr = NFT_Tracker.getAddress('NFT_Tracker')
	contractConfig = '../build/contracts/NFT_Tracker.json'

	## new NFT_Tracker instance
	myToken = NFT_Tracker(httpProvider, contractAddr, contractConfig)

	accounts = myToken.getAccounts()

	## switch test cases
	if(args.test_op==1):
		tokenId=NFT_Tracker.getAddress(args.id)
		owner = myToken.ownerToken(tokenId)
		if(owner!=None):	
			token_URI = myToken.get_tokenURI(tokenId)
		else:
			token_URI = ""
		tracker_length = myToken.get_totalTracker(tokenId)
		print("Token_id:{}  owner: {}   token_URI:{}   tracker num: {}".format(tokenId, owner, token_URI, tracker_length))
		for idx in range(tracker_length):
			tracker_data = myToken.get_DataTracker(tokenId, idx)
			print("sender:{}   receiver:{}".format(tracker_data[0], tracker_data[1]))

	elif(args.test_op==2):
		tokenId=NFT_Tracker.getAddress(args.id)
		other_account = NFT_Tracker.getAddress('other_account')
		if(args.op_status==1):
			receipt = myToken.mint_Tracker(tokenId, other_account)
			if(receipt!=None):
				print('Token {} is mint by {}'.format(tokenId,other_account))
				print(receipt)
			else:
				owner = myToken.ownerToken(tokenId)
				print('Token {} has been mint by {}'.format(tokenId, owner))
		else:
			receipt = myToken.mint_Tracker(tokenId, accounts[0])
			## print out receipt
			if(receipt!=None):
				print('Token {} is mint by {}'.format(tokenId,accounts[0]))
				print(receipt)
			else:
				owner = myToken.ownerToken(tokenId)
				print('Token {} has been mint by {}'.format(tokenId, owner))
	elif(args.test_op==3):
		tokenId=NFT_Tracker.getAddress(args.id)
		owner = myToken.ownerToken(tokenId)
		receipt = myToken.burn_Tracker(tokenId)
		if(receipt!=None):
			print('Token {} is burn by owner {}'.format(tokenId, owner))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))
	elif(args.test_op==4):
		tokenId=NFT_Tracker.getAddress(args.id)
		tokenURI = args.value
		receipt = myToken.set_tokenURI(tokenId, tokenURI)
		if(receipt!=None):
			print('Token {} set_tokenURI: {}'.format(tokenId, tokenURI))
			print(receipt)
		else:
			print('Token {} is not existed'.format(tokenId))
	elif(args.test_op==5):
		tokenId=NFT_Tracker.getAddress(args.id)
		sender = NFT_Tracker.getAddress('host_account')
		receiver = NFT_Tracker.getAddress('other_account')
		receipt = myToken.transfer_DataTracker(tokenId, sender, receiver)
		if(receipt!=None):
			print('Token {} transferred'.format(tokenId))
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