from typing import Dict
from datetime import datetime


class CurrencyConverter:
    # Exchange rates as of a recent date (can be updated periodically)
    # Base currency is USD
    EXCHANGE_RATES: Dict[str, float] = {
        "USD": 1.0,
        "SEK": 10.83,  # Last updated 2025-02-13
    }

    @classmethod
    def convert(cls, amount: float, target_currency: str) -> float:
        """Convert USD amount to target currency."""
        target_currency = target_currency.upper()

        if target_currency not in cls.EXCHANGE_RATES:
            raise ValueError(f"Unsupported currency: {target_currency}")

        converted_amount = amount * cls.EXCHANGE_RATES[target_currency]
        return converted_amount
