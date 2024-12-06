/* This is a demo test script to acces diamond facet */
/* global contract artifacts web3 before it assert */

// Initialize web3 instance
const { Web3 } = require('web3');
const web3 = new Web3();

// Create a new connection. Here we use local node's http provider
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));


// load contract 
const Diamond = require('../build/contracts/Diamond')
const DiamondCutFacet = require('../build/contracts/DiamondCutFacet')
const DiamondLoupeFacet = require('../build/contracts/DiamondLoupeFacet')
const OwnershipFacet = require('../build/contracts/OwnershipFacet')
const Test1Facet = require('../build/contracts/Test1Facet')
const Test2Facet = require('../build/contracts/Test2Facet')
const FacetCutAction = {
  Add: 0,
  Replace: 1,
  Remove: 2
}


function getSelectors (contract) {
  const selectors = contract.abi.reduce((acc, val) => {
    if (val.type === 'function') {
      // console.log(val.name)
      // get function signature
      let functionSignature = web3.eth.abi.encodeFunctionSignature(val);
      acc.push(functionSignature)
      return acc
    } else {
      return acc
    }
  }, [])
  return selectors
}

function getSelectorByName (contract, name) {
  const selector = contract.abi.reduce((acc, val) => {
    if (val.name === name) {
      // console.log(val.name)
      // get function signature
      let functionSignature = web3.eth.abi.encodeFunctionSignature(val);
      acc.push(functionSignature)
      return acc
    } else {
      return acc
    }
  }, [])
  return selector
}

function removeItem (array, item) {
  array.splice(array.indexOf(item), 1)
  return array
}

function findPositionInFacets (facetAddress, facets) {
  for (let i = 0; i < facets.length; i++) {
    if (facets[i].facetAddress === facetAddress) {
      return i
    }
  }
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}


async function DiamondTest() {
  var addresses = []

  const zeroAddress = '0x0000000000000000000000000000000000000000'
  // set diamond address
  const diamond_address = '0x5a971550087777b6589afB2D7aFA29aeFd7a5E88'
  const test1Facet_address = '0x646eB7D385d0B51A57ebD255050272322E171937'
  const test2Facet_address = '0x581B12229b133b59C136145A1220d5126992441a'


  var diamondCutFacet = new web3.eth.Contract(DiamondCutFacet.abi, diamond_address);
  var diamondLoupeFacet = new web3.eth.Contract(DiamondLoupeFacet.abi, diamond_address);
  var ownershipFacet = new web3.eth.Contract(OwnershipFacet.abi, diamond_address);


  // use first account as test account
  var accounts = await web3.eth.getAccounts();
  var test_account = accounts[0];
  console.log(test_account);

  console.log('should have three facets -- call to facetAddresses function')
  for (const address of await diamondLoupeFacet.methods.facetAddresses().call()) {
    addresses.push(address)
  }
  console.log(addresses.length==3)

  console.log('facets should have the right function selectors -- call to facetFunctionSelectors function')
  selectors = getSelectors(DiamondCutFacet)
  console.log(selectors)
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[0]).call()
  console.log(result)

  selectors = getSelectors(DiamondLoupeFacet)
  console.log(selectors)
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[1]).call()
  console.log(result)

  selectors = getSelectors(OwnershipFacet)
  console.log(selectors)
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[2]).call()
  console.log(result)

  console.log('selectors should be associated to facets correctly -- multiple calls to facetAddress function')
  result = await diamondLoupeFacet.methods.facetAddress('0x1f931c1c').call()
  console.log(result==addresses[0])
  result = await diamondLoupeFacet.methods.facetAddress('0xcdffacc6').call()
  console.log(result==addresses[1])
  result = await diamondLoupeFacet.methods.facetAddress('0x01ffc9a7').call()
  console.log(result==addresses[1])
  result = await diamondLoupeFacet.methods.facetAddress('0xf2fde38b').call()
  console.log(result==addresses[2])

  console.log('should get all the facets and function selectors of the diamond -- call to facets function')
  result = await diamondLoupeFacet.methods.facets().call()
  for (let i = 0; i < result.length; i++) {
    console.log(result[i].facetAddress)
    console.log(result[i].functionSelectors)
    console.log(result[i].facetAddress == addresses[i])
  }

  //------------- Add all test1 Facet functions ------------------------------
  console.log('should add all test1 functions')
  selectors = getSelectors(Test1Facet).slice(0, -1)
  console.log(selectors)
  addresses.push(test1Facet_address)
  await diamondCutFacet.methods
    .diamondCut([[test1Facet_address, FacetCutAction.Add, selectors]], zeroAddress, '0x')
    .send({ from: test_account, gas: 1000000 })
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[3]).call()
  console.log(result)

  //------------- Run test1 Facet functions -----------------------------------
  var test1Facet = new web3.eth.Contract(Test1Facet.abi, diamond_address);

  console.log('should test1 function call MyAddress')
  await test1Facet.methods.test1Func1(addresses[1]).send({ from: test_account, gas: 1000000 })
  myAddress = await test1Facet.methods.test1Func2().call()
  console.log(myAddress)

  console.log('should test1 function call MyNum')
  await test1Facet.methods.test1Func3(getRandomInt(100)).send({ from: test_account, gas: 1000000 })
  myNum = await test1Facet.methods.test1Func4().call()
  console.log(myNum)

  //------------- Remove and Add some test1 Facet functions ---------------------
  console.log('should remove some test1 functions')
  removeSelectors = getSelectorByName(Test1Facet, 'test1Func2')
  console.log(removeSelectors)
  await diamondCutFacet.methods
    .diamondCut([[zeroAddress, FacetCutAction.Remove, removeSelectors]], zeroAddress, '0x')
    .send({ from: test_account, gas: 6000000 })
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[3]).call()
  console.log(result)

  console.log('should add some test1 functions')
  addSelectors = getSelectorByName(Test1Facet, 'test1Func2')
  console.log(addSelectors)
  await diamondCutFacet.methods
    .diamondCut([[test1Facet_address, FacetCutAction.Add, addSelectors]], zeroAddress, '0x')
    .send({ from: test_account, gas: 1000000 })
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[3]).call()
  console.log(result)

  //------------- Remove all test1 Facet functions ---------------------
  console.log('should remove all test1 functions')
  removeSelectors = getSelectors(Test1Facet).slice(0, -1)
  console.log(removeSelectors)
  await diamondCutFacet.methods
    .diamondCut([[zeroAddress, FacetCutAction.Remove, removeSelectors]], zeroAddress, '0x')
    .send({ from: test_account, gas: 6000000 })
  result = await diamondLoupeFacet.methods.facetFunctionSelectors(addresses[3]).call()
  console.log(result)


  //------------- Run LoupeFacet functions to show facet status -----------------------------------
  console.log('LoupeFacet functions: show facet status')
  result = await diamondLoupeFacet.methods.facets().call()
  console.log(result)

  result = await diamondLoupeFacet.methods.facetAddresses().call()
  console.log(result)
}

DiamondTest()
