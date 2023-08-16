import pytest
from src.ccxtools.okx import Okx
from src.ccxtools.tools import get_env_vars


@pytest.fixture
def config():
    return get_env_vars()


@pytest.fixture
def okx(config):
    return Okx('', 'USDT', config)


def test_get_contract_sizes(okx):
    sizes = okx.get_contract_sizes()
    assert isinstance(sizes, dict)
    assert sizes['BTC'] == 0.01
    assert sizes['ETH'] == 0.1


def test_get_balance(okx):
    # Test input Start
    ticker = 'USDT'
    # Test input End

    balance = okx.get_balance(ticker)


def test_set_leverage(okx):
    ticker = 'BTC'
    leverage = 5
    response = okx.set_leverage(ticker, leverage)
    assert response['data'][0]['instId'][:3] == ticker
    assert int(response['data'][0]['lever']) == leverage
