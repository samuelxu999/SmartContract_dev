var NFT_CapAC = artifacts.require("./NFT_CapAC.sol");
var NFT_Data = artifacts.require("./NFT_Data.sol");
var NFT_Tracker = artifacts.require("./NFT_Tracker.sol");

module.exports = function(deployer) {
	deployer.deploy(NFT_CapAC, 'NFT-CapAC', 'CapAC');
	deployer.deploy(NFT_Data, 'NFT-Data', 'Data');
	deployer.deploy(NFT_Tracker, 'NFT-Tracker', 'Tracker');
};
