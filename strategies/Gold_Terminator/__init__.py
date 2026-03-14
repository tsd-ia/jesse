from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Gold_Terminator(Strategy):
    def _qty(self):
        return utils.size_to_qty(self.balance * 4, self.price, fee_rate=self.fee_rate)

    def should_long(self) -> bool:
        return ta.rsi(self.candles, period=7) > 60 and self._qty() > 0

    def should_short(self) -> bool:
        return ta.rsi(self.candles, period=7) < 40 and self._qty() > 0

    def go_long(self):
        # Usar self.price para simular mercado en Jesse
        self.buy = self._qty(), self.price

    def go_short(self):
        self.sell = self._qty(), self.price

    def on_open_position(self, order):
        qty = self.position.qty
        if self.is_long:
            self.stop_loss = qty, self.price - 2.0
            self.take_profit = qty, self.price + 8.0
        else:
            self.stop_loss = qty, self.price + 2.0
            self.take_profit = qty, self.price - 8.0

    def should_cancel_entry(self) -> bool:
        return True
