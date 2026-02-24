"""
models.py - Data Structures for the Trading Bot

This file defines all the data structures (types) used in our trading bot.
Think of these as blueprints or templates for organizing information.

Key concepts for beginners:
- TypedDict: A dictionary with specific keys and types (like a struct in other languages)
- Decimal: A precise number type for money (better than float for currency)
"""

from decimal import Decimal
from typing import TypedDict

# ==============================================================================
# PRECISION CONSTANTS
# ==============================================================================
# These control how many decimal places we use for each currency
# USD uses 2 decimal places (cents): $10.50
USD_PRECISION = Decimal("0.01")

# XRP uses 6 decimal places (common for cryptocurrencies): 0.123456 XRP
XRP_PRECISION = Decimal("0.000001")


# ==============================================================================
# DATA STRUCTURES (TypedDicts)
# ==============================================================================


class Wallet(TypedDict):
    """
    Represents a cryptocurrency wallet containing two types of currency.

    A wallet is like your bank account - it keeps track of how much money you have.
    In our case, we track both regular money (USD) and cryptocurrency (XRP).

    Attributes:
        usd: Amount of US Dollars in the wallet (e.g., Decimal("1000.00"))
        xrp: Amount of XRP cryptocurrency in the wallet (e.g., Decimal("500.123456"))
    """

    usd: Decimal  # US Dollar balance
    xrp: Decimal  # XRP (Ripple) cryptocurrency balance


class Trade(TypedDict):
    """
    Represents a single trade instruction.

    A trade is an instruction to buy or sell cryptocurrency.

    Attributes:
        action: Either "buy" (purchase XRP with USD) or "sell" (sell XRP for USD)
        amount: How much XRP we want to trade

    Example:
        Trade(action="buy", amount=Decimal("100.0"))  # Buy 100 XRP
    """

    action: str  # "buy" or "sell"
    amount: Decimal  # Amount of XRP to trade


class TradeResult(TypedDict):
    """
    Represents the outcome of a trade after it's been executed.

    After we try to execute a trade, we get back a result that tells us:
    - Did it work? (success)
    - What changed in our wallet? (usd_change, xrp_change)
    - How much did we pay in fees? (fee_paid)
    - Any additional information? (note)

    Attributes:
        success: True if trade executed, False if it failed
        note: Human-readable message about what happened
        fee_paid: Amount paid to the exchange for doing the trade
        usd_change: How much USD changed (negative = spent, positive = received)
        xrp_change: How much XRP changed (positive = bought, negative = sold)

    Example:
        TradeResult(
            success=True,
            note="Buy executed successfully.",
            fee_paid=Decimal("1.00"),
            usd_change=Decimal("-100.00"),  # We spent $100
            xrp_change=Decimal("50.0")       # We received 50 XRP
        )
    """

    success: bool  # Did the trade execute successfully?
    note: str  # Additional information about the trade result
    fee_paid: Decimal  # Total fees paid for this trade
    usd_change: Decimal  # Change in USD balance (negative for buys, positive for sells)
    xrp_change: Decimal  # Change in XRP balance (positive for buys, negative for sells)
