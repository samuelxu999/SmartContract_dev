// scripts/NFT_AC.demo.js
const { expect } = require('chai');

const { BN, constants, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');

const { ZERO_ADDRESS } = constants;

//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('./addr_list.json');	
	return addrlist[node_name];	
};

async function main () {
	// // Our code will go here
	// // Retrieve accounts from the local node
	const accounts = await ethers.provider.listAccounts();
	// console.log(accounts);
	// print all accounts
	console.log('All accounts:');
	for (i = 0; i < accounts.length; i++) { 
		// display one account
		console.log(`[${i+1}] ${accounts[i]}`);
	}

	// Set up an ethers contract, representing our deployed Box instance
	const contractAddress = getAddress('NFT_AC');
	const NFT_AC = await ethers.getContractFactory('NFT_AC');
	const nft_ac = await NFT_AC.attach(contractAddress);

	// get token name and symbol
	const token_name = await nft_ac.name();
	const token_symbol = await nft_ac.symbol();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}`)

	// setup parameters
	var token = new BN(getAddress('token1')).toString();
	var mint_account = accounts[0]

	// mint token by mint_account
	console.log(`mint token_id:${token} by: ${mint_account}`)
	await nft_ac.mint(mint_account, token);

	// Query token balance of an account
	var value = await nft_ac.balanceOf(mint_account);
	console.log(`${mint_account} has token banalce ${value.toString()}`);

	// Check if a token existed
	var token_existed = await nft_ac.exists(token);
	console.log(`Token id: ${token} exists: ${token_existed}`);

	// Query the owner given a token id
	var owner_address = await nft_ac.ownerOf(token);
	console.log(`Token id: ${token} has owner ${owner_address}`);

	// burn token in test
	console.log(`burn token_id:${token}`)
	await nft_ac.burn(token);

	// Check if a token existed
	var token_existed = await nft_ac.exists(token);
	console.log(`Token id: ${token} exists: ${token_existed}`);
	
	// Query token balance of an account
	var value = await nft_ac.balanceOf(mint_account);
	console.log(`${mint_account} has token banalce ${value.toString()}`);

}

//================================= test demo ==================================
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });