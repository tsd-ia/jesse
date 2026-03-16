from jesse.strategies import Strategy

class MasterWarrior2026(Strategy):
    """
    TITAN HFT METRALLETA: Diseñada para 1440 trades diarios.
    Entra en cada vela sin preguntar.
    """
    def should_long(self) -> bool:
        # Entra si no hay posición abierta (Frecuencia máxima)
        return True

    def should_short(self) -> bool:
        return True

    def go_long(self):
        qty = 10 # 10 BTC de asalto (balance de $1M permite esto)
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 10
        self.take_profit = qty, self.price + 5 # Scalping ultra-corto

    def go_short(self):
        qty = 10
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 10
        self.take_profit = qty, self.price - 5

    def should_cancel_entry(self) -> bool: return False
