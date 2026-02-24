"""
bot.py - The Trading Bot (Brain of the Operation)

This file contains the TradingBot class, which is the "brain" of our trading system.
The bot looks for arbitrage opportunities and executes trades automatically.

What is Arbitrage?
- Arbitrage is buying something cheap in one place and selling it expensive in another
- Example: Buy XRP for $1.00 on Venue A, sell for $1.05 on Venue B = $0.05 profit!
- In real markets, these opportunities are small and disappear quickly

Key concepts for beginners:
- The bot monitors two exchanges looking for price differences
- When a profitable opportunity exists, it executes trades
- It keeps track of its wallet, fees paid, and profit/loss
"""

from decimal import Decimal
from loguru import logger

# Import our custom modules
from venue import TradingVenue
from models import Trade, Wallet, TradeResult, USD_PRECISION, XRP_PRECISION

# ==============================================================================
# TRADING BOT CLASS
# ==============================================================================


class TradingBot:
    """
    An automated bot that looks for arbitrage opportunities and executes trades.

    The bot watches two trading venues (exchanges) and looks for price differences.
    When it finds a profitable opportunity, it automatically:
    1. Buys XRP on the cheaper exchange
    2. Sells XRP on the more expensive exchange
    3. Keeps the profit (minus fees)

    Attributes:
        name: The bot's name (e.g., "ArbitrageBot")
        wallet: The bot's wallet containing USD and XRP
        venue_a: First trading venue to monitor
        venue_b: Second trading venue to monitor
        starting_capital: How much USD we started with
        trade_count: Number of successful trades executed
        total_fees_paid: Total fees paid across all trades
    """

    def __init__(
        self,
        name: str,
        starting_capital: Decimal,
        venue_a: TradingVenue,
        venue_b: TradingVenue,
    ):
        """
        Initialize a new trading bot.

        Args:
            name: Name for this bot (e.g., "ArbitrageBot")
            starting_capital: Starting amount of USD to trade with
            venue_a: First trading venue (exchange) to monitor
            venue_b: Second trading venue (exchange) to monitor
        """
        self.name = name

        # Create a wallet starting with USD and no XRP
        self.wallet: Wallet = {"usd": starting_capital, "xrp": Decimal("0")}

        # Save the two venues we'll be trading on
        self.venue_a = venue_a
        self.venue_b = venue_b

        # Track performance metrics
        self.starting_capital = starting_capital
        self.trade_count = 0
        self.total_fees_paid = Decimal("0")

    def get_wallet(self) -> Wallet:
        """
        Get the current wallet state.

        Returns:
            The bot's wallet with current USD and XRP balances
        """
        return self.wallet

    def run_arbitrage(self):
        """
        Look for arbitrage opportunities and execute trades if profitable.

        This is the main logic of the bot! It:
        1. Gets current prices from both venues
        2. Checks if there's a profitable price difference (after fees)
        3. If yes, executes a buy on the cheap venue and sell on the expensive one

        Arbitrage Example:
        - Venue A: XRP costs $1.00 (0.1% fee)
        - Venue B: XRP sells for $1.05 (0.2% fee)
        - Buy cost: $1.00 * 1.001 = $1.001
        - Sell revenue: $1.05 * 0.998 = $1.0479
        - Profit per XRP: $1.0479 - $1.001 = $0.0469 (4.69%)
        """
        # STEP 1: Get current prices from both venues
        price_a = self.venue_a.get_current_price()
        price_b = self.venue_b.get_current_price()

        # STEP 2: Get the trading fees from both venues
        # Fees are expressed as decimals (e.g., 0.001 = 0.1%)
        fee_a = self.venue_a.get_fee()
        fee_b = self.venue_b.get_fee()

        # STEP 3: Determine how much to trade
        # We trade 5% of our USD balance, but cap it at $1000 for safety
        # This prevents us from risking too much on a single trade
        amount_to_trade = min(
            self.wallet["usd"] * Decimal("0.05"),  # 5% of balance
            Decimal("1000"),  # Maximum $1000
        ).quantize(USD_PRECISION)

        # STEP 4: Check for arbitrage opportunities
        # We need to account for fees when checking profitability!

        # Opportunity 1: Buy on Venue A, Sell on Venue B
        # Check if: (buy price with fee) < (sell price after fee)
        buy_price_a_with_fee = price_a * (1 + fee_a)
        sell_price_b_after_fee = price_b * (1 - fee_b)

        if buy_price_a_with_fee < sell_price_b_after_fee:
            # Found an opportunity! Buy cheap on A, sell expensive on B
            logger.info(
                f"{self.name}: 💰 Arbitrage found! "
                f"Buy on {self.venue_a.name} at ${price_a}, "
                f"Sell on {self.venue_b.name} at ${price_b}"
            )

            # Execute the arbitrage trade
            result = self.buy_xrp(amount_to_trade, self.venue_a)
            self.handle_trade_result(result)

            result = self.sell_xrp(amount_to_trade, self.venue_b)
            self.handle_trade_result(result)

        # Opportunity 2: Buy on Venue B, Sell on Venue A
        # Check if: (buy price with fee) < (sell price after fee)
        else:
            buy_price_b_with_fee = price_b * (1 + fee_b)
            sell_price_a_after_fee = price_a * (1 - fee_a)

            if buy_price_b_with_fee < sell_price_a_after_fee:
                # Found an opportunity! Buy cheap on B, sell expensive on A
                logger.info(
                    f"{self.name}: 💰 Arbitrage found! "
                    f"Buy on {self.venue_b.name} at ${price_b}, "
                    f"Sell on {self.venue_a.name} at ${price_a}"
                )

                # Execute the arbitrage trade
                result = self.buy_xrp(amount_to_trade, self.venue_b)
                self.handle_trade_result(result)

                result = self.sell_xrp(amount_to_trade, self.venue_a)
                self.handle_trade_result(result)
            else:
                # No profitable opportunity right now
                logger.info(
                    f"{self.name}: No arbitrage opportunity "
                    f"(Venue A: ${price_a}, Venue B: ${price_b})"
                )

    def handle_trade_result(self, result: TradeResult):
        """
        Process the result of a trade and update bot statistics.

        After executing a trade, we need to:
        - Check if it succeeded
        - Update our trade counter
        - Track fees paid
        - Log what happened

        Args:
            result: The TradeResult from executing a trade
        """
        if result["success"]:
            # Trade succeeded! Log it and update statistics
            logger.success(
                f"{self.name}: ✅ Trade successful! "
                f"USD change: ${result['usd_change']}, "
                f"XRP change: {result['xrp_change']}, "
                f"Fee: ${result['fee_paid']}"
            )

            # Update our statistics
            self.trade_count += 1
            self.total_fees_paid += result["fee_paid"]
        else:
            # Trade failed - no changes were made to the wallet
            logger.warning(
                f"{self.name}: ⚠️ Trade failed! " f"Reason: {result['note']}"
            )

    def buy_xrp(self, amount: Decimal, venue: TradingVenue) -> TradeResult:
        """
        Buy XRP using USD at the specified venue.

        This method:
        1. Creates a "buy" trade instruction
        2. Sends it to the venue to execute
        3. Returns the result

        Args:
            amount: How much USD worth of XRP to buy
            venue: Which exchange to buy from

        Returns:
            TradeResult indicating success/failure and what changed
        """
        # Create the trade instruction
        trade = Trade(action="buy", amount=amount)

        # Log what we're attempting
        logger.info(
            f"{self.name}: 🛒 Attempting to buy XRP worth ${amount} "
            f"on {venue.name} at ${venue.get_current_price()}"
        )

        # Execute the trade at the venue
        result = venue.execute_trade(trade, self.wallet)
        return result

    def sell_xrp(self, amount: Decimal, venue: TradingVenue) -> TradeResult:
        """
        Sell XRP to get USD at the specified venue.

        This method:
        1. Creates a "sell" trade instruction
        2. Sends it to the venue to execute
        3. Returns the result

        Args:
            amount: How much USD worth of XRP to sell
            venue: Which exchange to sell on

        Returns:
            TradeResult indicating success/failure and what changed
        """
        # Create the trade instruction
        trade = Trade(action="sell", amount=amount)

        # Log what we're attempting
        logger.info(
            f"{self.name}: 💵 Attempting to sell XRP worth ${amount} "
            f"on {venue.name} at ${venue.get_current_price()}"
        )

        # Execute the trade at the venue
        result = venue.execute_trade(trade, self.wallet)
        return result

    def calculate_pnl(self) -> Decimal:
        """
        Calculate the bot's current Profit and Loss (PnL).

        PnL tells us if we're making or losing money.

        How it works:
        1. Calculate total current value (USD + value of XRP holdings)
        2. Compare to starting capital
        3. Positive = profit, Negative = loss

        Note: We value our XRP at the last known price from Venue A

        Returns:
            PnL in USD (positive = profit, negative = loss)

        Example:
            - Started with: $10,000
            - Now have: $9,500 USD + 600 XRP
            - XRP price: $1.00
            - Current value: $9,500 + (600 * $1.00) = $10,100
            - PnL: $10,100 - $10,000 = +$100 profit!
        """
        # Calculate the value of our XRP holdings in USD
        xrp_value_usd = self.wallet["xrp"] * self.venue_a.get_last_price()

        # Calculate total current value
        current_value = self.wallet["usd"] + xrp_value_usd

        # Calculate profit/loss
        pnl = current_value - self.starting_capital

        return pnl

    def generate_report(self):
        """
        Generate and log a detailed performance report for the bot.

        This creates a nicely formatted summary of:
        - Current profit/loss
        - Number of trades executed
        - Total fees paid
        - Final wallet balances
        """
        # Get current profit/loss
        pnl = self.calculate_pnl()

        # Create a formatted report
        report = f"""
{'='*60}
{self.name} - Performance Report
{'='*60}
Current PnL:           ${pnl.quantize(USD_PRECISION)}
Trades Executed:       {self.trade_count}
Total Fees Paid:       ${self.total_fees_paid.quantize(USD_PRECISION)}
Final USD Balance:     ${self.wallet['usd'].quantize(USD_PRECISION)}
Final XRP Balance:     {self.wallet['xrp'].quantize(XRP_PRECISION)}
{'='*60}
        """

        # Log the report
        logger.info(report)
