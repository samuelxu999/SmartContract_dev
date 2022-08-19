const { expect } = require('chai');

const { BN, constants, expectEvent, expectRevert } = require('@openzeppelin/test-helpers');

const { ZERO_ADDRESS } = constants;

const NFT_AC = artifacts.require('NFT_AC');

contract('NFT_AC', function ([ owner, other ]) {
	const name = 'Non Fungible Token';
	const symbol = 'NFT';

	const firstTokenId = new BN('5042');
	const secondTokenId = new BN('79217');
	const nonExistentTokenId = new BN('13');
	const fourthTokenId = new BN(4);
	const baseURI = 'https://api.example.com/v1/';

	const RECEIVER_MAGIC_VALUE = '0x150b7a02';

	beforeEach(async function () {
		this.token = await NFT_AC.new(name, symbol);
	});

	context('with minted tokens', function () {
		beforeEach(async function () {
		  await this.token.mint(owner, firstTokenId);
		  await this.token.mint(owner, secondTokenId);
		  this.toWhom = other; // default to other for toWhom in context-dependent tests
		});

		describe('balanceOf', function () {
		  context('when the given address owns some tokens', function () {
		    it('returns the amount of tokens owned by the given address', async function () {
		      expect(await this.token.balanceOf(owner)).to.be.bignumber.equal('2');
		    });
		  });

		  context('when the given address does not own any tokens', function () {
		    it('returns 0', async function () {
		      expect(await this.token.balanceOf(other)).to.be.bignumber.equal('0');
		    });
		  });

		  context('when querying the zero address', function () {
		    it('throws', async function () {
		      await expectRevert(
		        this.token.balanceOf(ZERO_ADDRESS), 'ERC721: address zero is not a valid owner',
		      );
		    });
		  });
		});
	});
});
