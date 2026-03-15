from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Antigravity_Beast(Strategy):
    """
    Antigravity Beast v1.0 - Diseñada para el Oro 2026.
    Enfoque: Liquidez Extrema y Seguimiento de Tendencia agresivo.
    """
    
    @property
    def trend_ema(self):
        return ta.ema(self.candles, period=200)
    
    @property
    def fast_ema(self):
        return ta.ema(self.candles, period=13)

    @property
    def adx(self):
        return ta.adx(self.candles, period=14)

    @property
    def atr(self):
        return ta.atr(self.candles, period=14)

    def should_long(self) -> bool:
        # Condición: Tendencia confirmada + Volatilidad (ADX > 25) + Momentum
        return (self.price > self.trend_ema and 
                self.fast_ema > self.trend_ema and 
                self.adx > 25 and 
                self.price > self.fast_ema)

    def should_short(self) -> bool:
        return (self.price < self.trend_ema and 
                self.fast_ema < self.trend_ema and 
                self.adx > 25 and 
                self.price < self.fast_ema)

    def go_long(self):
        # Gestión de capital dinámica basada en ATR
        risk_per_trade = self.balance * 0.05 # Arriesgamos 5%
        stop_distance = self.atr * 2
        
        qty = utils.size_to_qty(risk_per_trade / (stop_distance if stop_distance > 0 else 1), self.price, fee_rate=self.fee_rate)
        # Asegurar un lotaje mínimo y apalancamiento si es necesario
        qty = max(qty, utils.size_to_qty(self.balance * 0.2, self.price, fee_rate=self.fee_rate))
        
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - stop_distance
        self.take_profit = qty, self.price + (stop_distance * 4) # R:R 1:4 para ese 200%

    def go_short(self):
        risk_per_trade = self.balance * 0.05
        stop_distance = self.atr * 2
        
        qty = utils.size_to_qty(risk_per_trade / (stop_distance if stop_distance > 0 else 1), self.price, fee_rate=self.fee_rate)
        qty = max(qty, utils.size_to_qty(self.balance * 0.2, self.price, fee_rate=self.fee_rate))
        
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + stop_distance
        self.take_profit = qty, self.price - (stop_distance * 4)

    def should_cancel_entry(self) -> bool:
        return False
