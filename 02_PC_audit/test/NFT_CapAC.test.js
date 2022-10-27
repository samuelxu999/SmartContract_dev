const { expect } = require('chai');

const { BN, constants, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');

const { ZERO_ADDRESS } = constants;

const NFT_CapAC = artifacts.require('NFT_CapAC');

//get address from json file
function getAddress(node_name){
	// Load config data from SmartToken.json
	var addrlist = require('../scripts/addr_list.json');	
	return addrlist[node_name];	
};


contract('NFT_CapAC', function ([ owner, other ]) {
	const name = 'NFT-CapAC';
	const symbol = 'CapAC';

	const firstTokenId = new BN(getAddress('token1')).toString();
	const secondTokenId = new BN(getAddress('token2')).toString();
	const otherTokenId = new BN(getAddress('token3')).toString();
	const nonExistentTokenId = new BN(getAddress('token4')).toString();
	const baseURI = 'https://api.example.com/v1/';

	const RECEIVER_MAGIC_VALUE = '0x150b7a02';

	beforeEach(async function () {
		this.token = await NFT_CapAC.new(name, symbol);
	});

	context('with minted CapAC', function () {
		beforeEach(async function () {
		  await this.token.mint(owner, firstTokenId);
		  this.cap_ac = await this.token.query_CapAC(firstTokenId)
		});

		describe('mintCapAC', function () {
		  context('when the given token owns CapAC', function () {
		    it('returns the id', async function () {
		      expect(this.cap_ac[0]).to.be.bignumber.equal('1');
		    });
		    it('returns the issuedate', async function () {
		      expect(this.cap_ac[1]).to.be.bignumber.equal('0');
		    });
		    it('returns the expireddate', async function () {
		      expect(this.cap_ac[2]).to.be.bignumber.equal('0');
		    });
		    it('returns the authorization', async function () {
		      expect(this.cap_ac[3]).to.be.equal('NULL');
		    });
		  });
		});
	});

	context('with empty CapAC', function () {
		beforeEach(async function () {
		  this.cap_ac = await this.token.query_CapAC(firstTokenId)
		});

		context('when the given token without CapAC', function () {
			it('returns the id', async function () {
			  expect(this.cap_ac[0]).to.be.bignumber.equal('0');
			});
			it('returns the issuedate', async function () {
			  expect(this.cap_ac[1]).to.be.bignumber.equal('0');
			});
			it('returns the expireddate', async function () {
			  expect(this.cap_ac[2]).to.be.bignumber.equal('0');
			});
			it('returns the authorization', async function () {
			  expect(this.cap_ac[3]).to.be.equal('');
			});
		});
	});

	context('update CapAC', function () {
		beforeEach(async function () {
		  await this.token.mint(owner, firstTokenId);
		});

		describe('setCapAC_expireddate', function () {
		  context('when the given address owns CapAC', function () {
	          it('verify issuedate and expireddate', async function () {
	          	await this.token.setCapAC_expireddate(firstTokenId, 12345, 67890, { from: owner });
	          	this.cap_ac = await this.token.query_CapAC(firstTokenId);
	          	expect(this.cap_ac[1]).to.be.bignumber.equal('12345');
	          	expect(this.cap_ac[2]).to.be.bignumber.equal('67890');
	          });
		  });
		  context('when the given address does not own CapAC', function () {
	          it('reverts', async function () {
	            await expectRevert(
	              this.token.setCapAC_expireddate(firstTokenId, 12345, 67890, { from: other }),
	              'NFT_CapAC: setCapAC_expireddate from incorrect owner',
	            );
	          });
		  });
		});

		describe('setCapAC_authorization', function () {
		  context('when the given address owns CapAC', function () {
	          it('verify authorization', async function () {
	          	await this.token.setCapAC_authorization(firstTokenId, 'Assign access rights', { from: owner });
	          	this.cap_ac = await this.token.query_CapAC(firstTokenId);
	          	expect(this.cap_ac[3]).to.be.equal('Assign access rights');
	          });
		  });
		  context('when the given address does not own CapAC', function () {
	          it('reverts', async function () {
	            await expectRevert(
	              this.token.setCapAC_authorization(firstTokenId, 'Assign access rights', { from: other }),
	              'NFT_CapAC: setCapAC_authorization from incorrect owner',
	            );
	          });
		  });
		});
	});
});
