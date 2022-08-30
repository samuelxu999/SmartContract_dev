// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title NFT_Tracker
 * This provides a public functions for testing purposes, like data sharing
 */
contract NFT_Tracker is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {
    /*
        Define struct to represent data tracker object.
    */
    struct DataTracker {
        address sender;     // from previous owner
        address receiver;   // to current owner
    }


    // Mapping from token ID to DataTracker (array)
    mapping(uint256 => DataTracker[]) private _dataTracker;

    // event handle function
    event OnDataTracker_Update(uint256 tokenId, uint _value);

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

        // initialize a DataTracker given tokenId
        _dataTracker[tokenId].push( DataTracker(address(0), to) );
        
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
        
        // delete DataTracker given tokenId
        delete _dataTracker[tokenId];
    }

    function burn(uint256 tokenId) public {
        _burn(tokenId);
    }

    function exists(uint256 tokenId) public view returns (bool) {
        return _exists(tokenId);
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
    	require(ownerOf(tokenId) == msg.sender, "NFT_Tracker: setTokenURI from incorrect owner");
    	_setTokenURI(tokenId,_tokenURI);
    }

    // get total tracker given a tokenId
    function total(uint256 tokenId) public view returns (uint256) {
        return _dataTracker[tokenId].length;
    }

    // query DataTracker given token id
    function query_DataTracker(uint256 tokenId, uint256 index) public view returns (address, address) {
        require(index < _dataTracker[tokenId].length, "NFT_Tracker: index out of bounds");

        return(_dataTracker[tokenId][index].sender, 
            _dataTracker[tokenId][index].receiver
            );      
    }

    function transfer(uint256 tokenId, address from, address to) public {
        // call NFT transfer
        super.transferFrom(from, to, tokenId);

        // update tracker
        _dataTracker[tokenId].push( DataTracker(from, to) );

        emit OnDataTracker_Update(tokenId, _dataTracker[tokenId].length);
    }

}