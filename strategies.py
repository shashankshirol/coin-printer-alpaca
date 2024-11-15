import os
import pandas as pd
from backtesting import Backtest, Strategy

from fetch_data import generate_data

HISTORICAL = "historical_data"
PLOT_PATH = "bt_plots"
# test for apple
data = pd.read_pickle(os.path.join(HISTORICAL, "AMZN.pickle"))


# Moving Average Crossover Strategy
class SMACross(Strategy):
    N_short = 10
    N_long = 30

    def init(self):
        close = self.data.Close
        self.mva_short = self.I(self.mv_average, close, self.N_short)
        self.mva_long = self.I(self.mv_average, close, self.N_long)

    def next(self):
        if self.mva_short[-2] < self.mva_long[-2] and self.mva_short[-1] > self.mva_long[-1]:
            self.buy()
        elif self.mva_short[-2] > self.mva_long[-2] and self.mva_short[-1] < self.mva_long[-1]:
            if self.position:
                self.position.close()

    def mv_average(self, price, periods):
        return pd.Series(price).rolling(periods).mean()
    

def backtester():
    strategy = SMACross

    generate_data(False)
    datasets = [os.path.join(HISTORICAL, ticker_pickle) for ticker_pickle in os.listdir(HISTORICAL)]
    for ds in datasets:
        data = pd.read_pickle(ds)
        bt = Backtest(data, strategy, cash=10000, commission=0, exclusive_orders=True)
        output = bt.run()
        print(f'Return [%]: {round(output.get("Return [%]"), 3)} - Buy & Hold Return [%]: {round(output.get("Buy & Hold Return [%]"), 3)} - {ds}')

# Run the backtester
backtester()