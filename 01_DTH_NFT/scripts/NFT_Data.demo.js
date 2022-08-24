// scripts/NFT_Data.demo.js
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
	const contractAddress = getAddress('NFT_Data');
	const NFT_Data = await ethers.getContractFactory('NFT_Data');
	const nft_data = await NFT_Data.attach(contractAddress);

	// get token name and symbol
	const token_name = await nft_data.name();
	const token_symbol = await nft_data.symbol();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}`)

	// setup parameters
	var token = new BN(getAddress('token1')).toString();
	var mint_account = accounts[0]
	var other_account = accounts[1]

	// ---------- mint token by mint_account --------------
	console.log(`mint token_id:${token} by: ${mint_account}`)
	await nft_data.mint(mint_account, token);

	// Query token balance of an account
	var value = await nft_data.balanceOf(mint_account);
	console.log(`${mint_account} has token banalce ${value.toString()}`);

	// Check if a token existed
	var token_existed = await nft_data.exists(token);
	console.log(`Token id: ${token} exists: ${token_existed}`);

	// Query the owner given a token id
	var owner_address = await nft_data.ownerOf(token);
	console.log(`Token id: ${token} has owner ${owner_address}`);

	// Query totalSupply of current NFT
	var value = await nft_data.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)

	// ----------------- burn token in test ------------------
	console.log(`burn token_id:${token}`)
	await nft_data.burn(token);

	// Check if a token existed
	var token_existed = await nft_data.exists(token);
	console.log(`Token id: ${token} exists: ${token_existed}`);
	
	// Query token balance of an account
	var value = await nft_data.balanceOf(mint_account);
	console.log(`${mint_account} has token banalce ${value.toString()}`);

	// Query totalSupply of current NFT
	var value = await nft_data.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)
};

const test_Data = async () => {
	// // Our code will go here
	// // Retrieve accounts from the local node
	const accounts = await ethers.provider.listAccounts();

	// Set up an ethers contract, representing our deployed Box instance
	const contractAddress = getAddress('NFT_Data');
	const NFT_Data = await ethers.getContractFactory('NFT_Data');
	const nft_data = await NFT_Data.attach(contractAddress);

	// get token name and symbol
	const token_name = await nft_data.name();
	const token_symbol = await nft_data.symbol();

	// setup parameters
	var token = new BN(getAddress('token1')).toString();
	var other_token = new BN(getAddress('token2')).toString();
	var mint_account = accounts[0]
	var other_account = accounts[1]

	// ---------- mint token by mint_account --------------
	var token_existed = await nft_data.exists(token);
	if(token_existed==false) {
		console.log(`mint token_id:${token} by: ${mint_account}`)
		await nft_data.mint(mint_account, token);		
	}


	// ---------- mint token by other_account --------------
	var token_existed = await nft_data.exists(other_token);
	if(token_existed==false) {
		console.log(`mint token_id:${other_token} by: ${other_account}`)
		await nft_data.mint(other_account, other_token);
	}

	// Query totalSupply of current NFT
	var value = await nft_data.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)

	// ----------------- Data test ---------------------------
	var value = await nft_data.baseURI();
	console.log(`Query baseURI:${value}`);

	var value = await nft_data.tokenURI(token);
	console.log(`token_id: ${token}, tokenURI: ${value}`);

	var value = await nft_data.tokenURI(other_token);
	console.log(`token_id: ${other_token}, tokenURI: ${value}`);

	// set baseURI by owner
	console.log(`set baseURI by owner: ${mint_account}`)
	var baseURI = 'https://api.example.com/owner/';
	await nft_data.setBaseURI(baseURI, { from: mint_account });
	var value = await nft_data.baseURI();
	console.log(`Query baseURI:${value}`);

	// check default tokenURI
	var value = await nft_data.tokenURI(token);
	console.log(`token_id: ${token}, tokenURI: ${value}`);
	var value = await nft_data.tokenURI(other_token);
	console.log(`token_id: ${other_token}, tokenURI: ${value}`);

	// update token tokenURI by owner
	console.log(`set setTokenURI token_id:${token}`)
	await nft_data.setTokenURI(token, 'token1');

	// update token tokenURI by other
	console.log(`set setTokenURI token_id:${other_token}`)
	try {
		await nft_data.setTokenURI(other_token, 'token2');
	} catch (error) {
	  console.error(error);
	}
	
	// check updated tokenURI
	var value = await nft_data.tokenURI(token);
	console.log(`token_id: ${token}, tokenURI: ${value}`);
	var value = await nft_data.tokenURI(other_token);
	console.log(`token_id: ${other_token}, tokenURI: ${value}`);


	// ----------------- burn token in test ------------------
	console.log(`burn token_id:${token}`)
	await nft_data.burn(token);
	console.log(`burn token_id:${other_token}`)
	await nft_data.burn(other_token);

	// reset baseURI
	await nft_data.setBaseURI('');

	// qquery baseURI
	var value = await nft_data.baseURI();
	console.log(`Query baseURI:${value}`);

	try {
		var value = await nft_data.tokenURI(token);
		console.log(`token_id: ${token}, tokenURI: ${value}`);
	} catch (error) {
	  console.error(error);
	}

	try {
		var value = await nft_data.tokenURI(other_token);
		console.log(`token_id: ${other_token}, tokenURI: ${value}`);
	} catch (error) {
	  console.error(error);
	}

	// Query totalSupply of current NFT
	var value = await nft_data.totalSupply();
	console.log(`Token name: ${token_name}, symbol:${token_symbol}, totalSupply: ${value}`)
}

async function main () {
	// await test_basic();
	await test_Data();

}

//================================= test demo ==================================
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });