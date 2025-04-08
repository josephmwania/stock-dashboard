import yfinance as yf
import pandas as pd
import sqlite3

# Download stock data
stocks = ['AAPL', 'MSFT']
start_date = '2020-01-01'
end_date = '2021-01-01'

# Download data
data = {stock: yf.download(stock, start=start_date, end=end_date) for stock in stocks}

# Clean the data
for stock, df in data.items():
    # We only need the 'Close' price for comparison
    df = df[['Close']]  
    # Drop any rows with missing values (in case there are gaps in data)
    df.dropna(inplace=True)
    # Reset the index to use Date as a column
    df.reset_index(inplace=True)
    # Rename columns for easier access
    df.columns = ['Date', f'{stock}_Close']
    data[stock] = df

# Show cleaned data
for stock, df in data.items():
    print(f"{stock} cleaned data:")
    print(df.head())
    print("\n")
# Create a connection to the SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('stock_prices.db')

# Store the data in SQLite database
for stock, df in data.items():
    df.to_sql(stock, conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print("Data has been stored in SQLite!")
# Reconnect to the database
conn = sqlite3.connect('stock_prices.db')

# Read data back into pandas to confirm
query = "SELECT * FROM AAPL LIMIT 5"
aapl_data = pd.read_sql(query, conn)

print(aapl_data.head())

# Close the connection
conn.close()
# Reconnect to the SQLite database to fetch data
conn = sqlite3.connect('stock_prices.db')

# Read data from SQLite into pandas DataFrame
aapl_data = pd.read_sql("SELECT * FROM AAPL", conn)
msft_data = pd.read_sql("SELECT * FROM MSFT", conn)

# Close the connection
conn.close()

# Calculate daily returns
aapl_data['AAPL_Return'] = aapl_data['AAPL_Close'].pct_change() * 100
msft_data['MSFT_Return'] = msft_data['MSFT_Close'].pct_change() * 100

# Drop the first row as it will have NaN value due to pct_change()
aapl_data.dropna(inplace=True)
msft_data.dropna(inplace=True)

# Show the data with returns
print(aapl_data[['Date', 'AAPL_Close', 'AAPL_Return']].head())
print(msft_data[['Date', 'MSFT_Close', 'MSFT_Return']].head())

import matplotlib.pyplot as plt
import seaborn as sns

# Set up the plot
plt.figure(figsize=(14, 7))

# Plot closing prices for AAPL and MSFT
sns.lineplot(x='Date', y='AAPL_Close', data=aapl_data, label='Apple (AAPL)', color='blue')
sns.lineplot(x='Date', y='MSFT_Close', data=msft_data, label='Microsoft (MSFT)', color='orange')

# Set plot labels and title
plt.title('Stock Price Trends: Apple vs Microsoft (2020)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Closing Price (USD)', fontsize=14)
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
plt.figure(figsize=(14, 7))

# Plot daily returns for AAPL and MSFT
sns.lineplot(x='Date', y='AAPL_Return', data=aapl_data, label='Apple (AAPL) Returns', color='blue')
sns.lineplot(x='Date', y='MSFT_Return', data=msft_data, label='Microsoft (MSFT) Returns', color='orange')

# Set plot labels and title
plt.title('Daily Returns: Apple vs Microsoft (2020)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Daily Returns (%)', fontsize=14)
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Calculate cumulative returns
aapl_data['AAPL_CumReturn'] = (1 + aapl_data['AAPL_Return'] / 100).cumprod() - 1
msft_data['MSFT_CumReturn'] = (1 + msft_data['MSFT_Return'] / 100).cumprod() - 1

# Plot cumulative returns
plt.figure(figsize=(14, 7))

sns.lineplot(x='Date', y='AAPL_CumReturn', data=aapl_data, label='Apple (AAPL) Cumulative Return', color='blue')
sns.lineplot(x='Date', y='MSFT_CumReturn', data=msft_data, label='Microsoft (MSFT) Cumulative Return', color='orange')

# Set plot labels and title
plt.title('Cumulative Returns: Apple vs Microsoft (2020)', fontsize=16)
plt.xlabel('Date', fontsize=14)
plt.ylabel('Cumulative Return', fontsize=14)
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Calculate volatility (standard deviation of returns)
aapl_volatility = aapl_data['AAPL_Return'].std()
msft_volatility = msft_data['MSFT_Return'].std()

print(f"AAPL Volatility: {aapl_volatility:.4f}")
print(f"MSFT Volatility: {msft_volatility:.4f}")
