from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import jesse.helpers as jh

# ==========================================
# ESCUADRÓN 1: INSTITUTIONAL (SMC)
# ==========================================
class SMC_Elite_Hunter(Strategy):
    """Estilo: Prop Firm Champions. Busca liquidez en Kill Zones."""
    def should_long(self) -> bool:
        hour = jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].split(':')[0]
        if not (8 <= int(hour) <= 10 or 13 <= int(hour) <= 16): return False # Kill Zones
        low_sweep = self.price < ta.min(self.candles[:-1], 20) # Barrido de minimos
        return not self.is_open and low_sweep and self.price > self.candles[-1][2]

    def should_short(self) -> bool:
        hour = jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].split(':')[0]
        if not (8 <= int(hour) <= 10 or 13 <= int(hour) <= 16): return False
        high_sweep = self.price > ta.max(self.candles[:-1], 20)
        return not self.is_open and high_sweep and self.price < self.candles[-1][2]

    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.05, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 15.0
        self.take_profit = qty, self.price + 45.0 # R:R 1:3

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.05, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 15.0
        self.take_profit = qty, self.price - 45.0

# ==========================================
# ESCUADRÓN 2: HFT VELOCITY
# ==========================================
class HFT_Velocity_Bot(Strategy):
    """Estilo: MQL5 'XAU Scalper'. Basado en momentum HFT."""
    def should_long(self) -> bool:
        # Entra si la vela actual expande mas del 200% del ATR promedio en 1m
        return not self.is_open and self.price > ta.ema(self.candles, 10) and ta.atr(self.candles) > ta.atr(self.candles, 14) * 2

    def should_short(self) -> bool:
        return not self.is_open and self.price < ta.ema(self.candles, 10) and ta.atr(self.candles) > ta.atr(self.candles, 14) * 2

    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.take_profit = qty, self.price + 10.0
        self.stop_loss = qty, self.price - 5.0

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.take_profit = qty, self.price - 10.0
        self.stop_loss = qty, self.price + 5.0

# ==========================================
# ESCUADRÓN 3: GRID PRECISION
# ==========================================
class Dark_Venus_Grid(Strategy):
    """Estilo: 'Dark Venus'. Mean Reversion con red de seguridad."""
    def should_long(self) -> bool:
        return not self.is_open and ta.rsi(self.candles, 14) < 30 and self.price < ta.bollinger_bands(self.candles).lowerband

    def should_short(self) -> bool:
        return not self.is_open and ta.rsi(self.candles, 14) > 70 and self.price > ta.bollinger_bands(self.candles).upperband

    def go_long(self):
        qty = 0.01 # Lote minimo para aguantar el Grid
        self.buy = qty, self.price
        self.take_profit = qty, self.price + 5.0

    def go_short(self):
        qty = 0.01
        self.sell = qty, self.price
        self.take_profit = qty, self.price - 5.0

# (Seguiremos añadiendo hasta completar los 20 modelos en el simulador)
