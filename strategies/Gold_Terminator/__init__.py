from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils

class Gold_Terminator(Strategy):
    def _qty(self):
        qty = utils.size_to_qty(self.balance * 1, self.price, fee_rate=self.fee_rate)
        return qty if qty > 0 else 0.01 # Un mínimo para debug

    def should_long(self) -> bool:
        return ta.rsi(self.candles, period=7) > 60

    def should_short(self) -> bool:
        return ta.rsi(self.candles, period=7) < 40

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
        return False
