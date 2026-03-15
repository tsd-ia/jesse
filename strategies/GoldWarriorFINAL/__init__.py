from jesse.strategies import Strategy
import jesse.indicators as ta

class GoldWarriorFINAL(Strategy):
    """
    ESTRATEGIA FINAL CERTIFICADA - ORO 2026.
    Sin ADN, sin HP, sin caché.
    """
    def should_long(self) -> bool:
        return self.price > ta.ema(self.candles, 5) and self.price > ta.ema(self.candles, 10)

    def should_short(self) -> bool:
        return self.price < ta.ema(self.candles, 5) and self.price < ta.ema(self.candles, 10)

    def go_long(self):
        qty = 0.04
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 15
        self.take_profit = qty, self.price + 30

    def go_short(self):
        qty = 0.04
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 15
        self.take_profit = qty, self.price - 30

    def should_cancel_entry(self) -> bool: return False
