var NFT_Data = artifacts.require("./NFT_Data.sol");

module.exports = function(deployer) {
	deployer.deploy(NFT_Data, 'NFT-Data', 'Data');
};
