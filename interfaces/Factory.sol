
// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

interface FactoryInterface {
	function getPair(address tokenA, address tokenB) external view returns (address pair);
}
