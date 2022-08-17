// scripts/index.js
async function main () {
  // Our code will go here
  // Retrieve accounts from the local node
  // const accounts = await ethers.provider.listAccounts();
  // console.log(accounts);
  // Set up an ethers contract, representing our deployed Box instance
  const address = '0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9';
  const Box = await ethers.getContractFactory('Box');
  const box = await Box.attach(address);
  // Call the retrieve() function of the deployed Box contract
  const value = await box.retrieve();
  console.log('Box value is', value.toString());

  // Send a transaction to store() a new value in the Box
  if(value<=0){
    await box.store(value+23);
  }
  else{
    await box.store(value-23);
  }

  // Call the retrieve() function of the deployed Box contract
  const unpdate_value = await box.retrieve();
  console.log('Box value is', unpdate_value.toString());
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });
