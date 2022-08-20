// SPDX-License-Identifier: UNLICENSED

pragma solidity 0.8.16;

interface MasterChefLike {
    function poolInfo(uint256 id) external returns (
        address lpToken,
        uint256 allocPoint,
        uint256 lastRewardBlock,
        uint256 accSushiPerShare
    );

	function poolLength() external view returns (uint256);
}
