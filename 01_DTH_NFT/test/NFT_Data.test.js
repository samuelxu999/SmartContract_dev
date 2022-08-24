const { expect } = require('chai');

const { BN, constants, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');

const { ZERO_ADDRESS } = constants;

const NFT_Data = artifacts.require('NFT_Data');

//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('../scripts/addr_list.json');	
	return addrlist[node_name];	
};


contract('NFT_Data', function ([ owner, other ]) {
	const name = 'NFT-Data';
	const symbol = 'Data';

	const firstTokenId = new BN(getAddress('token1')).toString();
	const secondTokenId = new BN(getAddress('token2')).toString();
	const otherTokenId = new BN(getAddress('token3')).toString();
	const nonExistentTokenId = new BN(getAddress('token4')).toString();
	const baseURI = 'https://api.example.com/v1/';
	const newBaseURI = 'https://api.example.com/v2/';
	const tokenURI = 'test_sample';
	const RECEIVER_MAGIC_VALUE = '0x150b7a02';

	beforeEach(async function () {
		this.token = await NFT_Data.new(name, symbol);
	});

	context('with minted NFT_Data', function () {
		beforeEach(async function () {
		  await this.token.mint(owner, firstTokenId);
		});

		context('when the baseURI is default', function () {
			it('return empty string by default baseURI', async function () {
			  expect(await this.token.baseURI()).to.be.equal('');
			});
		});

		context('Set baseURI by owner', function () {
	        it('base URI can be set', async function () {
	          await this.token.setBaseURI(baseURI, { from: owner });
	          expect(await this.token.baseURI()).to.equal(baseURI);
	        });
	        it('base URI is added as a prefix to the token URI', async function () {
	          await this.token.setBaseURI(baseURI, { from: owner });
	          expect(await this.token.tokenURI(firstTokenId)).to.be.equal(baseURI + firstTokenId.toString());
	        });

	        it('token URI can be changed by changing the base URI', async function () {
	          await this.token.setBaseURI(newBaseURI, { from: owner });
	          expect(await this.token.tokenURI(firstTokenId)).to.be.equal(newBaseURI + firstTokenId.toString());
	        });
		});
		context('Set baseURI by other', function () {
			it('reverts', async function () {
				await expectRevert(
					this.token.setBaseURI(baseURI, { from: other }),
					'Ownable: caller is not the owner',
				);
			});
		});

		context('when the tokenURI is default', function () {
			it('return empty string by default tokenURI', async function () {
			  expect(await this.token.tokenURI(firstTokenId)).to.be.equal('');
			});
		});
		context('Set token URI by owner', function () {
	        it('token URI can be set', async function () {
	          await this.token.setTokenURI(firstTokenId, tokenURI, { from: owner });
	          expect(await this.token.tokenURI(firstTokenId)).to.equal(tokenURI);
	        });
	        it('Full token URI: concatenate base URI  and token URI', async function () {
	          await this.token.setBaseURI(baseURI, { from: owner });
	          await this.token.setTokenURI(firstTokenId, tokenURI, { from: owner });
	          expect(await this.token.tokenURI(firstTokenId)).to.be.equal(baseURI + tokenURI);
	        });
		});
		context('Set tokenURI by other', function () {
			it('reverts', async function () {
				await expectRevert(
					this.token.setTokenURI(firstTokenId, tokenURI, { from: other }),
					"NFT_Data: setTokenURI from incorrect owner",
				);
			});
		});
		context('Set baseURI by nonExistentTokenId', function () {
			it('reverts', async function () {
				await expectRevert(
					this.token.setTokenURI(otherTokenId, tokenURI, { from: owner }),
					"ERC721: invalid token ID",
				);
			});
		});
	});

});
