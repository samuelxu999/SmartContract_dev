# DTH_NFT Project

This project implement a prototype of secure NFT based digital twin healthcare (DTH) system.


## test folder includes unti test scripts and you can use Hardhat to run test suites.

1) For hardhat installation:
```shell
npm install				// install packages and dependencies
npx hardhat help		// list help information for npx hardhat
```

2) You can launch a screen sesstion to launch a local hardhat for test. 
```shell
screen -S hardhat_node  // open a screen session called hardhat_node and attach it
npx hardhat node        // launch a local hardhat for test
ctrl+A+D 				// detach screen and leave node runing in background
screen -r hardhat_node  // attach hardhat_node screen session
````

3) Run test on hardhat, you can try following commands. 
```shell
npx hardhat compile		// compile all contracts
npx hardhat run --network localhost scripts/deploy.js	// deploy contracts on local hardhat network
npx hardhat run --network localhost ./scripts/index.js	// execute *demo.js scripts
npx hardhat test		// execute unit test cases
````

## You can also setup local miners as test network.

You need check these points:

-- ensure local miners are running

-- enable networks->development in truffle-config.js 

-- correct deploy functions in 2_deploy_contracts.js

1) compile contracts and migrate to local network.
```shell
// compile contracts
truffle compile	

// deploy contracts on local network (enable networks->development in truffle-config.js)
truffle migrate --reset
````

2) To test on local network, you can try following commands.
```shell
cd src
// execute demo test cases (py), e.g,. NFT_CapAC.py
python3 NFT_CapAC.py -h  						// get usages
python3 NFT_CapAC.py --test_op 0				// display all accounts
python3 NFT_CapAC.py --test_op 1 --id token1	// query token1 
python3 NFT_CapAC.py --test_op 2 --id token1 --op_status 0	// mint token1 by owner
python3 NFT_CapAC.py --test_op 2 --id token2 --op_status 1	// mint token2 by other
python3 NFT_CapAC.py --test_op 3 --id token1	// burn token1
python3 NFT_CapAC.py --test_op 4 --id token1	// update AC expired date of token1
python3 NFT_CapAC.py --test_op 5 --id token1 --value "Assign access right!" // assign rights to token1
````