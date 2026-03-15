from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import jesse.helpers as jh

class MasterWarrior2026(Strategy):
    """
    MASTER WARRIOR 2026 - VERSIÓN ESTABLE ORO.
    Valores fijos para evitar errores de carga en Jesse Dash.
    """
    def should_long(self) -> bool:
        # Cruce simple de EMA 5/10 para el Oro
        ema5 = ta.ema(self.candles, 5)
        ema10 = ta.ema(self.candles, 10)
        return ema5 > ema10 and self.price > self.candles[-2][2]

    def should_short(self) -> bool:
        ema5 = ta.ema(self.candles, 5)
        ema10 = ta.ema(self.candles, 10)
        return ema5 < ema10 and self.price < self.candles[-2][2]

    def go_long(self):
        qty = 0.04 # Lotaje seguro para balance de $500
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 15
        self.take_profit = qty, self.price + 30

    def go_short(self):
        qty = 0.04
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 15
        self.take_profit = qty, self.price - 30

    def should_cancel_entry(self) -> bool:
        return False
