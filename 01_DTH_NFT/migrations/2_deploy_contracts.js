var NFT_CapAC = artifacts.require("./NFT_CapAC.sol");
var NFT_Data = artifacts.require("./NFT_Data.sol");

module.exports = function(deployer) {
	deployer.deploy(NFT_CapAC, 'NFT-CapAC', 'CapAC');
	deployer.deploy(NFT_Data, 'NFT-Data', 'Data');
};
