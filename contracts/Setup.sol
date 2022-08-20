// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

import "./MasterChefHelper.sol";

interface WETH9 is ERC20Like {
    function deposit() external payable;
}

contract Setup {
   	
	// NOTE that it could be any other token, not only WETH9
    WETH9 public immutable weth;
    MasterChefHelper public immutable mcHelper;

    constructor(address wethAddr) payable {
		weth = WETH9(wethAddr);	
        mcHelper = new MasterChefHelper();
        weth.deposit{value: 10 ether}();
        weth.transfer(address(mcHelper), 10 ether); // whoops
    }
	
    function isSolved() external view returns (bool) {
        return weth.balanceOf(address(mcHelper)) == 0;
    }

}
