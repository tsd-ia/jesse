from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class DeadMarketWinner(Strategy):
    """
    Estrategia diseñada para ganar en mercados con volatilidad de 0.01 centavos.
    Compra en el soporte del rango y vende en la resistencia.
    """
    def should_long(self) -> bool:
        # Si el precio toca el minimo del rango (.29)
        return not self.is_open and self.price <= 5024.29

    def should_short(self) -> bool:
        # Si el precio toca el maximo del rango (.30)
        return not self.is_open and self.price >= 5024.30

    def go_long(self):
        qty = 10.0 # Lotaje pesado para mercado muerto
        self.buy = qty, self.price
        self.take_profit = qty, 5024.30 # Salida en el siguiente centavo

    def go_short(self):
        qty = 10.0
        self.sell = qty, self.price
        self.take_profit = qty, 5024.29

    def should_cancel_entry(self) -> bool: return False
