import time
from ethereum._solidity import solc_wrapper
from pyethapp.rpc_client import JSONRPCClient, address_encoder
from ethereum.processblock import mk_contract_address
from ethereum.utils import denoms


RPC_PORT = 4000  # change for Geth
client = JSONRPCClient(port=RPC_PORT, print_communication=False)
sender = client.coinbase
code = open('spread.sol').read()

def create_creator():
    # create Creator contract
    contract_name = 'Creator'
    binary = solc_wrapper.compile(code, contract_name=contract_name)
    abi = solc_wrapper.mk_full_signature(code, 'Spread')
    print abi
    print 'creating Creator contract'
    assert sender
    creator_contract = client.send_transaction(sender, to='', value=0, data=binary, startgas=400000)
    assert len(creator_contract) == 40
    print 'creator contract at', creator_contract
    return creator_contract

def create_spread(creator_contract):
    # will create a Spread contract
    print
    print 'creating spread contract'
    tx = client.send_transaction(sender, to=creator_contract, startgas=300000)
    print 'res', tx
    spread_contract = mk_contract_address(creator_contract.decode('hex'), nonce=0)
    return spread_contract.encode('hex')

def do_spread(spread_contract, creator_contract):
    """
    Improve spend from multiple accounts, so we don't get nonce conflicts
    """
    while True:
        gas = 2400042
        gas = 3000000
        gaslimit = client.gaslimit()
        print "gaslimit", gaslimit
        # print 'gasprice', client.lastgasprice() / denoms.szabo, 'szabo'
        gas = gaslimit - 1024
        for gas in (gas,):
            tx = client.send_transaction(sender, to=spread_contract, startgas=gas, gasprice=10*denoms.szabo)
            print 'spreading fuel:%d / contracts created:%d' % (gas, client.nonce(creator_contract))
        time.sleep(5)


def check_availability(address):
    "checks if there is code at address"  # FIXME, should use listeners
    if not address:
        return False
    assert len(address) == 40
    for i in range(20):
        res = client.call('eth_getCode', address_encoder(address.decode('hex')))
        if len(res[2:]):
            print 'contract available at address', address
            return True
        time.sleep(1)
    print 'contract not available at address', address
    return False

create_creator()
creator_contract= '' #
spread_contract = ''
creator_contract= 'e35e196a53cabeb4eb4cdd66467427a798d8c24f' #
spread_contract = '903b0e300ec230949be02c28af89f9589c82b489'


while not check_availability(creator_contract):
    creator_contract = create_creator()
    time.sleep(20)
while not check_availability(spread_contract):
    spread_contract = create_spread(creator_contract)
    time.sleep(20)

do_spread(spread_contract, creator_contract)
