contract Spread {
    address[16] children;
    address creator_addr;

    event NextCalled(address indexed ataddr, uint indexed depth, uint indexed gas, uint val);

    function Spread(address creator) {
        creator_addr = creator;
    }

    function next(uint v, uint depth) {
        NextCalled(this, depth, msg.gas, v);
        address to;
        uint r = v % 16;
        v = v / 16;

        to = children[r];
        if (to == 0)
        {
            // create contract
            to = Creator(creator_addr).create();
            children[r] = to;
        }

        //Calling(to, depth + 1, msg.gas, v);
        Spread(to).next(v, depth+1);
    }

    function () {
      next(now, 0);
    }

    function start() {
      next(now, 0);
    }


}

contract Creator {

    event Created(address indexed addr, uint indexed gas);

    function create() returns (address to) {
        to = address(new Spread(address(this)));
        Created(to, msg.gas);
        return to;
    }
    function() { create(); }

}
