from brownie import Setup, Exploit
from brownie import network, accounts, config
from web3 import Web3

LOCAL_ENVS = ['development', 'ganache', 'mainnet-fork']

get_acc = lambda: accounts[0] if (
    network.show_active() in LOCAL_ENVS
) else accounts.add(config['wallets']['from_key'])


def main():
    setup = Setup.at(
        '0x0db3D3d4FbD9D6307BA17dAfe41A44aB22f8c37A'
    )
    exploit = Exploit.deploy(
        setup,
        {'from': get_acc(), 'value': Web3.toWei(11.001, 'ether')}
    )
    print(f'Hacked: {setup.isSolved()}')
    

