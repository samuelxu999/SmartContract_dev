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
	const ref_address = '0x9374E09e81d54c190Cd94266EaaD0F2A2b060AF6';
	const data_mac = '0x438d538a30e577832db65a1de046906f0f3e448308cf0834ac153c8dee728293';

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

		describe('setDataAC', function () {
		  context('when the given address owns DataAC', function () {
	          it('verify ref_address and data_mac', async function () {
	          	await this.token.setDataAC(firstTokenId, ref_address, data_mac, { from: owner });
	          	this.data_ac = await this.token.query_DataAC(firstTokenId);
	          	expect(this.data_ac[1]).to.be.bignumber.equal(ref_address);
	          	expect(this.data_ac[2]).to.be.bignumber.equal(data_mac);
	          });
		  });
		  context('when the given address does not own DataAC', function () {
	          it('reverts', async function () {
	            await expectRevert(
	              this.token.setDataAC(firstTokenId, ref_address, data_mac, { from: other }),
	              "NFT_DataAC: setDataAC from incorrect owner",
	            );
	          });
		  });
		});

		describe('setDataAC_authorization', function () {
		  context('when the given address owns DataAC', function () {
	          it('verify authorization', async function () {
	          	await this.token.setDataAC_authorization(firstTokenId, 'Assign access rights', { from: owner });
	          	this.data_ac = await this.token.query_DataAC(firstTokenId);
	          	expect(this.data_ac[3]).to.be.equal('Assign access rights');
	          });
		  });
		  context('when the given address does not own DataAC', function () {
	          it('reverts', async function () {
	            await expectRevert(
	              this.token.setDataAC_authorization(firstTokenId, 'Assign access rights', { from: other }),
	              'NFT_DataAC: setDataAC_authorization from incorrect owner',
	            );
	          });
		  });
		});
	});

});
