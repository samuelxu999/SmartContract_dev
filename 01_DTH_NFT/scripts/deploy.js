// scripts/deploy.js
// const hre = require("hardhat");

async function main() {
  // We get the NFT_AC contract to deploy
  const name = 'Non Fungible Token';
  const symbol = 'NFT';
  const NFT_AC = await ethers.getContractFactory('NFT_AC');
  console.log('Deploying NFT_AC...');
  const nft_ac = await NFT_AC.deploy(name,symbol);
  await nft_ac.deployed();

  console.log('NFT_AC deployed to:', nft_ac.address);
}

// We recommend this pattern to be able to use async/await everywhere
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
