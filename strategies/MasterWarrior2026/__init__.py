from jesse.strategies import Strategy
import jesse.indicators as ta

class MasterWarrior2026(Strategy):
    """
    TITAN HFT VAMPIRE: Diseñada para +1000 trades diarios.
    Entra por micro-oscilación de precio.
    """
    def hyperparameters(self):
        return [
            {'name': 'sensitivity', 'type': 'float', 'min': 0.1, 'max': 2.0, 'default': 0.5},
            {'name': 'tp_usd', 'type': 'float', 'min': 1.0, 'max': 10.0, 'default': 2.0}
        ]

    def should_long(self) -> bool:
        # Entra si el precio actual es distinto al de la vela anterior (Agresión pura)
        return abs(self.price - self.candles[-1][1]) > self.hp['sensitivity']

    def should_short(self) -> bool:
        # En HFT el short es el espejo del long
        return abs(self.price - self.candles[-1][1]) > self.hp['sensitivity']

    def go_long(self):
        # 0.5 lotes para BTC (~$30k de exposición con 50x)
        qty = 0.5 
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - self.hp['tp_usd']
        self.take_profit = qty, self.price + self.hp['tp_usd']

    def go_short(self):
        qty = 0.5
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + self.hp['tp_usd']
        self.take_profit = qty, self.price - self.hp['tp_usd']

    def should_cancel_entry(self) -> bool: return False
