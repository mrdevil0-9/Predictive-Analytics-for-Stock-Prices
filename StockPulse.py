import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def fetch_stock_data(ticker, market):
    ticker_symbol = f"{ticker}.NS" if market.lower() == 'nse' else f"{ticker}.BO"
    stock_data = yf.download(ticker_symbol, start="2000-01-01", end="2024-10-24", progress=False)
    return stock_data

def fetch_sentiment_data():
    urls = {
        "Pulse by Zerodha": "https://pulse.zerodha.com/",
        "Economic Times": "https://economictimes.indiatimes.com/",
        "NDTV Profit": "https://www.ndtvprofit.com/",
        "Bloomberg Quint": "https://www.bloombergquint.com/",
        "The Hindu Business": "https://www.thehindu.com/business/",
        "Moneycontrol": "https://www.moneycontrol.com/"
    }

    headlines = []
    sentiments = []

    for name, url in urls.items():
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Modify this based on the actual HTML structure for stock-related news
        for item in soup.find_all('h2'):  # Assuming headlines are in <h2> tags
            headline_text = item.get_text(strip=True)
            # Only include relevant headlines
            if any(keyword in headline_text.lower() for keyword in ["stock", "shares", "market", "invest"]):
                sentiment_percentage = np.random.uniform(40, 80)  # Placeholder for sentiment calculation
                headlines.append(headline_text)
                sentiments.append(sentiment_percentage)

    sentiment_data = pd.DataFrame({"headline": headlines, "sentiment": sentiments})

    # Remove rows with NaN or empty sentiment
    sentiment_data = sentiment_data.dropna()
    
    return sentiment_data

def predict_stock_price(stock_data):
    stock_data['Prediction'] = stock_data['Close'].shift(-1)
    
    # Use only the last 60 days for prediction to reduce noise
    X = np.array(stock_data[['Close']][-60:-1])  
    y = np.array(stock_data['Prediction'][-60:-1])
    
    if len(y) < 2:  # Ensure we have enough data for prediction
        return None

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LinearRegression()
    model.fit(X_train, y_train)
    predicted_price = model.predict(X_test)

    return np.mean(predicted_price)

if _name_ == "_main_":
    ticker = input("Enter stock tickers (e.g., ZOMATO for NSE or 543638 for BSE): ")
    market = input("Enter the market (NSE or BSE): ")
    
    stock_data = fetch_stock_data(ticker, market)
    print(f"Fetched data for {ticker}:\n{stock_data}")

    sentiment_data = fetch_sentiment_data()
    print(f"Sentiment data for {ticker}:\n{sentiment_data}")

    predicted_price = predict_stock_price(stock_data)
    
    if predicted_price is not None:
        print(f"Predicted next day price for {ticker}: {predicted_price:.2f}")
    else:
        print("Not enough data to predict the next day price.") 
