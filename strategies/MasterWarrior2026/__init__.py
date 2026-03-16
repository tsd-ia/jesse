from jesse.strategies import Strategy

class MasterWarrior2026(Strategy):
    """
    TITAN HFT METRALLETA: Ejecución forzada de +1000 trades/día.
    """
    def should_long(self) -> bool:
        # Entra si no hay posición (Gatillo instantáneo)
        return True

    def should_short(self) -> bool:
        return True

    def go_long(self):
        qty = 1.0 # 1.0 BTC por trade
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 10
        self.take_profit = qty, self.price + 5 

    def go_short(self):
        qty = 1.0
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 10
        self.take_profit = qty, self.price - 5

    def should_cancel_entry(self) -> bool: return False
