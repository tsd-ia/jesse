from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class HyperScalp(Strategy):
    def should_long(self) -> bool:
        # Cruce rapido de EMAs + RSI bajisimo (sobreventa extrema en M15)
        ema_fast = ta.ema(self.candles, period=9)
        ema_slow = ta.ema(self.candles, period=21)
        rsi = ta.rsi(self.candles, period=7)
        
        return self.price > ema_fast and ema_fast > ema_slow and rsi < 30

    def should_short(self) -> bool:
        ema_fast = ta.ema(self.candles, period=9)
        ema_slow = ta.ema(self.candles, period=21)
        rsi = ta.rsi(self.candles, period=7)
        
        return self.price < ema_fast and ema_fast < ema_slow and rsi > 70

    def go_long(self):
        # Apalancamiento agresivo para buscar el 200%
        qty = utils.size_to_qty(self.balance * 5, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        # SL muy ajustado (seguridad) y TP rapido
        self.stop_loss = qty, self.price - 2
        self.take_profit = qty, self.price + 6

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 5, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 2
        self.take_profit = qty, self.price - 6

    def should_cancel_entry(self) -> bool:
        return True
