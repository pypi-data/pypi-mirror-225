import numpy as np

from . import Strategy
from .. import Signal, TradeType


class PairTradingStrategy(Strategy):
    """
    A pair trading strategy that identifies trading opportunities between two correlated equities.

    Parameters:
    - threshold (float): Z-score threshold to trigger trading signals.

    Methods:
    - fit(history): Identify suitable pairs based on correlation and other criteria.
    - execute(row, idx, history) -> dict: Generate trading signals based on Z-score.
    """

    def __init__(self, threshold=2.0):
        super().__init__()
        self.threshold = threshold
        self.pair = None

    def fit(self, history):
        """
        Identify suitable pairs for trading based on correlation and other criteria.

        Args:
        - history (History): Historical price data of multiple equities.

        Returns:
        None
        """
        pass

    def execute(self, row, idx, history) -> list[Signal]:
        """
        Generate trading signals based on the Z-score of the selected equity pair.

        Args:
        - row (pd.Series): Latest row of equity prices.
        - idx (int): Index of the current row.
        - history (pd.DataFrame): Historical price data of multiple equities.

        Returns:
        dict: Trading signals for each equity.
        """
        signals = [Signal(TradeType.WAIT) for _ in range(len(history.columns))]
        if self.pair is not None:
            z_scores = (row[self.pair[0]] - row[self.pair[1]]) / np.std(history[self.pair[0]] - history[self.pair[1]])
            if z_scores > self.threshold:
                signals[0] = Signal(TradeType.SELL, 1)
                signals[1] = Signal(TradeType.BUY, 1)
            elif z_scores < -self.threshold:
                signals[0] = Signal(TradeType.BUY, 1)
                signals[1] = Signal(TradeType.SELL, 1)
        return signals
