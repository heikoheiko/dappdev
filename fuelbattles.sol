import "owned";

contract Simulator {

    event Started(address indexed a);

    function start(address a_ai, address b_ai) {
        Started(a_ai);
        Started(b_ai);
    }

}

contract AI is owned {

    event Moved(uint8 indexed number);

    function move(uint8 number) {
        Moved(number);
    }

    function neighbours() returns (uint8 z) {
        return 18;
    }
}


contract Stdlib {


    function uint8_min(uint8[] array) external returns (uint8 min){
        // access to a non-existing index will stop execution
        min = array[0];
        uint256 i = 0;
        for (i=1; i<array.length; i++){
            if (array[i] < min) {
                min = array[i];
            }
        }
        return min;
    }

    function echo(uint8 number) external returns (uint8 z){
        z = number;
        return number;
    }
/*
    function echo2(uint8[] numbers) external returns (uint8[] z){
        z = numbers;
        return z;
    }
*/
}

contract Counter {

    uint8 count;

    event Incremented(uint8 inc, uint8 total);
    event OverFlow();

    function increment(uint8 inc) public returns (uint8 z) {
        if (count == 255) {
            OverFlow();
        }
        count += inc;
        Incremented(inc, count);
        return count;
    }
}



contract ArrayContract {
  uint[2**20] m_aLotOfIntegers;
  bool[2][] m_pairsOfFlags;
  function setAllFlagPairs(bool[2][] newPairs) external {
    // assignment to array replaces the complete array
    m_pairsOfFlags = newPairs;
  }
  function setFlagPair(uint index, bool flagA, bool flagB) {
    // access to a non-existing index will stop execution
    m_pairsOfFlags[index][0] = flagA;
    m_pairsOfFlags[index][1] = flagB;
  }
  function changeFlagArraySize(uint newSize) {
    // if the new size is smaller, removed array elements will be cleared
    m_pairsOfFlags.length = newSize;
  }
  function clear() {
    // these clear the arrays completely
    delete m_pairsOfFlags;
    delete m_aLotOfIntegers;
    // identical effect here
    m_pairsOfFlags.length = 0;
  }

}
