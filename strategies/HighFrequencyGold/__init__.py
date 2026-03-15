from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class HighFrequencyGold(Strategy):
    """
    Estrategia HFT diseñada para 1,800+ jugadas al día.
    Entra en cada micro-oscilación del precio.
    """
    def should_long(self) -> bool:
        # Entrar si el precio es menor que el cierre anterior (micro-reversión)
        return not self.is_open and self.price < self.candles[-1][2]

    def should_short(self) -> bool:
        return not self.is_open and self.price > self.candles[-1][2]

    def go_long(self):
        # Usamos 0.05 para que el profit de $10 sea significativo ($0.50 neto)
        qty = 0.05 
        self.buy = qty, self.price
        self.take_profit = qty, self.price + 10.0
        self.stop_loss = qty, self.price - 5.0

    def go_short(self):
        qty = 0.05
        self.sell = qty, self.price
        self.take_profit = qty, self.price - 10.0
        self.stop_loss = qty, self.price + 5.0

    def should_cancel_entry(self) -> bool: return False
