import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

# Function to fetch stock data from SQLite
def fetch_stock_data(stock, start_date, end_date):
    conn = sqlite3.connect('stock_prices.db')
    query = f"SELECT * FROM {stock} WHERE Date BETWEEN '{start_date}' AND '{end_date}'"
    stock_data = pd.read_sql(query, conn)
    conn.close()
    return stock_data

# Streamlit page title
st.title('Stock Market Price Comparison')

# Dropdown for selecting stock
stocks = ['AAPL', 'MSFT']
selected_stock = st.selectbox('Select a Stock', stocks)

# Date range picker
start_date = st.date_input('Start Date', pd.to_datetime('2020-01-01'))
end_date = st.date_input('End Date', pd.to_datetime('2021-01-01'))

# Load the stock data
stock_data = fetch_stock_data(selected_stock, start_date, end_date)

# Plot Closing Price
st.subheader(f'Closing Price for {selected_stock}')
plt.figure(figsize=(14, 7))
sns.lineplot(x='Date', y=f'{selected_stock}_Close', data=stock_data, label=f'{selected_stock} Closing Price', color='blue')
plt.title(f'{selected_stock} Stock Price Trend')
plt.xlabel('Date')
plt.ylabel('Closing Price (USD)')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Calculate and plot daily returns
stock_data[f'{selected_stock}_Return'] = stock_data[f'{selected_stock}_Close'].pct_change() * 100
stock_data.dropna(inplace=True)

st.subheader(f'Daily Returns for {selected_stock}')
plt.figure(figsize=(14, 7))
sns.lineplot(x='Date', y=f'{selected_stock}_Return', data=stock_data, label=f'{selected_stock} Daily Returns', color='orange')
plt.title(f'{selected_stock} Daily Returns')
plt.xlabel('Date')
plt.ylabel('Daily Returns (%)')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)

# Calculate and plot cumulative returns
stock_data[f'{selected_stock}_CumReturn'] = (1 + stock_data[f'{selected_stock}_Return'] / 100).cumprod() - 1

st.subheader(f'Cumulative Returns for {selected_stock}')
plt.figure(figsize=(14, 7))
sns.lineplot(x='Date', y=f'{selected_stock}_CumReturn', data=stock_data, label=f'{selected_stock} Cumulative Return', color='green')
plt.title(f'{selected_stock} Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Return')
plt.xticks(rotation=45)
plt.grid(True)
st.pyplot(plt)
