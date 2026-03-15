from jesse.strategies import Strategy
import jesse.indicators as ta

class MasterWarrior2026(Strategy):
    """
    TITAN HFT VAMPIRE v2: Gatillo ultra-rápido para +1000 trades/día.
    """
    def hyperparameters(self):
        return [
            {'name': 'sensitivity', 'type': 'float', 'min': 0.01, 'max': 0.5, 'default': 0.1},
            {'name': 'tp_usd', 'type': 'float', 'min': 0.5, 'max': 5.0, 'default': 1.0}
        ]

    def should_long(self) -> bool:
        # Entra si hay cualquier movimiento superior a la sensibilidad (HFT)
        return abs(self.price - self.candles[-1][1]) > self.hp['sensitivity']

    def should_short(self) -> bool:
        return abs(self.price - self.candles[-1][1]) > self.hp['sensitivity']

    def go_long(self):
        # Lotaje mínimo (0.001) para permitir miles de trades sin liquidación inmediata
        qty = 0.01
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - self.hp['tp_usd']
        self.take_profit = qty, self.price + self.hp['tp_usd']

    def go_short(self):
        qty = 0.01
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + self.hp['tp_usd']
        self.take_profit = qty, self.price - self.hp['tp_usd']

    def should_cancel_entry(self) -> bool: return False
