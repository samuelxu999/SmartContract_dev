// scripts/NFT_AC.demo.js
const { expect } = require('chai');

const { BN, constants, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');

const { ZERO_ADDRESS } = constants;

async function main () {
	// // Our code will go here
	// // Retrieve accounts from the local node
	const accounts = await ethers.provider.listAccounts();
	console.log(accounts);
	// Set up an ethers contract, representing our deployed Box instance
	const address = '0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512';
	const NFT_AC = await ethers.getContractFactory('NFT_AC');

	const name = 'Non Fungible Token';
	const symbol = 'NFT';

	const firstTokenId = new BN('5041').toString();
	console.log(firstTokenId)

	const nft_ac = await NFT_AC.attach(address);
	// await nft_ac.mint(accounts[0], firstTokenId);

	const value = await nft_ac.balanceOf(accounts[0]);
	console.log('nft_ac value is', value.toString());

}

//================================= test demo ==================================
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });