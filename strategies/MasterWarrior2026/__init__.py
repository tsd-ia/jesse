from jesse.strategies import Strategy

class MasterWarrior2026(Strategy):
    """
    TITAN HFT VAMPIRE: Diseñada para +1000 trades diarios.
    Gatillo ultra-sensible para scalping de alta frecuencia.
    """
    def should_long(self) -> bool:
        # Dispara si el precio actual es distinto al cierre anterior por $0.10
        return abs(self.price - self.candles[-1][2]) > 0.1

    def should_short(self) -> bool:
        return abs(self.price - self.candles[-1][2]) > 0.1

    def go_long(self):
        qty = 0.5 # Lotaje de asalto
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 2.0
        self.take_profit = qty, self.price + 2.0

    def go_short(self):
        qty = 0.5
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 2.0
        self.take_profit = qty, self.price - 2.0

    def should_cancel_entry(self) -> bool: return False
