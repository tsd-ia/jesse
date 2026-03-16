from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class MasterWarrior2026(Strategy):
    """
    TITAN HFT: Diseñada para altísima frecuencia (+1000 trades/día).
    Gatillo basado en micro-volatilidad y reversión rápida.
    """
    def should_long(self) -> bool:
        # Entra si el precio actual está apenas por debajo de la apertura (Scalping agresivo)
        return self.price < self.candles[-1][1] - 1

    def should_short(self) -> bool:
        # Vende si el precio sube un mínimo (Short Scalping)
        return self.price > self.candles[-1][1] + 1

    def go_long(self):
        # 0.1 BTC para que el margen no nos bloquee los 1000 trades
        qty = 0.1
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 20 # SL muy corto
        self.take_profit = qty, self.price + 10 # TP rapidísimo para cerrar y volver a entrar

    def go_short(self):
        qty = 0.1
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 20
        self.take_profit = qty, self.price - 10

    def should_cancel_entry(self) -> bool:
        return False
