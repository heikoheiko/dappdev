from ethereum._solidity import solc_wrapper
from ethereum import tester
import json

code = """
import "owned";

contract TestMan is owned {
    function yeah(uint32 number, uint256 peers, bool really){}
    function yip(bool[2][] newPairs, address recipient) external {}
    function yip2(address recipient){}
}
"""

r = solc_wrapper.combined(code)
print json.dumps(r, indent=2)

state = tester.state()
contract = state.abi_contract(code, language='solidity')
