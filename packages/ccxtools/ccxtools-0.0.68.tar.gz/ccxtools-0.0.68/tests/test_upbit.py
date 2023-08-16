import pytest

from src.ccxtools.tools import get_env_vars
from src.ccxtools.upbit import Upbit


@pytest.fixture
def config():
    return get_env_vars()


@pytest.fixture
def upbit(config):
    return Upbit('', '', config)


def test_get_last_price(upbit):
    price = upbit.get_last_price('BTC')
    assert isinstance(price, float)


def test_get_best_book_price(upbit):
    assert isinstance(upbit.get_best_book_price('BTC', 'ask'), float)
    assert isinstance(upbit.get_best_book_price('BTC', 'bid'), float)


def test_post_market_order(upbit):
    # Test input Start
    ticker = 'XRP'
    amount = 10
    # Test input End

    last_price = upbit.get_last_price(ticker)

    buy_price = upbit.post_market_order(ticker, 'buy', amount, last_price)
    assert 0.9 * last_price < buy_price < 1.1 * last_price
    sell_price = upbit.post_market_order(ticker, 'sell', amount, last_price)
    assert 0.9 * last_price < sell_price < 1.1 * last_price
