from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class ExnessSniper(Strategy):
    """
    Estrategia ajustada para mercados de bajisima volatilidad (0.01 centavos).
    Busca explotar el Spread Cero de Exness.
    """
    def should_long(self) -> bool:
        # Entrar si hay CUALQUIER movimiento hacia arriba respecto a la vela anterior
        if len(self.candles) < 2: return False
        return not self.is_open and self.price > self.candles[-2][2]

    def should_short(self) -> bool:
        if len(self.candles) < 2: return False
        return not self.is_open and self.price < self.candles[-2][2]

    def go_long(self):
        qty = 0.1 # Lotaje agresivo para notar los centavos
        self.buy = qty, self.price
        # Take Profit ultra-rapido de 5 centavos
        self.take_profit = qty, self.price + 0.05
        self.stop_loss = qty, self.price - 0.05

    def go_short(self):
        qty = 0.1
        self.sell = qty, self.price
        self.take_profit = qty, self.price - 0.05
        self.stop_loss = qty, self.price + 0.05

    def should_cancel_entry(self) -> bool: return False
