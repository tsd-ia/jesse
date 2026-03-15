from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class GoldMasterGrid(Strategy):
    """
    Lógica 'robada' de bots tipo Grid.
    Realiza múltiples entradas si el precio va en contra, 
    buscando una salida rápida en profit total.
    """
    def should_long(self) -> bool:
        # 1800 jugadas significa entrar casi siempre que haya una pequeña desviación
        return not self.is_open and ta.rsi(self.candles, 14) < 45

    def should_short(self) -> bool:
        return not self.is_open and ta.rsi(self.candles, 14) > 55

    def go_long(self):
        # Lotaje pequeño para aguantar el Grid (0.01)
        self.buy = 0.01, self.price
        self.take_profit = 0.01, self.price + 2.0

    def go_short(self):
        self.sell = 0.01, self.price
        self.take_profit = 0.01, self.price - 2.0

    def should_cancel_entry(self) -> bool: return False
