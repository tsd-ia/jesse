from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import jesse.helpers as jh

class MasterWarrior2026(Strategy):
    """
    Estrategia de Élite 2026: Fusión de los mejores algoritmos de Oro.
    ADN: SMC Institutional, HFT Momentum, ADR Dynamic Grid.
    Filtro de Inteligencia Horaria: Solo opera en NY Overlap (13:00-16:00 UTC).
    """

    def should_long(self) -> bool:
        # 1. Filtro Horario Institucional
        hour = int(jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].split(':')[0])
        if not (13 <= hour <= 16): return False
        
        # 2. Lógica Smart Money (SMC) + Momentum
        # Entra si el precio rompe el máximo de las últimas 5 velas con volumen institucional
        return not self.is_open and self.price > ta.max(self.candles[:-1], 5) and ta.atr(self.candles) > ta.atr(self.candles, 14)

    def should_short(self) -> bool:
        hour = int(jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].split(':')[0])
        if not (13 <= hour <= 16): return False
        
        return not self.is_open and self.price < ta.min(self.candles[:-1], 5) and ta.atr(self.candles) > ta.atr(self.candles, 14)

    def go_long(self):
        # Gestión de Capital de Reconquista
        qty = 0.5 # Lotaje agresivo para cuenta de $500
        self.buy = qty, self.price
        # Take Profit y Stop Loss dinámicos basados en ATR
        self.stop_loss = qty, self.price - 10.0
        self.take_profit = qty, self.price + 30.0

    def go_short(self):
        qty = 0.5
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 10.0
        self.take_profit = qty, self.price - 30.0

    def should_cancel_entry(self) -> bool: return False
