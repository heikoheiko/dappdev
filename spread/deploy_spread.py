import time
from ethereum._solidity import solc_wrapper
from pyethapp.rpc_client import JSONRPCClient, address_encoder
from pyethapp.accounts import mk_privkey
from ethereum.processblock import mk_contract_address

secret = 'YOUR_SECRET_TO_AN_ACCOUNT'
PRIVKEY = mk_privkey(secret)  # your privkey here

client = JSONRPCClient(privkey=PRIVKEY, print_communication=False)
code = open('spread.sol').read()

def create_creator():
    # create Creator contract
    contract_name = 'Creator'
    binary = solc_wrapper.compile(code, contract_name=contract_name)
    print 'creating Creator contract'
    creator_contract = client.send_transaction(to='', value=0, data=binary, startgas=400000)
    assert len(creator_contract) == 40
    print 'creator contract at', creator_contract
    return creator_contract

def create_spread(creator_contract):
    # will create a Spread contract
    print
    print 'creating spread contract'
    tx = client.send_transaction(to=creator_contract, startgas=300000)
    print 'res', tx
    spread_contract = mk_contract_address(creator_contract.decode('hex'), nonce=0)
    return spread_contract.encode('hex')

def do_spread(spread_contract, creator_contract):
    while True:
        for i in range(1, 4):
            # call spread contract start
            gas = 3000000/i
            for j in range(i):
                tx = client.send_transaction(to=spread_contract, startgas=gas)
                print 'spreading, created:', client.nonce(creator_contract), gas
            time.sleep(3)

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


creator_contract = ''
spread_contract = ''

while not check_availability(creator_contract):
    creator_contract = create_creator()
    time.sleep(20)
while not check_availability(spread_contract):
    spread_contract = create_spread(creator_contract)
    time.sleep(20)

do_spread(spread_contract, creator_contract)
