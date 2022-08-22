var NFT_CapAC = artifacts.require("./NFT_CapAC.sol");

module.exports = function(deployer) {
	deployer.deploy(NFT_CapAC, 'NFT-CapAC', 'CapAC');
};
