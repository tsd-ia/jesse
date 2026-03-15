from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import jesse.helpers as jh

class MasterWarrior2026_V2(Strategy):
    """
    VERSIÓN DE FUERZA BRUTA: Bypass de caché de Jesse.
    """
    @property
    def dna(self):
        if self.hp is None: return 'Trend_Sniper'
        return self.hp.get('dna', 'Trend_Sniper')

    def should_long(self) -> bool:
        return self.price > ta.ema(self.candles, 5)

    def should_short(self) -> bool:
        return self.price < ta.ema(self.candles, 5)

    def go_long(self):
        qty = 0.05
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 10
        self.take_profit = qty, self.price + 20

    def go_short(self):
        qty = 0.05
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 10
        self.take_profit = qty, self.price - 20

    def should_cancel_entry(self) -> bool: return False
