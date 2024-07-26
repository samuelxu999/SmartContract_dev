// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title NFT_Data
 * This provides a public functions for testing purposes, like data sharing
 */
contract NFT_Data is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
	// save base URI for contract
	string private _base_URI = "";

    /*
        Define struct to represent data object.
    */
    struct DataAC {
        uint id;                // incremental id
        string mkt_root;   	    // reference address (hash string) of data
        string[] data_mac;   	// authentor for data integrity
        uint total_mac;         // count total number of data_mac
    }

    // Mapping from token ID to DataAC
    mapping(uint256 => DataAC) private _dataAC;

    // event handle function
    event OnDataAC_Update(uint256 tokenId, uint _value);

    constructor(string memory name, string memory symbol) ERC721(name, symbol) {}

    // The following functions are overrides required by Solidity.

    function _beforeTokenTransfer(address from, address to, uint256 tokenId)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }

    function mint(address to, uint256 tokenId) public {
        _mint(to, tokenId);

        // mint a TokenURI given tokenId
        _setTokenURI(tokenId,'');

        // mint a DataAC given tokenId
        _mintDataAC(tokenId);
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
        
        // mint a DataAC given tokenId
        _burnDataAC(tokenId);
    }

    function burn(uint256 tokenId) public {
        _burn(tokenId);
    }

    function exists(uint256 tokenId) public view returns (bool) {
        return _exists(tokenId);
    }

    function _baseURI() internal view override(ERC721) returns (string memory) 
    {
        return _base_URI;
    }

    function baseURI() public view returns (string memory) {
        return _baseURI();
    }

    function setBaseURI(string memory str_baseURI) public onlyOwner {
        _base_URI = str_baseURI;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    // override virtual functions in ERC721URIStorage
    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal override(ERC721URIStorage) {
        super._setTokenURI(tokenId, _tokenURI);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
    	require(ownerOf(tokenId) == msg.sender, "NFT_Data: setTokenURI from incorrect owner");
    	_setTokenURI(tokenId,_tokenURI);
    }

    // DataAC functions
    function query_DataAC(uint256 tokenId) public view returns (uint, 
                                                        string memory, 
                                                        string[] memory,
                                                        uint) {
        return(_dataAC[tokenId].id, 
            _dataAC[tokenId].mkt_root,
            _dataAC[tokenId].data_mac,
            _dataAC[tokenId].total_mac
            );      
    }

    function _mintDataAC(uint256 tokenId) private {
        _dataAC[tokenId].id = 1;
        _dataAC[tokenId].mkt_root = '0x00';
        _dataAC[tokenId].total_mac = 0;
    }

    function _burnDataAC(uint256 tokenId) private {
        delete _dataAC[tokenId];
    }

    // Set data information for a DataAC
    function setDataAC(uint256 tokenId, 
                                    string memory mkt_root, 
                                    string[] memory data_mac) public {
        require(ownerOf(tokenId) == msg.sender, "NFT_DataAC: setDataAC from incorrect owner");

        _dataAC[tokenId].id += 1;
        _dataAC[tokenId].mkt_root = mkt_root;

        // reset total_mac and data_mac
        if(_dataAC[tokenId].total_mac!=0){
            delete _dataAC[tokenId].data_mac;
            _dataAC[tokenId].total_mac=0;
        }

        // for each item to add data_mac
        for(uint i =0; i<data_mac.length; i++){
            _dataAC[tokenId].data_mac.push(data_mac[i]);
            _dataAC[tokenId].total_mac+=1;
        }

        emit OnDataAC_Update(tokenId, _dataAC[tokenId].id);

    }

}