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
	var contractAddress = getAddress('NFT_AC');
	const NFT_AC = await ethers.getContractFactory('NFT_AC');

	const name = 'Non Fungible Token';
	const symbol = 'NFT';

	const token_id = new BN(getAddress('token3')).toString();
	console.log(`token id:${token_id}`)

	mint_account = accounts[0]
	const nft_ac = await NFT_AC.attach(contractAddress);
	// await nft_ac.mint(mint_account, token_id);

	const value = await nft_ac.balanceOf(accounts[0]);
	console.log(`${mint_account} has token banalce ${value.toString()}`);

}

//================================= test demo ==================================
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });