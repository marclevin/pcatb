# Python Crypto Arbitrage Trading Bot - Educational Project

## 🎯 Project Overview

This is an **educational cryptocurrency arbitrage trading bot** designed to teach Python programming concepts through a real-world application. The bot simulates automated trading across two cryptocurrency exchanges, looking for profit opportunities.

### What is Arbitrage?
**Arbitrage** is the practice of buying an asset at a low price in one market and selling it at a higher price in another market to make a profit. 

**Real-world example:**
- You find Bitcoin selling for $40,000 on Exchange A
- The same Bitcoin sells for $40,200 on Exchange B
- You buy on Exchange A and sell on Exchange B
- Profit: $200 (minus trading fees)

### What This Bot Does
1. Monitors prices on two simulated exchanges
2. Detects profitable price differences
3. Automatically executes buy/sell trades
4. Tracks profit/loss and trading fees
5. Generates detailed reports

---

## 📖 What You'll Learn

This project demonstrates essential Python concepts:

### Core Python Concepts
- ✅ **Classes and Objects**: Organize code using object-oriented programming
- ✅ **Functions**: Break down complex tasks into reusable pieces
- ✅ **Dictionaries**: Store and manage data with key-value pairs
- ✅ **Lists**: Work with sequences of data
- ✅ **Loops**: Iterate through data and repeat actions
- ✅ **Conditionals**: Make decisions in code (if/elif/else)
- ✅ **Exception Handling**: Handle errors gracefully (try/except)
- ✅ **Type Hints**: Specify expected data types for clarity

### Advanced Concepts
- ✅ **TypedDict**: Define structured dictionary types
- ✅ **Decimal Numbers**: Handle money/currency precisely
- ✅ **Logging**: Track program behavior
- ✅ **Command Line Interfaces (CLI)**: Create user-friendly commands
- ✅ **File I/O**: Read from and write to files

### Software Design Patterns
- ✅ **Separation of Concerns**: Each file has a specific purpose
- ✅ **Encapsulation**: Data and methods grouped in classes
- ✅ **Code Reusability**: DRY (Don't Repeat Yourself) principle
- ✅ **Error Handling**: Defensive programming practices

---

## 🧠 Key Concepts Explained

### 1. Why Use `Decimal` Instead of `float`?

```python
# ❌ BAD: Using float for money
price = 0.1 + 0.2  # Result: 0.30000000000000004 (imprecise!)

# ✅ GOOD: Using Decimal for money
from decimal import Decimal
price = Decimal("0.1") + Decimal("0.2")  # Result: 0.3 (precise!)
```

**Why it matters:** Computers can't represent decimal numbers like 0.1 precisely in binary. For money, even tiny errors add up! `Decimal` gives us exact precision.

### 2. What are TypedDicts?

TypedDicts are dictionaries with specific keys and value types:

```python
from typing import TypedDict
from decimal import Decimal

class Wallet(TypedDict):
    usd: Decimal  # This wallet MUST have a 'usd' key with a Decimal value
    xrp: Decimal  # And MUST have an 'xrp' key with a Decimal value

# ✅ Valid wallet
my_wallet: Wallet = {"usd": Decimal("1000"), "xrp": Decimal("500")}

# ❌ Invalid - missing 'xrp' (your IDE will warn you!)
bad_wallet: Wallet = {"usd": Decimal("1000")}
```

**Benefits:**
- Auto-completion in your IDE
- Type checking catches errors before running code
- Self-documenting code (you can see what keys are expected)

### 3. Trading Fees Explained

Every exchange charges a fee for trades:

```python
# Example: Buy XRP with 0.1% fee
xrp_amount = Decimal("100")  # We want 100 XRP
price = Decimal("1.00")      # Price is $1.00 per XRP
fee_rate = Decimal("0.001")  # 0.1% = 0.001 in decimal

# Calculate cost WITH fee
cost_without_fee = xrp_amount * price  # $100.00
fee_amount = cost_without_fee * fee_rate  # $0.10
total_cost = cost_without_fee + fee_amount  # $100.10

# Simpler formula
total_cost = xrp_amount * price * (1 + fee_rate)  # $100.10
```

### 4. How Arbitrage Becomes Profitable

For arbitrage to be profitable, the price difference must exceed the combined fees:

```python
# Venue A: Price = $1.00, Fee = 0.1%
buy_cost = Decimal("1.00") * (1 + Decimal("0.001"))  # $1.001

# Venue B: Price = $1.02, Fee = 0.2%
sell_revenue = Decimal("1.02") * (1 - Decimal("0.002"))  # $1.01796

# Profit per XRP
profit = sell_revenue - buy_cost  # $1.01796 - $1.001 = $0.01696
profit_percentage = (profit / buy_cost) * 100  # 1.69% profit!
```

---

## 🚀 Installation

### Prerequisites
- Python via Conda
- pip (Python package installer)
- Command line / terminal access

### Step 1: Clone or Download the Project
```bash
# If using git
git clone # fill in after publish
cd pcatb
```

### Step 2: Create a Virtual Environment (Recommended)

**Using conda:**
```bash
conda create -n trading-bot python
conda activate trading-bot
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `click` - For creating command-line interfaces
- `loguru` - For easy and beautiful logging
- `black` - For code formatting (optional)

---

## 🎮 How to Run

### Basic Usage

**Run the trading bot simulation:**
```bash
python trading.py execute-trades
```

This starts a simulation with default settings:
- Starting capital: $10,000
- Trading steps: 45

### Custom Settings

**Change starting capital:**
```bash
python trading.py execute-trades --capital 5000
```

**Change number of trading steps:**
```bash
python trading.py execute-trades --steps 100
```

**Combine both:**
```bash
python trading.py execute-trades --capital 20000 --steps 200
```

### Other Commands

**Clear the log file:**
```bash
python trading.py clear-logs
```

**Get help:**
```bash
python trading.py --help
python trading.py execute-trades --help
```

### Understanding the Output

When you run the bot, you'll see:

```
🤖 Starting Trading Bot Simulation
💵 Starting capital: $10,000.00
⏱️  Trading steps: 45
------------------------------------------------------------
📊 Generating market data...
✅ Generated 45 price points
------------------------------------------------------------
🚀 Running arbitrage strategy...
[... trading activity ...]
============================================================
📊 TRADING SUMMARY
============================================================
📈 PnL: $156.34
🔄 Trades executed: 23
💸 Total fees paid: $45.12
💵 Final USD: $10,100.00
🪙 Final XRP: 15.234567
============================================================
✅ Session complete! Check trading.log for details.
```

**Check the log file** (`trading.log`) for detailed information about each trade!

---

## 📁 Project Structure

```
pcatb/
│
├── models.py          # Data structures (Wallet, Trade, TradeResult)
├── venue.py           # Trading venue/exchange simulation
├── bot.py             # The trading bot logic
├── trading.py         # Command-line interface (CLI)
├── requirements.txt   # Python dependencies
├── README.md          # This file!
└── trading.log        # Generated log file (after running)
```

### File Descriptions

#### `models.py` - Data Structures
Defines the "blueprints" for our data:
- `Wallet`: Stores USD and XRP balances
- `Trade`: Represents a buy or sell instruction
- `TradeResult`: Records what happened after a trade
- Constants for decimal precision

**Key Learning:** TypedDict, Decimal, type hints

#### `venue.py` - Trading Venue
Simulates a cryptocurrency exchange:
- Manages price history
- Executes trades (buy/sell)
- Calculates fees
- Generates simulated market data

**Key Learning:** Classes, methods, exception handling, static methods

#### `bot.py` - Trading Bot
The "brain" of the operation:
- Monitors two venues for price differences
- Detects arbitrage opportunities
- Executes trades automatically
- Tracks performance (PnL, fees, trades)

**Key Learning:** Object-oriented programming, business logic, calculations

#### `trading.py` - Command Line Interface
The entry point for users:
- Parses command-line arguments
- Sets up the simulation
- Runs the trading loop
- Displays results

**Key Learning:** CLI design with Click, user interaction, program flow

---

## 🔍 How It Works

### Step-by-Step Execution Flow

1. **Initialization**
   - Create two trading venues with different fees
   - Generate simulated price data
   - Create a trading bot with starting capital

2. **Trading Loop** (repeats for each time step)
   ```
   For each time step:
   ├─ Get current prices from both venues
   ├─ Check: Is there an arbitrage opportunity?
   │  ├─ If YES:
   │  │  ├─ Buy XRP on cheaper venue
   │  │  ├─ Sell XRP on expensive venue
   │  │  └─ Record profit and fees
   │  └─ If NO:
   │     └─ Wait and check next time step
   └─ Move to next time step
   ```

3. **Results**
   - Calculate total profit/loss
   - Display summary
   - Save detailed log

### Arbitrage Detection Logic

```python
# Simplified arbitrage detection
price_a = venue_a.get_current_price()  # e.g., $1.00
price_b = venue_b.get_current_price()  # e.g., $1.02
fee_a = venue_a.get_fee()              # e.g., 0.001 (0.1%)
fee_b = venue_b.get_fee()              # e.g., 0.002 (0.2%)

# Check if buying on A and selling on B is profitable
buy_price_with_fee = price_a * (1 + fee_a)      # $1.001
sell_price_after_fee = price_b * (1 - fee_b)    # $1.01796

if buy_price_with_fee < sell_price_after_fee:
    # Profitable! Execute the arbitrage
    buy_on_venue_a()
    sell_on_venue_b()
```

---

## 💻 Code Walkthrough

### Example 1: Creating a Wallet

```python
from decimal import Decimal
from models import Wallet

# Create a wallet with $1000 USD and 0 XRP
my_wallet: Wallet = {
    "usd": Decimal("1000.00"),
    "xrp": Decimal("0")
}

# Access balances
print(f"USD Balance: ${my_wallet['usd']}")  # USD Balance: $1000.00
print(f"XRP Balance: {my_wallet['xrp']}")   # XRP Balance: 0

# Update balances
my_wallet["usd"] -= Decimal("100")  # Spend $100
my_wallet["xrp"] += Decimal("50")   # Receive 50 XRP
```

### Example 2: Executing a Trade

```python
from decimal import Decimal
from models import Trade, Wallet
from venue import TradingVenue

# Create a venue
venue = TradingVenue(name="Test Exchange", fee=Decimal("0.001"))
venue.price_history = [Decimal("1.00")]  # Set price to $1.00

# Create a wallet
wallet: Wallet = {"usd": Decimal("1000"), "xrp": Decimal("0")}

# Create a buy trade for $100 worth of XRP
trade = Trade(action="buy", amount=Decimal("100"))

# Execute the trade
result = venue.execute_trade(trade, wallet)

# Check the result
if result["success"]:
    print(f"Trade successful!")
    print(f"USD changed by: ${result['usd_change']}")
    print(f"XRP changed by: {result['xrp_change']}")
    print(f"Fee paid: ${result['fee_paid']}")
else:
    print(f"Trade failed: {result['note']}")
```

### Example 3: Running the Bot

```python
from decimal import Decimal
from bot import TradingBot
from venue import TradingVenue

# Set up venues
venue_a = TradingVenue("Venue A", Decimal("0.001"))
venue_b = TradingVenue("Venue B", Decimal("0.002"))

# Generate and load market data
market_data = TradingVenue.generate_market_data(steps=10)
for price_a, price_b in market_data:
    venue_a.price_history.append(price_a)
    venue_b.price_history.append(price_b)

# Create bot
bot = TradingBot(
    name="MyBot",
    starting_capital=Decimal("10000"),
    venue_a=venue_a,
    venue_b=venue_b
)

# Run for each time step
for step in range(len(market_data)):
    bot.run_arbitrage()
    venue_a.tick()
    venue_b.tick()

# Check results
pnl = bot.calculate_pnl()
print(f"Profit/Loss: ${pnl}")
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue: "ModuleNotFoundError: No module named 'click'"
**Solution:** You haven't installed the dependencies.
```bash
pip install -r requirements.txt
```

#### Issue: "Not enough USD in wallet to execute trade"
**Solution:** This is expected if:
- You set starting capital too low
- Trades are too large
- Too many fees have been paid

Try increasing starting capital:
```bash
python trading.py execute-trades --capital 20000
```

#### Issue: "No price history set for trading venue"
**Solution:** This happens if you manually create venues without setting prices. The `execute_trades` command handles this automatically.

#### Issue: Log file is huge
**Solution:** Clear the log file before running:
```bash
python trading.py clear-logs
python trading.py execute-trades
```

#### Issue: "Price goes negative in simulation"
**Solution:** This shouldn't happen (there's a safety check), but if it does, reduce volatility in `TradingVenue.generate_market_data()`.

### Getting Help

1. **Read the error message carefully** - Python error messages tell you:
   - What went wrong
   - Which file has the problem
   - Which line number

2. **Use print statements** - Add `print()` to see what values variables have:
   ```python
   print(f"Current price: {price}")
   print(f"Wallet balance: {wallet}")
   ```

3. **Check the log file** - `trading.log` contains detailed information about what the bot did

4. **Use a debugger** - VS Code and other IDEs let you step through code line by line

---

## 📚 Additional Resources

### Python Concepts
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python - Classes and Objects](https://realpython.com/python3-object-oriented-programming/)
- [Decimal Module Documentation](https://docs.python.org/3/library/decimal.html)

### Trading Concepts
- [What is Arbitrage?](https://www.investopedia.com/terms/a/arbitrage.asp)
- [Understanding Trading Fees](https://www.investopedia.com/terms/t/transactioncosts.asp)
- [Cryptocurrency Basics](https://www.investopedia.com/terms/c/cryptocurrency.asp)

### Tools Used
- [Click Documentation](https://click.palletsprojects.com/)
- [Loguru Documentation](https://loguru.readthedocs.io/)

---

Happy coding! 🚀
