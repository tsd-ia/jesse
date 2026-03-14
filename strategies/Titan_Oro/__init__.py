from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Titan_Oro(Strategy):
    @property
    def fast_ema(self):
        return ta.ema(self.candles, period=13)
        
    @property
    def slow_ema(self):
        return ta.ema(self.candles, period=50)

    @property
    def rsi(self):
        return ta.rsi(self.candles, period=14)

    def should_long(self) -> bool:
        # Tendencia alcista + RSI saliendo de sobreventa
        return self.price > self.slow_ema and self.fast_ema > self.slow_ema and self.rsi > 45

    def should_short(self) -> bool:
        # Tendencia bajista + RSI saliendo de sobrecompra
        return self.price < self.slow_ema and self.fast_ema < self.slow_ema and self.rsi < 55

    def go_long(self):
        # 10% del balance por trade, apalancado (Jesse maneja el balance total)
        qty = utils.size_to_qty(self.balance * 0.2, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 15
        self.take_profit = qty, self.price + 45 # Risk Reward 1:3

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.2, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 15
        self.take_profit = qty, self.price - 45

    def should_cancel_entry(self) -> bool:
        return True
