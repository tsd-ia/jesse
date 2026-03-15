from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils

class GridMasterGold(Strategy):
    """Lógica Robada: Grid Progresivo de XAUUSD."""
    def should_long(self) -> bool:
        return len(self.positions) == 0 and ta.rsi(self.candles, period=14) < 30

    def should_short(self) -> bool:
        return len(self.positions) == 0 and ta.rsi(self.candles, period=14) > 70

    def go_long(self):
        qty = utils.size_to_qty(50, self.price, fee_rate=self.fee_rate) # $50 lotaje base
        self.buy = qty, self.price
        self.take_profit = qty, self.price + 5.0

    def go_short(self):
        qty = utils.size_to_qty(50, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.take_profit = qty, self.price - 5.0

class ICTJudasSwing(Strategy):
    """Lógica Robada: Judas Swing de ICT (Kill Zones)."""
    def should_long(self) -> bool:
        # Solo opera en Kill Zone (ej: 13:00 UTC)
        is_kill_zone = jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].startswith('13:')
        return is_kill_zone and self.price < ta.ema(self.candles, 50) # Manipulación abajo

    def should_short(self) -> bool:
        is_kill_zone = jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].startswith('13:')
        return is_kill_zone and self.price > ta.ema(self.candles, 50)

    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.2, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.take_profit = qty, self.price + 20.0
        self.stop_loss = qty, self.price - 5.0

class XAUSniperBreakout(Strategy):
    """Lógica Robada: Sniper de Volatilidad."""
    def should_long(self) -> bool:
        return self.price > ta.high_pass(self.candles) and ta.adx(self.candles) > 25

    def should_short(self) -> bool:
        return self.price < ta.low_pass(self.candles) and ta.adx(self.candles) > 25

    def go_long(self):
        qty = utils.size_to_qty(self.balance * 0.5, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.take_profit = qty, self.price + 10.0
        self.stop_loss = qty, self.price - 2.0
