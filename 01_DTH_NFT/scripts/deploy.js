// scripts/deploy.js
// const hre = require("hardhat");

async function main() {
  // We get the NFT_AC contract to deploy
  var name = 'NFT-CapAC';
  var symbol = 'CapAC';
  const NFT_CapAC = await ethers.getContractFactory('NFT_CapAC');
  console.log('Deploying NFT_CapAC...');
  const nft_ac = await NFT_CapAC.deploy(name,symbol);
  await nft_ac.deployed();

  console.log('NFT_CapAC deployed to:', nft_ac.address);
  
  // We get the NFT_Data contract to deploy
  name = 'NFT-Data';
  symbol = 'Data';
  const NFT_Data = await ethers.getContractFactory('NFT_Data');
  console.log('Deploying NFT_Data...');
  const nft_data = await NFT_Data.deploy(name,symbol);
  await nft_data.deployed();

  console.log('NFT_Data deployed to:', nft_data.address);
}

// We recommend this pattern to be able to use async/await everywhere
main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
