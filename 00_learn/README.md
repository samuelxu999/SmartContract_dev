# Sample Hardhat Project for learning process

This project demonstrates a basic Hardhat use case. It comes with a sample contract, a test for that contract, and a script that deploys that contract.

reference:https://docs.openzeppelin.com/learn/

## Organization of project

|   name   | Description |
|:----------:|-------------|
| contracts | src folder containing all smart contract source files (*.sol). |
| scripts | scrpts directory containing deploy.js and other demo cases, e.g,. index.js. |
| test | unit test folder containeing all test cases file (*.js). |
| hardhat.config.js | configuration file for hardhat environment. |
| package.json | save all dependencies and packages for node.js. |
| truffle-config.js | configuration file for truffle environment. |


## Preparation

1) install truffle:
```shell
npm install -g truffle
```

2) install Hardhat and other packages
```shell
npm install				// install items from package.json
npx hardhat help		// list help information for npx hardhat	
```

3) For hardhat.config.js and truffle-config.js, you need to change compilers-->solc to current solidity verions. 

To check current solidity version:
```shell
truffle version
```

## Using Hardhat to compile, deploy and test smart contracts

### 1) compile and run unit test:

```shell
npx hardhat compile		// compile all contracts
npx hardhat test		// execute unit test cases
```

### 2) deploy smart contrac on local hardhat test network and run demo

a) First of all, you need launch a local hardhat test network and let it run background.

```shell
screen -S hardhat_node  // open a screen session called hardhat_node and attach it
npx hardhat node        // launch a local hardhat for test
ctrl+A+D 				// detach screen and leave node runing in background
screen -r hardhat_node  // attach hardhat_node screen session
```

b) deploy and test demo cases.
```shell
npx hardhat run --network localhost scripts/deploy.js	// deploy contracts on local hardhat network
npx hardhat run --network localhost ./scripts/index.js	// execute scripts
```