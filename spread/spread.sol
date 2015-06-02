contract Spread {
    address[3] children;
    address creator_addr;

    event NextCalled(address indexed ataddr, uint indexed depth, uint indexed gas, uint val);
    event Calling(address indexed addr, uint indexed depth, uint indexed gas);


    function Spread(address creator) {
        creator_addr = creator;
    }

    function next(uint v, uint depth, address root) {
        NextCalled(this, depth, msg.gas, v);
        address to;
        uint r = v % 3;
        v = v / 3;

        to = children[r];
        if (to == 0 && msg.gas > 500000)
        {
            // create contract
            to = Creator(creator_addr).create();
            children[r] = to;
        }
        if (to == 0)
            to = root;
        if (msg.gas > 30000)
        {
            //Calling(to, depth, msg.gas);
            Spread(to).next(v, depth+1, root);
        } else
        {
            while (msg.gas > 1000)
                v = v+1;
        }

    }

    function () {
      start();
    }

    function start() {
      next(now, 0, address(this));
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
