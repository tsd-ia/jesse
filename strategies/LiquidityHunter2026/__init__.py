from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class LiquidityHunter2026(Strategy):
    """
    SMC Liquidity Hunter - Basada en bots de alto rendimiento MQL5 2026.
    Lógica: Detectar Fair Value Gaps (FVG) y Order Blocks institucionales.
    """
    
    @property
    def fvg_gap(self):
        # Un FVG simple: Espacio entre la mecha de la vela 1 y la 3
        if len(self.candles) < 3: return 0
        v1_high = self.candles[-3][3]
        v3_low = self.candles[-1][4]
        if v3_low > v1_high: # FVG alcista
            return v3_low - v1_high
        return 0

    def should_long(self) -> bool:
        # Estructura alcista (EMA 200) + FVG (Liquidez)
        ema200 = ta.ema(self.candles, period=200)
        return self.price > ema200 and self.fvg_gap > 0.5 # Gap significativo

    def should_short(self) -> bool:
        ema200 = ta.ema(self.candles, period=200)
        v1_low = self.candles[-3][4]
        v3_high = self.candles[-1][3]
        fvg_bearish = v1_low - v3_high
        return self.price < ema200 and fvg_bearish > 0.5

    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        # Stop Loss por debajo del FVG
        self.stop_loss = qty, self.price - 5.0
        self.take_profit = qty, self.price + 15.0

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 5.0
        self.take_profit = qty, self.price - 15.0

    def should_cancel_entry(self) -> bool:
        return False
