from jesse.strategies import Strategy

class MasterWarrior2026(Strategy):
    """
    TITAN VAMPIRO HFT: Diseñada para +1000 trades diarios.
    Gatillo ultra-sensible de $1.00 USD.
    """
    def should_long(self) -> bool:
        # Si el precio se mueve $1 hacia arriba respecto a la apertura de la vela, DISPARA.
        return self.price > self.candles[-1][1] + 1.0

    def should_short(self) -> bool:
        # Si el precio se mueve $1 hacia abajo, DISPARA.
        return self.price < self.candles[-1][1] - 1.0

    def go_long(self):
        qty = 0.5 # Lotaje de asalto
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 5.0
        self.take_profit = qty, self.price + 5.0

    def go_short(self):
        qty = 0.5
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 5.0
        self.take_profit = qty, self.price - 5.0

    def should_cancel_entry(self) -> bool: return False
