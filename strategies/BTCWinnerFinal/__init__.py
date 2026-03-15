from jesse.strategies impfrom jesse.strategies import Strategy, Parameter
import jesse.indicators as ta
from jesse import utils

class BTCWinnerFinal(Strategy):
    @property
        def hyperparameters(self):
                return [
                            {'name': 'rsi_period', 'type': int, 'min': 7, 'max': 30, 'default': 14},
                                        {'name': 'rsi_level', 'type': int, 'min': 20, 'max': 40, 'default': 30},
                                                ]
                                                
                                                    def should_long(self) -> bool:
                                                            return ta.rsi(self.candles, self.hp['rsi_period']) < self.hp['rsi_level']
                                                            
                                                                def should_short(self) -> bool:
                                                                        return False
                                                                        
                                                                            def should_cancel_entry(self) -> bool:
                                                                                    return True
                                                                                    
                                                                                        def go_long(self):
                                                                                                self.buy = 0.05, self.price
                                                                                                
                                                                                                    def go_short(self):
                                                                                                            pass
                                                                                                            
                                                                                                                def on_open_position(self, order):
                                                                                                                        self.stop_loss = self.position.qty, self.price * 0.98
                                                                                                                                self.take_profit = self.position.qty, self.price * 1.02
                                                                                                                                ort Strategy
import jesse.indicators as ta
from jesse import utils


class BTCWinnerFinal(Strategy):
    def should_long(self) -> bool:
        return False

    def should_short(self) -> bool:
        # For futures trading only
        return False
        
    def go_long(self):
        pass

    def go_short(self):
        # For futures trading only
        pass
