"""
venue.py - Trading Venue (Exchange) Simulation

This file simulates a cryptocurrency exchange (like Coinbase or Binance).
A "venue" is just a fancy name for an exchange where you can buy and sell crypto.

Key concepts for beginners:
- A trading venue has a price for XRP (which changes over time)
- Each venue charges a fee for trades (like a commission)
- We simulate market data instead of connecting to real exchanges
"""

from decimal import Decimal
import random
from typing import List, Tuple
from loguru import logger

# Import our data structures from models.py
from models import (
    Trade,
    TradeResult,
    Wallet,
    USD_PRECISION,
    XRP_PRECISION,
)

# ==============================================================================
# TRADING VENUE CLASS
# ==============================================================================


class TradingVenue:
    """
    Simulates a cryptocurrency exchange (like Coinbase, Binance, etc.).

    A trading venue is where you can buy and sell cryptocurrency.
    Each venue has:
    - A name (e.g., "Venue A")
    - A fee structure (e.g., 0.1% per trade)
    - Price history (how the price of XRP changes over time)

    Attributes:
        name: The name of this exchange (e.g., "Venue A")
        fee: The percentage charged per trade (e.g., 0.001 = 0.1%)
        price_history: List of XRP prices over time
        current_step: Which time point we're currently at
        last_price: The most recent price we accessed
    """

    def __init__(self, name: str, fee: Decimal):
        """
        Initialize a new trading venue.

        Args:
            name: Name of the exchange (e.g., "Venue A")
            fee: Trading fee as a decimal (e.g., Decimal("0.001") = 0.1%)
        """
        self.name = name  # Exchange name
        self.price_history = []  # List of prices over time
        self.fee = fee  # Trading fee percentage
        self.current_step = 0  # Current time step (starts at 0)
        self.last_price = None  # Most recent price accessed

    def get_fee(self) -> Decimal:
        """
        Get the trading fee for this venue.

        Returns:
            The fee as a decimal (e.g., 0.001 means 0.1% fee)
        """
        return self.fee

    def set_price_history(self, price_history: List[Decimal]):
        """
        Set the price history for this venue.

        In a real bot, prices would come from an API. For learning,
        we manually set the prices ahead of time.

        Args:
            price_history: List of XRP prices over time
        """
        self.price_history = price_history

    def get_current_price(self) -> Decimal:
        """
        Get the current XRP price at this venue.

        This simulates making an API call to get the current price.
        In reality, you'd call something like: GET https://api.exchange.com/ticker

        Returns:
            The current XRP price in USD

        Raises:
            ValueError: If no price history is set
            IndexError: If we've run out of price data
        """
        # Check if we have any price data
        if not self.price_history:
            raise ValueError("Price history is not set for this trading venue.")

        # Check if we've gone past the end of our data
        if self.current_step >= len(self.price_history):
            raise IndexError("Current step exceeds available market data.")

        # Return the price at the current time step
        return self.price_history[self.current_step]

    def get_last_price(self) -> Decimal:
        """
        Get the last price we accessed.

        This is useful for calculating profit/loss when we have XRP left over.
        We value our remaining XRP at the last known price.

        Returns:
            The last accessed price, or current price if none accessed yet
        """
        # If we haven't accessed any price yet, use the current one
        if self.last_price is None:
            return self.get_current_price()

        # Round to USD precision (2 decimal places)
        return self.last_price.quantize(USD_PRECISION)

    def execute_trade(self, trade: Trade, wallet: Wallet) -> TradeResult:
        """
        Execute a buy or sell trade at this venue.

        This is the core trading logic. It:
        1. Checks if we have enough money/crypto to make the trade
        2. Calculates the cost including fees
        3. Updates the wallet balances
        4. Returns a result telling us what happened

        For BUY trades:
        - We spend USD to buy XRP
        - The cost includes the fee (we pay MORE than the base price)
        - Example: Buy 100 XRP at $1.00 with 0.1% fee = $100.10 total

        For SELL trades:
        - We sell XRP to get USD
        - The fee reduces what we receive (we get LESS than the base price)
        - Example: Sell 100 XRP at $1.00 with 0.1% fee = $99.90 received

        Args:
            trade: The trade instruction (buy/sell and amount)
            wallet: The wallet to update (will be modified!)

        Returns:
            TradeResult with success status and changes made
        """
        try:
            # STEP 1: Get the current price
            # We can't trade without knowing the price!
            price = self.get_current_price()

            # Save this price for later calculations
            self.last_price = price

            # STEP 2: Get the amount of XRP we want to trade
            xrp_amount = trade["amount"]

            # STEP 3: Handle BUY or SELL logic
            # The math is different depending on whether we're buying or selling

            if trade["action"].lower() == "buy":
                # ============================================================
                # BUY: We're using USD to purchase XRP
                # ============================================================

                # Calculate total cost in USD (including fee)
                # Formula: amount * price * (1 + fee_percentage)
                # Example: 100 XRP * $1.00 * (1 + 0.001) = $100.10
                usd_cost = (xrp_amount * price * (1 + self.fee)).quantize(USD_PRECISION)

                # Calculate just the fee portion
                # Formula: total_cost - base_cost
                fee_paid = usd_cost - (xrp_amount * price).quantize(USD_PRECISION)

                # Check if we have enough USD in the wallet
                if wallet["usd"] < usd_cost:
                    raise ValueError(
                        f"Not enough USD! Need ${usd_cost} but only have ${wallet['usd']}"
                    )

                # Execute the trade by updating the wallet
                wallet["usd"] -= usd_cost  # Subtract USD
                wallet["xrp"] += xrp_amount.quantize(XRP_PRECISION)  # Add XRP

                # Return success result with all the details
                return TradeResult(
                    success=True,
                    fee_paid=fee_paid,
                    usd_change=-usd_cost,  # Negative because we spent USD
                    xrp_change=xrp_amount,  # Positive because we gained XRP
                    note=f"✓ Bought {xrp_amount} XRP for ${usd_cost} (fee: ${fee_paid})",
                )

            elif trade["action"].lower() == "sell":
                # ============================================================
                # SELL: We're selling XRP to get USD
                # ============================================================

                # Check if we have enough XRP to sell
                if wallet["xrp"] < xrp_amount:
                    raise ValueError(
                        f"Not enough XRP! Need {xrp_amount} but only have {wallet['xrp']}"
                    )

                # Calculate USD received (after fee)
                # Formula: amount * price * (1 - fee_percentage)
                # Example: 100 XRP * $1.00 * (1 - 0.001) = $99.90
                usd_received = (xrp_amount * price * (1 - self.fee)).quantize(
                    USD_PRECISION
                )

                # Calculate the fee amount
                # Formula: base_value - amount_received
                fee_paid = (xrp_amount * price - usd_received).quantize(USD_PRECISION)

                # Execute the trade by updating the wallet
                wallet["xrp"] -= xrp_amount.quantize(XRP_PRECISION)  # Subtract XRP
                wallet["usd"] += usd_received  # Add USD

                # Return success result with all the details
                return TradeResult(
                    success=True,
                    fee_paid=fee_paid,
                    usd_change=usd_received,  # Positive because we received USD
                    xrp_change=-xrp_amount,  # Negative because we sold XRP
                    note=f"✓ Sold {xrp_amount} XRP for ${usd_received} (fee: ${fee_paid})",
                )

            else:
                # Invalid action (not "buy" or "sell")
                raise ValueError(
                    f"Invalid trade action: '{trade['action']}'. Must be 'buy' or 'sell'."
                )

        except (ValueError, IndexError) as e:
            # If anything goes wrong, log the error and return a failed result
            # This prevents the bot from crashing due to a single bad trade
            logger.error(f"❌ Trade failed on {self.name}: {e}")

            return TradeResult(
                success=False,
                fee_paid=Decimal("0"),
                usd_change=Decimal("0"),
                xrp_change=Decimal("0"),
                note=str(e),
            )

    def tick(self):
        """
        Move forward one time step in the market simulation.

        Think of time as moving in discrete steps (like frames in a video).
        Each time we call tick(), we move to the next price in our price_history.

        This allows us to simulate the passage of time and changing prices.
        """
        self.current_step += 1

    @staticmethod
    def generate_market_data(
        steps: int = 45,
        base_price: Decimal = Decimal("1.0"),
        volatility: Decimal = Decimal("0.03"),
        noise: Decimal = Decimal("0.02"),
    ) -> List[Tuple[Decimal, Decimal]]:
        """
        Generate simulated market data for two trading venues.

        This simulates realistic-looking price movements using a "random walk" model.
        In reality, you'd get prices from real exchange APIs.

        How it works:
        1. Start with a base price (e.g., $1.00 for XRP)
        2. Each step, the price changes randomly within the volatility range
        3. Add some noise to make it more realistic
        4. Create slightly different prices for two venues

        Args:
            steps: How many time points to generate (default: 45)
            base_price: Starting price of XRP in USD (default: $1.00)
            volatility: Max percentage price change per step (default: 3%)
            noise: Max random fluctuation to add (default: 2%)

        Returns:
            A list of (venue_a_price, venue_b_price) tuples for each time step

        Example:
            generate_market_data(steps=3) might return:
            [
                (Decimal("1.01"), Decimal("1.02")),  # Step 1
                (Decimal("0.99"), Decimal("0.98")),  # Step 2
                (Decimal("1.03"), Decimal("1.04")),  # Step 3
            ]
        """
        market_data = []  # List to store all the price data
        current_price = base_price  # Start at the base price

        # Generate prices for each time step
        for i in range(steps):
            # STEP 1: Calculate a random price change (can be positive or negative)
            # This simulates market movement
            # Formula: current_price * random_percentage_between(-volatility, +volatility)
            price_change = current_price * Decimal(
                random.uniform(-float(volatility), float(volatility))
            )

            # STEP 2: Add random noise to make it more realistic
            # Markets don't move smoothly - there's always random fluctuation
            noise_value = current_price * Decimal(
                random.uniform(-float(noise), float(noise))
            )

            # STEP 3: Update the price with both change and noise
            current_price += price_change + noise_value

            # STEP 4: Make sure price never goes negative or too low
            # In reality, crypto prices can't be negative!
            current_price = max(current_price, Decimal("0.01"))

            # STEP 5: Create slightly different prices for the two venues
            # Real exchanges always have small price differences - this creates arbitrage opportunities!
            venue_a_price = (
                current_price + Decimal(random.uniform(-0.01, 0.01))
            ).quantize(USD_PRECISION)

            venue_b_price = (
                current_price + Decimal(random.uniform(-0.01, 0.01))
            ).quantize(USD_PRECISION)

            # STEP 6: Add this time point to our market data
            market_data.append((venue_a_price, venue_b_price))

        return market_data
