// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract TestERC20 is ERC20 {
	constructor(uint256 initialSupply) ERC20("TestERC20", "TEST") {
		_mint(msg.sender, initialSupply);
	}
}
