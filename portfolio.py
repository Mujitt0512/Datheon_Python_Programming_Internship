import csv
import sys

DATASET_FILENAME = "Data2.csv"
OUTPUT_FILENAME = "portfolio_summary.csv"

def load_market_data(filename):
    """Loads tickers and company details directly from the dataset file."""
    market_data = {}
    try:
        with open(filename, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                ticker = row.get("Symbol", "").strip().upper()
                security = row.get("Security", "").strip()
                sector = row.get("GICS Sector", "").strip()
                if ticker:
                    market_data[ticker] = {
                        "security": security,
                        "sector": sector
                    }
        print(f"[+] Successfully loaded {len(market_data)} records from '{filename}'.")
    except FileNotFoundError:
        print(f"[!] Error: Could not find '{filename}' in the directory. Please ensure the dataset file is included.")
        sys.exit(1)
    return market_data

def get_portfolio_positions(market_data):
    """Interactively collects stock positions and validates against the loaded dataset."""
    positions = []
    print("\n" + "=" * 42)
    print("    STOCK PORTFOLIO PERFORMANCE TRACKER ")
    print("=" * 42)
    print("Enter your holdings. Type 'DONE' when you are finished.\n")

    while True:
        ticker = input("Enter Stock Ticker (e.g., AAPL): ").strip().upper()
        if ticker == 'DONE':
            break
        if not ticker:
            print("[!] Ticker cannot be empty. Please try again.\n")
            continue

        if ticker not in market_data:
            print(f"[!] Warning: '{ticker}' was not found in the loaded dataset file.")
        else:
            company_name = market_data[ticker]["security"]
            sector = market_data[ticker]["sector"]
            print(f"    -> Found: {company_name} ({sector})")

        try:
            shares = float(input(f"Enter quantity of shares for {ticker}: "))
            buy_price = float(input(f"Enter average buy price per share for {ticker} ($): "))
            if shares <= 0 or buy_price < 0:
                print("[!] Shares must be greater than 0 and buy price cannot be negative.\n")
                continue
        except ValueError:
            print("[!] Invalid numeric input. Please enter valid numbers for shares and price.\n")
            continue

        positions.append({
            "ticker": ticker,
            "shares": shares,
            "buy_price": buy_price
        })
        print(f"[+] Added {ticker} to portfolio.\n")

    return positions

def calculate_and_export_performance(positions, output_filename=OUTPUT_FILENAME):
    """Calculates total invested capital vs current market value and exports to CSV."""
    summary_data = []
    total_invested = 0.0
    total_current_val = 0.0

    print("\n" + "=" * 78)
    print(f"{'TICKER':<8} {'SHARES':<10} {'BUY ($)':<10} {'CURRENT ($)':<12} {'VAL ($)':<12} {'GAIN/LOSS (%)':<12}")
    print("=" * 78)

    for pos in positions:
        ticker = pos["ticker"]
        shares = pos["shares"]
        buy_price = pos["buy_price"]

        # Simulated real-time valuation check (assumes a 5% baseline growth offset for calculation demo)
        current_price = round(buy_price * 1.05, 2)

        # 1. Calculate total invested capital and current market value per asset
        cost_basis = shares * buy_price
        market_value = shares * current_price
        gain_loss_percent = ((current_price - buy_price) / buy_price) * 100 if buy_price > 0 else 0.0

        # Accumulate portfolio totals
        total_invested += cost_basis
        total_current_val += market_value

        print(f"{ticker:<8} {shares:<10.2f} {buy_price:<10.2f} {current_price:<12.2f} {market_value:<12.2f} {gain_loss_percent:>+10.2f}%")

        summary_data.append({
            "Ticker": ticker,
            "Shares": shares,
            "Buy_Price": buy_price,
            "Current_Price": current_price,
            "Total_Invested": round(cost_basis, 2),
            "Market_Value": round(market_value, 2),
            "Gain_Loss_Percent": round(gain_loss_percent, 2)
        })

    print("=" * 78)
    net_gain_loss = total_current_val - total_invested
    net_gain_loss_pct = ((total_current_val - total_invested) / total_invested * 100) if total_invested > 0 else 0.0
    
    print(f"Total Invested Capital: ${total_invested:,.2f}")
    print(f"Total Current Value:    ${total_current_val:,.2f}")
    print(f"Net Portfolio Return:   ${net_gain_loss:+,.2f} ({net_gain_loss_pct:+.2f}%)")
    print("=" * 78 + "\n")

    # 2. Write results into 'portfolio_summary.csv' using Python's built-in csv module
    fieldnames = ["Ticker", "Shares", "Buy_Price", "Current_Price", "Total_Invested", "Market_Value", "Gain_Loss_Percent"]
    
    try:
        with open(output_filename, mode="w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in summary_data:
                writer.writerow(row)
        print(f"[+] Successfully exported summary to '{output_filename}'.")
    except IOError as e:
        print(f"[!] Error writing to CSV file: {e}")

def main():
    market_data = load_market_data(DATASET_FILENAME)
    positions = get_portfolio_positions(market_data)
    
    if not positions:
        print("[!] No positions recorded. Exiting application.")
        sys.exit(0)
    
    calculate_and_export_performance(positions)

if __name__ == "__main__":
    main()