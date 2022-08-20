from brownie import Setup, Exploit
from brownie import chain, network, accounts, config
from web3 import Web3

LOCAL_ENVS = ['development', 'ganache', 'mainnet-fork']

get_acc = lambda: accounts[0] if (
    network.show_active() in LOCAL_ENVS
) else accounts.add(config['wallets']['from_key'])


def main():
    setup = Setup.deploy(
        {'from': get_acc(), 'value': Web3.toWei(10, 'ether')}
    )
    exploit = Exploit.deploy(
        setup,
        {'from': get_acc(), 'value': Web3.toWei(11.001, 'ether')}
    )
    chain.mine(1)
    print(f'Hacked: {setup.isSolved()}')
    

