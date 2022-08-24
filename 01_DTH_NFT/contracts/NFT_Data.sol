// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title NFT_Data
 * This provides a public functions for testing purposes
 */
contract NFT_Data is ERC721, ERC721Enumerable, ERC721URIStorage, Ownable {

	string private _base_URI = "";

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
    }

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
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


    // function query_CapAC(uint256 tokenId) public view returns (uint, 
    //                                                     uint256, 
    //                                                     uint256, 
    //                                                     string memory) {
    //     // return(id, issuedate, expireddate, authorization);  
    //     return(_capAC[tokenId].id, 
    //         _capAC[tokenId].issuedate,
    //         _capAC[tokenId].expireddate,
    //         _capAC[tokenId].authorization
    //         );      
    // }

    // function _mintCapAC(uint256 tokenId) private {
    //     _capAC[tokenId].id = 1;
    //     _capAC[tokenId].issuedate = 0;
    //     _capAC[tokenId].expireddate = 0;
    //     _capAC[tokenId].authorization = 'NULL';
    // }

    // function _burnCapAC(uint256 tokenId) private {
    //     delete _capAC[tokenId];
    // }

    // // Set time limitation for a CapAC
    // function setCapAC_expireddate(uint256 tokenId, 
    //                                 uint256 issueddate, 
    //                                 uint256 expireddate) public {
    //     require(ownerOf(tokenId) == msg.sender, "NFT_CapAC: setCapAC_expireddate from incorrect owner");

    //     _capAC[tokenId].id += 1;
    //     _capAC[tokenId].issuedate = issueddate;
    //     _capAC[tokenId].expireddate = expireddate;

    //     emit OnCapAC_Update(tokenId, _capAC[tokenId].id);

    // }

    // // Assign access rights to a CapAC
    // function setCapAC_authorization(uint256 tokenId, 
    //                                     string memory accessright) public {
    //     require(ownerOf(tokenId) == msg.sender, "NFT_CapAC: setCapAC_authorization from incorrect owner");

    //     _capAC[tokenId].id += 1;
    //     _capAC[tokenId].authorization = accessright;

    //     emit OnCapAC_Update(tokenId, _capAC[tokenId].id);
   
    // }
}