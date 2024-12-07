import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import streamlit as st

# Fetch data from Yahoo Finance
def fetch_yahoo_data(ticker, period="5D", interval="1m"):
    data = yf.download(ticker, period=period, interval=interval)
    return data

# Calculate extreme ranges
def calculate_extreme_ranges(data, probabilities):
    close_prices = data['Close'].dropna()
    results = {
        "Probability": [],
        "Bottom Extreme (Min to A)": [],
        "Top Extreme (B to Max)": [],
    }

    for prob in probabilities:
        lower_percentile = prob * 100
        upper_percentile = 100 - (prob * 100)

        A = np.percentile(close_prices, lower_percentile)
        B = np.percentile(close_prices, upper_percentile)

        results["Probability"].append(f"{int(prob * 100)}%")
        results["Bottom Extreme (Min to A)"].append(f"{close_prices.min()} to {A}")
        results["Top Extreme (B to Max)"].append(f"{B} to {close_prices.max()}")

    return pd.DataFrame(results)

# Calculate potential profit with eToro fees
def calculate_potential_profit_with_fees(results_df, investment_amount, blockchain_fee=0, tax_rate=0):
    lower_bounds = [float(range_str.split(' to ')[1]) for range_str in results_df["Bottom Extreme (Min to A)"]]
    upper_bounds = [float(range_str.split(' to ')[0]) for range_str in results_df["Top Extreme (B to Max)"]]

    buy_price = max(lower_bounds)
    sell_price = min(upper_bounds)

    # Apply eToro fees (1% for buy and sell)
    buy_price_with_fee = buy_price * 1.01
    sell_price_with_fee = sell_price * 0.99

    units_purchased = investment_amount / buy_price_with_fee
    total_revenue = units_purchased * sell_price_with_fee
    profit = total_revenue - investment_amount - blockchain_fee

    tax = profit * tax_rate / 100
    profit_after_tax = profit - tax

    return buy_price_with_fee, sell_price_with_fee, profit_after_tax, tax

# Interactive Streamlit App
def main():
    st.title("Interactive Trading Profit Calculator")
    st.sidebar.header("Input Parameters")

    # User inputs
    ticker = st.sidebar.text_input("Enter Ticker (e.g., BTC-USD, AAPL)", "BTC-USD")
    investment_amount = st.sidebar.number_input("Investment Amount (in USD)", value=1000.0)
    blockchain_fee = st.sidebar.number_input("Blockchain Fee (in USD)", value=0.0)
    tax_rate = st.sidebar.slider("Tax Rate (%)", min_value=0, max_value=50, value=0)

    # Fetch and display data
    data = fetch_yahoo_data(ticker, period="5D", interval="1m")
    if data.empty:
        st.warning("No data found for the specified ticker. Please try another one.")
        return

    st.write(f"### Historical Close Prices for {ticker}")
    st.line_chart(data['Close'])

    # Calculate extreme ranges
    probabilities = [0.1, 0.2, 0.3]  # Probabilities for extreme regions
    results_df = calculate_extreme_ranges(data, probabilities)

    st.write("### Extreme Ranges")
    st.table(results_df)

    # Calculate potential profit
    buy_price, sell_price, profit, tax = calculate_potential_profit_with_fees(
        results_df, investment_amount, blockchain_fee, tax_rate
    )

    # Display profit calculation
    st.write("### Profit Calculation")
    st.write(f"**Buy Price (with fees):** ${buy_price:.2f}")
    st.write(f"**Sell Price (with fees):** ${sell_price:.2f}")
    st.write(f"**Tax:** ${tax:.2f}")
    st.write(f"**Potential Profit (after tax):** ${profit:.2f}")

    # Download results
    csv = results_df.to_csv(index=False)
    st.download_button(label="Download Extreme Ranges as CSV", data=csv, file_name="extreme_ranges.csv")

if __name__ == "__main__":
    main()
