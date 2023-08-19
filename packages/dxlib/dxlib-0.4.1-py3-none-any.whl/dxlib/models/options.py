import numpy as np
import pandas as pd
from scipy.stats import norm
from typing import Optional
from enum import Enum


class OptionType(Enum):
    CALL = 1
    PUT = -1


class GenericOption:
    def __init__(self, strike: float, expiry: float, option_type: OptionType):
        self.strike = strike
        self.expiry = expiry
        self.option_type = option_type


class Option(GenericOption):
    def __init__(self, strike: float, expiry: float, option_type: OptionType, underlying_price: Optional[float] = None,
                 volatility: Optional[float] = None):
        super().__init__(strike, expiry, option_type)
        self.underlying_price = underlying_price
        self.volatility = volatility


class OptionHelper:
    def __init__(self, option: Option, risk_free_rate: float):
        self.option = option
        self.risk_free_rate = risk_free_rate

    def d1(self) -> float:
        return (np.log(self.option.underlying_price / self.option.strike) + (
                self.risk_free_rate + 0.5 * self.option.volatility ** 2) * self.option.expiry) / (
                self.option.volatility * np.sqrt(self.option.expiry))

    def d2(self) -> float:
        return self.d1() - self.option.volatility * np.sqrt(self.option.expiry)

    def option_price(self) -> float:
        if self.option.option_type == OptionType.CALL:
            return self.option.underlying_price * norm.cdf(self.d1()) - self.option.strike * np.exp(
                -self.risk_free_rate * self.option.expiry) * norm.cdf(self.d2())
        else:
            return self.option.strike * np.exp(-self.risk_free_rate * self.option.expiry) * norm.cdf(
                -self.d2()) - self.option.underlying_price * norm.cdf(-self.d1())

    def vega(self) -> float:
        return self.option.underlying_price * norm.pdf(self.d1()) * np.sqrt(self.option.expiry)

    def implied_volatility(self, market_price: float) -> float:
        MAX_ITERATIONS = 100
        PRECISION = 1.0e-5

        sigma = 0.5
        for i in range(0, MAX_ITERATIONS):
            self.option.volatility = sigma
            price = self.option_price() - market_price
            if abs(price) < PRECISION:
                return sigma
            sigma = sigma - price / self.vega()

        return sigma  # Value didn't converge in MAX_ITERATIONS, return best guess
