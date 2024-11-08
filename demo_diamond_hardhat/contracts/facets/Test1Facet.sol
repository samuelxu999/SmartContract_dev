// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Example library to show a simple example of diamond storage

library TestLib {

  bytes32 constant DIAMOND_STORAGE_POSITION = keccak256("diamond.standard.test.storage");
  
  struct TestState {
      address myAddress;
      uint256 myNum;
  }

  function diamondStorage() internal pure returns (TestState storage ds) {
      bytes32 position = DIAMOND_STORAGE_POSITION;
      assembly {
          ds.slot := position
      }
  }

  function setMyAddress(address _myAddress) internal {
    TestState storage testState = diamondStorage();
    testState.myAddress = _myAddress;
  }

  function getMyAddress() internal view returns (address) {
    TestState storage testState = diamondStorage();
    return testState.myAddress;
  }

  function setmyNum(uint256 _myNum) internal {
    TestState storage testState = diamondStorage();
    testState.myNum = _myNum;
  }

  function getmyNum() internal view returns (uint256) {
    TestState storage testState = diamondStorage();
    return testState.myNum;
  }
}

contract Test1Facet {
    event TestEvent(address something);

   function test1Func1() external {
      TestLib.setMyAddress(address(this));
    }

    function test1Func2() external view returns (address){
      return TestLib.getMyAddress();
    }

    function test1Func3(uint256 _myNum) external {
      TestLib.setmyNum(_myNum);
    }

    function test1Func4() external view returns (uint256) {
      return TestLib.getmyNum();
    }

    function test1Func5() external {}

    function test1Func6() external {}

    function test1Func7() external {}

    function test1Func8() external {}

    function test1Func9() external {}

    function test1Func10() external {}

    function test1Func11() external {}

    function test1Func12() external {}

    function test1Func13() external {}

    function test1Func14() external {}

    function test1Func15() external {}

    function test1Func16() external {}

    function test1Func17() external {}

    function test1Func18() external {}

    function test1Func19() external {}

    function test1Func20() external {}

    function supportsInterface(bytes4 _interfaceID) external view returns (bool) {}
}
