#!/usr/bin/env python
from ethereum import tester
from ethereum._solidity import solc_wrapper
import json
import sys
import re


def strip_imports(code):
    import_statements = re.findall('(import.*?["\'].*?["\'].*?;)', code, re.MULTILINE)
    imports = []
    for s in import_statements:
        imports += re.findall('import ["\'](.*?)["\']', code, re.MULTILINE)
        code = code.replace(s, '')
    return imports, code


def read_contract(fn, paths=[]):
    """
    find and read contract
    """
    if not fn.endswith('.sol'):
        fn += '.sol'
    print 'opening', fn
    return open(fn).read()


def collect_code(name, imported=[], code_by_name={}, paths=[]):
    """
    recursively collects code of a contract
    """
    code = read_contract(name, paths)
    imports, code_wo_imports = strip_imports(code)
    code_by_name[name] = code_wo_imports
    imported.insert(0, name)
    for i_name in reversed(imports):
        # move import to the top
        if i_name in imported:
            imported.insert(0, imported.pop(imported.index(i_name)))
        else:
            collect_code(i_name, imported, code_by_name, paths)
    return '\n'.join(code_by_name[n] for n in imported)


def create_contract(name, state=None):
    state = state or tester.state()
    code = collect_code(name)
    return state.abi_contract(code, language='solidity')


class Contracts(object):

    def __init__(self, state=None, fn=None):
        self.state = state or tester.state()
        if fn:
            self.load(fn)

    def load(self, fn):
        code = read_contract(fn)
        contract_names = solc_wrapper.contract_names(code)
        for name in contract_names:
            c = self.state.abi_contract(code, language='solidity', contract_name=name)
            setattr(self, name, c)


def deploy_contract(fn, contract_name):
    from pyethapp import rpc_client
    code = read_contract(fn)
    binary = solc_wrapper.compile(code, contract_name=contract_name)
    sig = solc_wrapper.mk_full_signature(code, contract_name=contract_name)
    client = rpc_client.JSONRPCClient()
    sender = rpc_client.address_decoder(client.call('eth_coinbase'))
    contract_address = client.eth_sendTransaction(sender=sender, data=binary)
    assert len(contract_address) == 20
    print 'contract created:', contract_address.encode('hex')
    print 'signature:'
    print json.dumps(sig, indent=2)


if __name__ == '__main__':
    #contracts = Contracts(sys.argv[1])
    deploy_contract(sys.argv[1], sys.argv[2])
