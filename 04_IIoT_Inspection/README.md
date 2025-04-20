# DIW_authentication Project

This project implement a prototype of a decentralized digital markering authentication for visual inspection system under smart manufacturing environments in Industry 4.0.


## Run IPFS test network.

Refer to https://github.com/samuelxu999/Course_dev/tree/main/01_Blockchain/02_IPFS


## You can run local miners as test network.

Refer to https://github.com/samuelxu999/Course_dev/tree/main/01_Blockchain/04_Ethereum/boot_network


## Install required tools: ganache-cli and truffle
```shell
npm install -g ganache-cli  // install ganache to run test Ethereum network
npm install -g truffle  // install truffle to compile contract and deploy chain code
npm install				// install packages and dependencies
```

## You can also setup ganache as test network.

1) Opne a new terminal, then run ganache-cli:
```shell
screen -S ganache_node						// open a screen session called ganache_node and attach it
ganache-cli -i 5777 --gasLimit 10000000 --port 8544		// launch a ganache-cli for ethereum test network, use port 8544.
ctrl+A+D 									// detach screen and leave node runing in background
screen -r ganache_node  					// attach ganache_node screen session to get information
```


2) compile contracts and migrate to local network.
```shell
// compile contracts
truffle compile	

// deploy contracts on local network (You need properly setup networks->development in truffle-config.js)
truffle migrate --reset
```

## Demo and test cases.

1) Update configuration data in "./src/config/addr_list.json".

--- HttpProvider: replace with you local geth interface 'ip:port'

--- NFT_Data: replace with deployed contract address

--- host_account: input coinbase account used in your local geth node.

1) Contract wrapper unit test.
```shell
cd src
// execute NFT_Data.py containing unit test cases
python3 NFT_Data.py -h  	// get usages
python3 NFT_Data.py --test_op 0		// display main account and data tokens.
python3 NFT_Data.py --test_op 1 --id token1		// query token1 
python3 NFT_Data.py --test_op 2 --id token1 --op_status 0		// mint token1 by owner
python3 NFT_Data.py --test_op 2 --id token2 --op_status 1		// mint token2 by other account
python3 NFT_Data.py --test_op 3 --id token1		// burn token by id
python3 NFT_Data.py --test_op 4 --id token1	--value "prod1,mkroot,cid1:cid2:hash1:hash2"	// update reference data
```


3) To test on local network, you can try following commands.
```shell
cd src
// execute test_demo.py containing demo and performance evaluation
python3 test_demo.py -h  													// get usages
python3 test_demo.py --test_func 0											// display main account and data tokens.
python3 test_demo.py --test_func 1 --id 1									// query by id 
python3 test_demo.py --test_func 2 --value host_account --tx_round 10		// mint tokens by owner, ids range in [args.id+1, args.id+10]
python3 test_demo.py --test_func 2 --value other_account					// mint a token by other, use default id=1
python3 test_demo.py --test_func 3 --value host_account --tx_round 10		// burn tokens by owner, ids range in [args.id+1, args.id+10]
python3 test_demo.py --test_func 4  --value 10 --op_status 1 --tx_round 5	// Use 10 figures in folder "src/test_fig" to create MKT of frames and save results into a token with ids range in [args.id+1, args.id+10]
python3 test_demo.py --test_func 5 --op_status 1 --tx_round 5 				// Audit token data ids range in [args.id+1, args.id+10]
```


4) To test on webservice, you can try following commands.
```shell
cd src

// execute server app
python3 NFT_Server.py

// execute client app to run test cases			
python3 Test_Client.py -h  							// get usages
python3 Test_Client.py --test_func 0 				// query main account and data tokens. 
python3 Test_Client.py --test_func 1 --id 5 		// query a token by id=5
python3 Test_Client.py --test_func 2 --id 1 --thread_count 10 --tx_round 2 		// bindle multiple token query (threads) in a process, ids range in [args.id+1, args.id+10], repeat test count: 2.
```