import ccxt

from ccxtools.base.CcxtFutureExchange import CcxtFutureExchange


class Binance(CcxtFutureExchange):

    def __init__(self, who, market, config):
        super().__init__(market)

        config = {
            'apiKey': config(f'BINANCE_API_KEY{who}'),
            'secret': config(f'BINANCE_SECRET_KEY{who}')
        }

        if market == 'USDT':
            config['options'] = {
                'defaultType': 'future',
                'fetchMarkets': ['linear']
            }
        elif market == 'COIN':
            config['options'] = {
                'defaultType': 'delivery',
                'fetchMarkets': ['inverse']
            }

        self.ccxt_inst = ccxt.binance(config)
        if self.market == 'USDT':
            self.contract_sizes = self.get_contract_sizes()

    def get_mark_price(self, ticker):
        if self.market == 'USDT':
            return float(self.ccxt_inst.fapiPublicGetPremiumIndex({'symbol': f'{ticker}USDT'})['markPrice'])
        if self.market == 'COIN':
            return float(self.ccxt_inst.dapiPublicGetPremiumIndex({'symbol': f'{ticker}USD_PERP'})[0]['markPrice'])

    def get_best_book_price(self, ticker, side):
        if self.market == 'USDT':
            best_book_price_data = self.ccxt_inst.fapiPublicGetDepth({'symbol': f'{ticker}USDT'})[f'{side}s'][0]
            return float(best_book_price_data[0])
        if self.market == 'COIN':
            best_book_price_data = self.ccxt_inst.dapiPublicGetDepth({'symbol': f'{ticker}USD_PERP'})[f'{side}s'][0]
            return float(best_book_price_data[0])

    def get_contract_size(self, ticker):
        if self.market == 'USDT':
            return self.contract_sizes[ticker]
        elif self.market == 'COIN':
            markets = self.ccxt_inst.dapiPublicGetExchangeInfo()['symbols']
            ticker_market = list(filter(lambda x: x['symbol'] == f'{ticker}USD_PERP', markets))[0]
            return float(ticker_market['contractSize'])

    def get_contract_sizes(self):
        """
        :return: {
            'BTC': 0.1,
            'ETH': 0.01,
            ...
        }
        """
        if self.market == 'USDT':
            contracts = self.ccxt_inst.fetch_markets()

            sizes = {}
            for contract in contracts:
                if contract['info']['contractType'] != 'PERPETUAL' or contract['info']['marginAsset'] != 'USDT':
                    continue
                if contract['info']['status'] != 'TRADING':
                    continue

                ticker = contract['base']
                for fil in contract['info']['filters']:
                    if fil['filterType'] == 'LOT_SIZE':
                        size = float(fil['stepSize'])

                sizes[ticker] = size

            return sizes

    def get_max_position_qtys(self):
        """
        :return: {
            'BTC': 20000000,
            'ETH': 5000000,
            ...
        }
        """
        if self.market == 'USDT':
            positions = self.ccxt_inst.fetch_positions()

            qtys = {}
            for position in positions:
                symbol = position['symbol']
                if '/' in symbol and symbol[-4:] == 'USDT':
                    ticker = symbol[:symbol.find('/')]
                    qtys[ticker] = int(position['info']['maxNotionalValue'])

            return qtys

    def get_balance(self, ticker):
        if self.market == 'USDT':
            return super().get_balance(ticker)
        elif self.market == 'COIN':
            return self.ccxt_inst.fetch_balance()['total'][ticker]

    def get_position(self, ticker: str) -> float:
        if self.market == 'USDT':
            return float(
                self.ccxt_inst.fapiprivatev2_get_positionrisk({'symbol': f'{ticker}USDT'})[0]['positionAmt'])
        elif self.market == 'COIN':
            data = list(filter(lambda position: 'PERP' in position['symbol'],
                               self.ccxt_inst.dapiPrivateGetPositionRisk({'pair': f'{ticker}USD'})))[0]
            contract_size = self.get_contract_size(ticker)
            return float(data['positionAmt']) * contract_size

    def post_market_order(self, ticker, side, open_close, amount):
        """
        :param ticker: <String>
        :param side: <Enum: "buy" | "sell">
        :param open_close: <Enum: "open" | "close">
        :param amount: <Float | Int>
        :return: <Float> average filled price
        """
        if self.market == 'USDT':
            if open_close == 'open':
                extra_params = {}
            elif open_close == 'close':
                extra_params = {'reduceOnly': 'true'}

            trade_info = self.ccxt_inst.create_market_order(f'{ticker}USDT', side, amount, params=extra_params)
            return trade_info['average']
        elif self.market == 'COIN':
            trade_info = self.ccxt_inst.create_market_order(f'{ticker}USD_PERP', side, amount // 10)
            return trade_info['average']

    def get_max_trading_qtys(self):
        """
        :return: {
            'BTC': 120,
            'ETH': 2000,
            ...
        """
        qtys = {}
        for contract in self.ccxt_inst.fetch_markets():
            if contract['linear'] and contract['quote'] == 'USDT' and contract['info']['contractType'] == 'PERPETUAL':
                ticker = contract['info']['baseAsset']
                max_qty = list(filter(lambda x: x['filterType'] == 'MARKET_LOT_SIZE', contract['info']['filters']))[0][
                    'maxQty']

                qtys[ticker] = float(max_qty)

        return qtys
