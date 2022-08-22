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


const test_basic = async () => {
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
	const contractAddress = getAddress('NFT_CapAC');
	const NFT_CapAC = await ethers.getContractFactory('NFT_CapAC');
	const nft_ac = await NFT_CapAC.attach(contractAddress);

	// get token name and symbol
	const token_name = await nft_ac.name();
	const token_symbol = await nft_ac.symbol();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}`)

	// setup parameters
	var token = new BN(getAddress('token1')).toString();
	var mint_account = accounts[0]
	var other_account = accounts[1]

	// ---------- mint token by mint_account --------------
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

	// Query totalSupply of current NFT
	var value = await nft_ac.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)

	// ----------------- burn token in test ------------------
	console.log(`burn token_id:${token}`)
	await nft_ac.burn(token);

	// Check if a token existed
	var token_existed = await nft_ac.exists(token);
	console.log(`Token id: ${token} exists: ${token_existed}`);
	
	// Query token balance of an account
	var value = await nft_ac.balanceOf(mint_account);
	console.log(`${mint_account} has token banalce ${value.toString()}`);

	// Query totalSupply of current NFT
	var value = await nft_ac.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)

	var value = await nft_ac.query_CapAC(token);
	console.log(`query_CapAC token_id:${token}, CapAC:${value}`)
};

const test_CapAC = async () => {
	// // Our code will go here
	// // Retrieve accounts from the local node
	const accounts = await ethers.provider.listAccounts();

	// Set up an ethers contract, representing our deployed Box instance
	const contractAddress = getAddress('NFT_CapAC');
	const NFT_CapAC = await ethers.getContractFactory('NFT_CapAC');
	const nft_ac = await NFT_CapAC.attach(contractAddress);

	// get token name and symbol
	const token_name = await nft_ac.name();
	const token_symbol = await nft_ac.symbol();

	// setup parameters
	var token = new BN(getAddress('token1')).toString();
	var other_token = new BN(getAddress('token2')).toString();
	var mint_account = accounts[0]
	var other_account = accounts[1]

	// ---------- mint token by mint_account --------------
	console.log(`mint token_id:${token} by: ${mint_account}`)
	await nft_ac.mint(mint_account, token);

	// ---------- mint token by other_account --------------
	console.log(`mint token_id:${other_token} by: ${other_account}`)
	await nft_ac.mint(other_account, other_token);

	// Query totalSupply of current NFT
	var value = await nft_ac.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)

	// ----------------- AC test ---------------------------
	var value = await nft_ac.query_CapAC(token);
	console.log(`query_CapAC token_id:${token}, CapAC:${value}`)
	var value = await nft_ac.query_CapAC(other_token);
	console.log(`query_CapAC token_id:${other_token}, CapAC:${value}`)

	// update CapAC1
	console.log(`set setCapAC_expireddate token_id:${token} by: ${mint_account}`)
	await nft_ac.setCapAC_expireddate(token, 12345, 67890);

	console.log(`set setCapAC_authorization token_id:${token} by: ${mint_account}`)
	await nft_ac.setCapAC_authorization(token, 'samuel has access!');

	var value = await nft_ac.query_CapAC(token);
	console.log(`query_CapAC token_id:${token}, CapAC:${value}`)
	var value = await nft_ac.query_CapAC(other_token);
	console.log(`query_CapAC token_id:${other_token}, CapAC:${value}`)

	// update CapAC2
	console.log(`set setCapAC_expireddate token_id:${other_token} by: ${other_account}`)
	await nft_ac.setCapAC_expireddate(other_token, 0, 0);

	console.log(`set setCapAC_authorization token_id:${other_token} by: ${other_account}`)
	await nft_ac.setCapAC_authorization(other_token, 'samuel has no access!');

	var value = await nft_ac.query_CapAC(token);
	console.log(`query_CapAC token_id:${token}, CapAC:${value}`)
	var value = await nft_ac.query_CapAC(other_token);
	console.log(`query_CapAC token_id:${other_token}, CapAC:${value}`)

	// ----------------- burn token in test ------------------
	console.log(`burn token_id:${token}`)
	await nft_ac.burn(token);
	console.log(`burn token_id:${other_token}`)
	await nft_ac.burn(other_token);

	var value = await nft_ac.query_CapAC(token);
	console.log(`query_CapAC token_id:${token}, CapAC:${value}`)
	var value = await nft_ac.query_CapAC(other_token);
	console.log(`query_CapAC token_id:${other_token}, CapAC:${value}`)

	// Query totalSupply of current NFT
	var value = await nft_ac.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)
}

async function main () {
	// await test_basic();
	await test_CapAC();

}

//================================= test demo ==================================
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });