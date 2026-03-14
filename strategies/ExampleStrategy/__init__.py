from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class ExampleStrategy(Strategy):
    @property
    def rsi(self):
        return ta.rsi(self.candles, period=14)

    @property
    def bb(self):
        return ta.bollinger_bands(self.candles, period=20, devup=2, devdn=2)

    def should_long(self) -> bool:
        # Long si el precio toca la banda inferior y RSI esta bajo (Sobreventa)
        return self.price <= self.bb[2] and self.rsi < 35

    def should_short(self) -> bool:
        # Short si el precio toca la banda superior y RSI esta alto (Sobrecompra)
        return self.price >= self.bb[0] and self.rsi > 65

    def should_cancel_entry(self) -> bool:
        return True

    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        # Stop Loss a 10 pips de Oro y Take Profit a 20 pips
        self.stop_loss = qty, self.price - 10
        self.take_profit = qty, self.price + 20

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 10
        self.take_profit = qty, self.price - 20
