# from https://github.com/ethereum/cpp-ethereum/blob/develop/libsolidity/CompilerStack.cpp#L43
# writes base contracts to dir
#

base_contracts = [
    {"coin", '''import "CoinReg";
    import "Config";
    import "configUser";
    contract coin is configUser{function coin(bytes3 name, uint denom) {CoinReg(Config(configAddr()).lookup(3)).register(name, denom);
    }}'''},
    {"Coin",
        '''contract Coin{function isApprovedFor(address _target,address _proxy)constant returns(bool _r){}function isApproved(address _proxy)constant returns(bool _r){}function sendCoinFrom(address _from,uint256 _val,address _to){}function coinBalanceOf(address _a)constant returns(uint256 _r){}function sendCoin(uint256 _val,address _to){}function coinBalance()constant returns(uint256 _r){}function approve(address _a){}}'''},
    {"CoinReg",
        '''contract CoinReg{function count()constant returns(uint256 r){}function info(uint256 i)constant returns(address addr,bytes3 name,uint256 denom){}function register(bytes3 name,uint256 denom){}function unregister(){}}'''},
    {"configUser",
        '''contract configUser{function configAddr()constant returns(address a){ return 0xc6d9d2cd449a754c494264e1809c50e34d64562b
;
}}'''},
    {"Config",
        '''contract Config{function lookup(uint256 service)constant returns(address a){}function kill(){}function unregister(uint256 id){}function register(uint256 id,address service){}}'''},
    {"mortal", '''import "owned";
    contract mortal is owned {function kill() { if (msg.sender == owner) suicide(owner);
     }}'''},
    {"named", '''import "Config";
    import "NameReg";
    import "configUser";
    contract named is configUser {function named(bytes32 name) {NameReg(Config(configAddr()).lookup(1)).register(name);
    }}'''},
    {"NameReg",
        '''contract NameReg{function register(bytes32 name){}function addressOf(bytes32 name)constant returns(address addr){}function unregister(){}function nameOf(address addr)constant returns(bytes32 name){}}'''},
    {"owned",
        '''contract owned{function owned(){owner = msg.sender
;
}modifier onlyowner(){if(msg.sender==owner)_}address owner
;
}'''},
    {"service", '''import "Config";
    import "configUser";
    contract service is configUser{function service(uint _n){Config(configAddr()).register(_n, this);
    }}'''},
    {"std", '''import "owned";
    import "mortal";
    import "Config";
    import "configUser";
    import "NameReg";
    import "named";
    '''}

]


for name, code in base_contracts:
    if ' ' in name:
        code, name = name, code
    print name
    open(name + '.sol', 'w').write(code)
