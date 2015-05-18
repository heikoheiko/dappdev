import soltester
from ethereum import tester
from ethereum import utils

logc = ':info,eth.vm.exit:trace,eth.pb.msg:debug'
tester.configure_logging(config_string=logc)

spread_contracts = []

depths = [0]

def listener(log):
    print "LISTENER", log
    if log['_event_type'] == 'Created':
        addr = utils.int_to_addr(log['addr'])
        spread_contracts.append(addr.encode('hex'))
    if log['_event_type'] == 'NextCalled':
        depths.append(log['depth'])

s = tester.state()

code = soltester.read_contract(fn='spread.sol')
contract_names = soltester.solc_wrapper.contract_names(code)

creator = s.abi_contract(code, language='solidity', contract_name='Creator', log_listener=listener)
spread_base = s.abi_contract(code, language='solidity', contract_name='Spread', listen=False)

spread_addr = creator.create()
print spread_addr
s.mine()

c = tester.ABIContract(s, spread_base.abi, spread_addr, log_listener=listener)
print
for i in range(10):
    print 'calling start'
    r = c.start()
    print spread_contracts
    for a in spread_contracts:
        print a, len(s.block.get_code(a))
    print 'round', i, len(spread_contracts), s.block.timestamp, max(depths)
    s.mine()
