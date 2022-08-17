// scripts/deploy.js
async function main () {
  // We get the contract to deploy
  const Box = await ethers.getContractFactory('Box');
  console.log('Deploying Box...');
  const box = await Box.deploy();
  await box.deployed();

  console.log('BoxPro deployed to:', box.address);
  const BoxPro = await ethers.getContractFactory('BoxPro');
  console.log('Deploying BoxPro...');
  const boxpro = await BoxPro.deploy();
  await boxpro.deployed();
  console.log('BoxPro deployed to:', boxpro.address);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
