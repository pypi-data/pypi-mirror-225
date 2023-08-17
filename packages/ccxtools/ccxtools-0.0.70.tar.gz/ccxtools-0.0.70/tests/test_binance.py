import pytest
import math
from src.ccxtools.tools import get_env_vars
from src.ccxtools.binance import Binance


@pytest.fixture
def config():
    return get_env_vars()


@pytest.fixture
def binance_usdt(config):
    return Binance('', 'USDT', config)


@pytest.fixture
def binance_coin(config):
    return Binance('', 'COIN', config)


def test_get_mark_price(binance_usdt, binance_coin):
    assert isinstance(binance_usdt.get_mark_price('BTC'), float)
    assert isinstance(binance_coin.get_mark_price('BTC'), float)


def test_get_best_book_price(binance_usdt, binance_coin):
    assert isinstance(binance_usdt.get_best_book_price('BTC', 'ask'), float)
    assert isinstance(binance_usdt.get_best_book_price('BTC', 'bid'), float)
    assert isinstance(binance_coin.get_best_book_price('BTC', 'ask'), float)
    assert isinstance(binance_coin.get_best_book_price('BTC', 'bid'), float)


def test_get_contract_size(binance_usdt, binance_coin):
    assert binance_usdt.get_contract_size('BTC') == 0.001
    assert binance_coin.get_contract_size('BTC') == 100
    assert binance_coin.get_contract_size('XRP') == 10


def test_get_contract_sizes(binance_usdt):
    sizes = binance_usdt.get_contract_sizes()
    assert isinstance(sizes, dict)
    assert sizes['BTC'] == 0.001
    assert sizes['ETH'] == 0.001


def test_get_max_position_qtys(binance_usdt):
    qtys = binance_usdt.get_max_position_qtys()
    assert 'BTC' in qtys
    assert isinstance(qtys['BTC'], int)
    assert 'ETH' in qtys
    assert isinstance(qtys['ETH'], int)


def test_get_balance(binance_usdt, binance_coin):
    # Test input Start
    usdt_ticker = 'USDT'
    usdt_balance_input = 10459

    coin_ticker = 'XRP'
    coin_balance_input = 22400
    # Test input End

    usdt_balance = binance_usdt.get_balance(usdt_ticker)
    assert usdt_balance_input * 0.9 <= usdt_balance <= usdt_balance_input * 1.1

    coin_balance = binance_coin.get_balance(coin_ticker)
    assert isinstance(coin_balance, float)
    assert coin_balance_input * 0.9 <= coin_balance <= coin_balance_input * 1.1


def test_get_position(binance_usdt, binance_coin):
    # Test input Start
    usdt_ticker = 'LPT'
    usdt_amount = 0

    coin_ticker = 'XRP'
    coin_amount = 1000
    # Test input End
    position = binance_usdt.get_position(usdt_ticker)
    assert isinstance(position, float)
    if usdt_amount:
        assert math.isclose(position, usdt_amount)

    position = binance_coin.get_position(coin_ticker)
    assert isinstance(position, float)
    if coin_amount:
        assert math.isclose(position, coin_amount)


def test_post_market_order(binance_usdt, binance_coin):
    # Test input Start
    ticker = 'XRP'
    usdt_amount = 20
    coin_amount = 10
    # Test input End

    last_price = binance_usdt.ccxt_inst.fetch_ticker(f'{ticker}USDT')['last']

    buy_open_price = binance_usdt.post_market_order(ticker, 'buy', 'open', usdt_amount)
    assert 0.9 * last_price < buy_open_price < 1.1 * last_price
    sell_close_price = binance_usdt.post_market_order(ticker, 'sell', 'close', usdt_amount)
    assert 0.9 * last_price < sell_close_price < 1.1 * last_price
    sell_open_price = binance_usdt.post_market_order(ticker, 'sell', 'open', usdt_amount)
    assert 0.9 * last_price < sell_open_price < 1.1 * last_price
    buy_close_price = binance_usdt.post_market_order(ticker, 'buy', 'close', usdt_amount)
    assert 0.9 * last_price < buy_close_price < 1.1 * last_price

    last_price = binance_coin.ccxt_inst.fetch_ticker(f'{ticker}USD_PERP')['last']

    buy_open_price = binance_coin.post_market_order(ticker, 'buy', 'open', coin_amount)
    assert 0.9 * last_price < buy_open_price < 1.1 * last_price
    sell_close_price = binance_coin.post_market_order(ticker, 'sell', 'close', coin_amount)
    assert 0.9 * last_price < sell_close_price < 1.1 * last_price
    sell_open_price = binance_coin.post_market_order(ticker, 'sell', 'open', coin_amount)
    assert 0.9 * last_price < sell_open_price < 1.1 * last_price
    buy_close_price = binance_coin.post_market_order(ticker, 'buy', 'close', coin_amount)
    assert 0.9 * last_price < buy_close_price < 1.1 * last_price


def test_get_precise_order_amount(binance_usdt):
    ticker = 'BTC'
    ticker_amount = 0.00111
    assert binance_usdt.get_precise_order_amount(ticker, ticker_amount) == 0.001


def test_get_max_trading_qtys(binance_usdt):
    max_qtys = binance_usdt.get_max_trading_qtys()
    assert isinstance(max_qtys, dict)
    assert 'BTC' in max_qtys
    assert max_qtys['BTC'] == 120
