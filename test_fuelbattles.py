import sys
if __name__ != '__main__':
    sys.path = [x for x in sys.path if not ('ethereum' in x and x.endswith('.egg'))]
    print __name__
import pytest
from ethereum import tester
from soltester import Contracts
import logging
logging.NOTSET = logging.INFO

mem = [None]


@pytest.fixture
def contracts():
    if not mem[0]:
        fn = 'fuelbattles.sol'
        print 'loading', fn
        mem[0] = Contracts(fn=fn)
    return mem[0]


def test_simulator(contracts):
    contracts.Simulator.start(tester.a1, tester.a2)


def test_ai(contracts):
    contracts.AI.move(12)
    assert 18 == contracts.AI.neighbours()


def test_echo(contracts):
    r = contracts.Stdlib.echo(2)
    print 'echoed', r
    assert r == 2


def test_echo2(contracts):
    a = [2, 6, 2**32]
    r = contracts.Stdlib.echo2(a)
    assert r == a


def test_counter(contracts):
    for i in range(260):
        r = contracts.Counter.increment(1)
        assert (i + 1) % 256 == r, (r, i + 1)


def test_min(contracts):
    r = contracts.Stdlib.uint8_min([9, 5, 6, 4, 1])
    print 'min is', r
    assert r == 1

# def test_setAllFlagPairs():
#     contracts = get_contracts()
#     contracts.ArrayContract.setAllFlagPairs([True, False] * 5)

if __name__ == '__main__':
    logging.NOTSET = logging.TRACE
    contracts = contracts()
    test_counter(contracts)
    # test_simulator(contracts)
    # test_ai(contracts)
    # test_echo2(contracts)
    # test_min(contracts)
