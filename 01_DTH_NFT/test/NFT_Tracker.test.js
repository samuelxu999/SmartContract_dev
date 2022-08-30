const { expect } = require('chai');

const { BN, constants, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');

const { ZERO_ADDRESS } = constants;

const NFT_Tracker = artifacts.require('NFT_Tracker');

//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('../scripts/addr_list.json');	
	return addrlist[node_name];	
};


contract('NFT_Tracker', function ([ owner, other ]) {
	const name = 'NFT-Tracker';
	const symbol = 'Tracker';

	const firstTokenId = new BN(getAddress('token1')).toString();
	const otherTokenId = new BN(getAddress('token2')).toString();
	const tokenURI = 'http://128.226.78.24:8080/';

	beforeEach(async function () {
		this.token = await NFT_Tracker.new(name, symbol);
	});

	context('with minted NFT_Tracker', function () {
		beforeEach(async function () {
		  await this.token.mint(owner, firstTokenId);
		  await this.token.mint(other, otherTokenId);
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
		});
		context('Set tokenURI by other', function () {
			it('reverts', async function () {
				await expectRevert(
					this.token.setTokenURI(firstTokenId, tokenURI, { from: other }),
					"NFT_Tracker: setTokenURI from incorrect owner",
				);
			});
		});

		context('when tracker is default', function () {
			beforeEach(async function () {
				this.tracker0 = await this.token.query_DataTracker(firstTokenId, 0);
				this.tracker_length = await this.token.total(firstTokenId);
			});
			it('return 0 address by sender', async function () {
			  	expect(this.tracker0[0]).to.be.equal(ZERO_ADDRESS);
			});
			it('return owner address by receiver', async function () {
			  	expect(this.tracker0[1]).to.be.equal(owner);
			});
			it('return length of tracker', async function () {
			  	expect(this.tracker_length).to.be.equal(1);
			});
		});

		describe('NFT_Tracker transfer by owner', function () {
			beforeEach(async function () {
				await this.token.transfer(firstTokenId, owner, other, { from: owner });
				this.tracker_length = await this.token.total(firstTokenId);
				this.tracker = await this.token.query_DataTracker(firstTokenId, this.tracker_length-1);
			});
			it('return owner address by sender', async function () {
			  	expect(this.tracker[0]).to.be.equal(owner);
			});
			it('return other address by receiver', async function () {
			  	expect(this.tracker[1]).to.be.equal(other);
			});
			it('return length of tracker', async function () {
			  	expect(this.tracker_length).to.be.equal(2);
			});
		});

		describe('NFT_Tracker transfer by other', function () {
			it('reverts', async function () {
				await expectRevert(
				  this.token.transfer(otherTokenId, owner, other, { from: other }),
				  "ERC721: transfer from incorrect owner",
				);
			});
			it('return length of tracker', async function () {
				this.tracker_length = await this.token.total(otherTokenId);
			  	expect(this.tracker_length).to.be.equal(1);
			});
		});

		context('burn token', function () {
			beforeEach(async function () {
				await this.token.burn(firstTokenId);
				await this.token.burn(otherTokenId);
			});
			it('return length of tracker for token1', async function () {
				this.tracker_length = await this.token.total(firstTokenId);
			  	expect(this.tracker_length).to.be.equal(0);
			});
			it('return length of tracker for token2', async function () {
				this.tracker_length = await this.token.total(otherTokenId);
			  	expect(this.tracker_length).to.be.equal(0);
			});
		});

	});

	context('with empty NFT_Tracker', function () {
		context('length of tracker is 0', function () {
			it('return length of tracker', async function () {
				this.tracker_length = await this.token.total(firstTokenId);
			  	expect(this.tracker_length).to.be.equal(0);
			});
		});

	});

});

		// describe('setDataAC', function () {
		//   context('when the given address owns DataAC', function () {
	 //          it('verify ref_address and data_mac', async function () {
	 //          	await this.token.setDataAC(firstTokenId, ref_address, data_mac, { from: owner });
	 //          	this.data_ac = await this.token.query_DataAC(firstTokenId);
	 //          	expect(this.data_ac[1]).to.be.bignumber.equal(ref_address);
	 //          	expect(this.data_ac[2]).to.be.bignumber.equal(data_mac);
	 //          });
		//   });
		//   context('when the given address does not own DataAC', function () {
	 //          it('reverts', async function () {
	 //            await expectRevert(
	 //              this.token.setDataAC(firstTokenId, ref_address, data_mac, { from: other }),
	 //              "NFT_Tracker: setDataAC from incorrect owner",
	 //            );
	 //          });
		//   });
		// });
