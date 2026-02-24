"""
trading.py - Command Line Interface (CLI) for the Trading Bot

This file provides a command-line interface to run the trading bot.
You can use commands like "python trading.py execute-trades" to run the bot.

What is a CLI?
- CLI = Command Line Interface
- It allows you to interact with programs using text commands
- Instead of clicking buttons, you type commands like "execute-trades"

This file uses the "click" library to make creating CLIs easy.

Key concepts for beginners:
- @click.group() creates a group of commands
- @click.command() creates a specific command
- @click.option() adds flags like --capital 5000
"""

import os
from decimal import Decimal
import click
from loguru import logger

# Import our custom modules
from bot import TradingBot
from venue import TradingVenue

# ==============================================================================
# CLI SETUP
# ==============================================================================


@click.group()
def cli():
    """
    Main CLI group for the trading bot.

    This is the entry point for all commands.
    Commands are defined below using @cli.command()
    """
    pass


# ==============================================================================
# COMMAND: Execute Trades
# ==============================================================================


@cli.command()
@click.option(
    "--capital",
    default=10000,
    type=float,
    help="Starting capital in USD (default: $10,000)",
)
@click.option(
    "--steps",
    default=45,
    type=int,
    help="Number of trading time steps to simulate (default: 45)",
)
def execute_trades(capital, steps):
    """
    Run the arbitrage trading bot simulation.

    This command:
    1. Sets up two simulated trading venues with different fees
    2. Generates realistic market data (price movements over time)
    3. Creates a trading bot with starting capital
    4. Runs the bot through all time steps, looking for arbitrage
    5. Shows a summary of performance

    Examples:
        python trading.py execute-trades
        python trading.py execute-trades --capital 5000 --steps 100
    """
    # STEP 1: Set up logging
    # This saves all trading activity to a file for later review
    logger.add(
        "trading.log",
        rotation="1 MB",  # Create new log file when current one reaches 1 MB
        level="SUCCESS",  # Log successes and errors (not just info)
    )

    # STEP 2: Display startup information to user
    click.echo(click.style("🤖 Starting Trading Bot Simulation", fg="cyan", bold=True))
    click.echo(f"💵 Starting capital: ${capital:,.2f}")
    click.echo(f"⏱️  Trading steps: {steps}")
    click.echo("-" * 60)

    # STEP 3: Create two trading venues with different fee structures
    # Real exchanges have different fees - this creates arbitrage opportunities!
    venue_a = TradingVenue(name="Venue A", fee=Decimal("0.001"))  # 0.1% trading fee
    venue_b = TradingVenue(
        name="Venue B", fee=Decimal("0.002")  # 0.2% trading fee (higher than Venue A)
    )

    # STEP 4: Generate simulated market data
    # This creates realistic price movements for both venues
    click.echo("📊 Generating market data...")
    market_data = TradingVenue.generate_market_data(steps=steps)

    # STEP 5: Load the price history into both venues
    # Each venue gets slightly different prices (this is realistic!)
    for price_a, price_b in market_data:
        venue_a.price_history.append(price_a)
        venue_b.price_history.append(price_b)

    click.echo(f"✅ Generated {len(market_data)} price points")
    click.echo("-" * 60)

    # STEP 6: Create the trading bot
    trading_bot = TradingBot(
        name="ArbitrageBot",
        starting_capital=Decimal(str(capital)),  # Convert float to Decimal
        venue_a=venue_a,
        venue_b=venue_b,
    )

    click.echo("🚀 Running arbitrage strategy...")

    # STEP 7: Run the trading loop
    # For each time step:
    # - Check for arbitrage opportunities
    # - Execute trades if profitable
    # - Move to next time step
    for step in range(len(market_data)):
        logger.info(f"{'='*20} Step {step + 1}/{len(market_data)} {'='*20}")

        # Run the arbitrage strategy for this time step
        trading_bot.run_arbitrage()

        # Move both venues to the next time step
        venue_a.tick()
        venue_b.tick()

    logger.info("=" * 60)
    logger.info("Trading session completed")
    logger.info("=" * 60)

    # STEP 8: Calculate and display results
    pnl = trading_bot.calculate_pnl()  # Calculate profit/loss

    # Display a nice summary to the console
    click.echo("\n" + "=" * 60)
    click.echo(click.style("📊 TRADING SUMMARY", fg="green", bold=True))
    click.echo("=" * 60)

    # Color the PnL green if profit, red if loss
    pnl_color = "green" if pnl >= 0 else "red"
    pnl_symbol = "📈" if pnl >= 0 else "📉"

    click.echo(
        f"{pnl_symbol} PnL: {click.style(f'${pnl:,.2f}', fg=pnl_color, bold=True)}"
    )
    click.echo(f"🔄 Trades executed: {trading_bot.trade_count}")
    click.echo(f"💸 Total fees paid: ${trading_bot.total_fees_paid:,.2f}")
    click.echo(f"💵 Final USD: ${trading_bot.wallet['usd']:,.2f}")
    click.echo(f"💵 Final XRP: {trading_bot.wallet['xrp']:,.6f}")
    click.echo("=" * 60)
    click.echo(
        click.style("✅ Session complete! Check trading.log for details.", fg="cyan")
    )


# ==============================================================================
# COMMAND: Clear Logs
# ==============================================================================


@cli.command()
def clear_logs():
    """
    Delete the trading log file.

    Use this to clear old logs before starting a new trading session.

    Example:
        python trading.py clear-logs
    """
    log_file = "trading.log"

    # Check if the log file exists
    if os.path.exists(log_file):
        # Delete the file
        os.remove(log_file)
        click.echo(click.style(f"✅ Cleared {log_file}", fg="green"))
    else:
        # File doesn't exist - nothing to delete
        click.echo(click.style(f"ℹ️  No log file found ({log_file})", fg="yellow"))


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    """
    Entry point when running this script directly.

    When you run: python trading.py execute-trades
    Python executes this block, which starts the CLI.
    """
    cli()
