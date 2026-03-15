from jesse.strategies import Strategy
import jesse.indicators as ta
from jesse import utils
import jesse.helpers as jh

class SMC_KillZone_Sniper(Strategy):
    """
    Estrategia de Élite: Kill Zone Sniper 2026.
    Lógica: Solo opera de 13:00 a 17:00 UTC. 
    Busca barrido de liquidez y expansión institucional.
    """
    
    def should_long(self) -> bool:
        # 1. Filtro Horario (Kill Zone NY/London Overlap)
        hour = jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].split(':')[0]
        is_kill_zone = 13 <= int(hour) <= 17
        
        if not is_kill_zone: return False
        
        # 2. Filtro de Liquidez (Precio por debajo de la EMA 50 en 1m = Descuento)
        ema50 = ta.ema(self.candles, 50)
        
        # 3. Disparador: Cambio de carácter micro (Cierre arriba de la vela anterior)
        return not self.is_open and self.price < ema50 and self.price > self.candles[-2][2]

    def should_short(self) -> bool:
        hour = jh.timestamp_to_date(self.current_candle[0]).split(' ')[1].split(':')[0]
        is_kill_zone = 13 <= int(hour) <= 17
        
        if not is_kill_zone: return False
        
        ema50 = ta.ema(self.candles, 50)
        return not self.is_open and self.price > ema50 and self.price < self.candles[-2][2]

    def go_long(self):
        # Arriesgamos el 10% por operación con stop ajustado
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.buy = qty, self.price
        self.stop_loss = qty, self.price - 10.0
        self.take_profit = qty, self.price + 30.0

    def go_short(self):
        qty = utils.size_to_qty(self.balance * 0.1, self.price, fee_rate=self.fee_rate)
        self.sell = qty, self.price
        self.stop_loss = qty, self.price + 10.0
        self.take_profit = qty, self.price - 30.0

    def should_cancel_entry(self) -> bool: return False
