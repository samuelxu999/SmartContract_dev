// scripts/deploy.js
// const hre = require("hardhat");

async function main() {
  // We get the NFT_AC contract to deploy
  const name = 'NFT-CapAC';
  const symbol = 'CapAC';
  const NFT_CapAC = await ethers.getContractFactory('NFT_CapAC');
  console.log('Deploying NFT_CapAC...');
  const nft_ac = await NFT_CapAC.deploy(name,symbol);
  await nft_ac.deployed();

  console.log('NFT_CapAC deployed to:', nft_ac.address);
}

// We recommend this pattern to be able to use async/await everywhere
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
