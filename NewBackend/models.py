import pandas as pd
import requests
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import r2_score, mean_squared_error 
import pickle 
import yfinance as yf




def fetch_crypto_data(crypto_symbol, days):
    url = f'https://api.coingecko.com/api/v3/coins/{crypto_symbol}/market_chart'
    parameters = {
        'vs_currency': 'usd',
        'days': days,
    }

    response = requests.get(url, params=parameters)
    data = response.json()

    if response.status_code == 200:
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms').dt.date
        df = df.drop(columns=['timestamp'])
        return df
    else:
        raise Exception('Error fetching cryptocurrency data.')

def fetch_sp500_data(period):
    sp500 = yf.Ticker("^GSPC")
    hist = sp500.history(period=period)
    df = hist[['Close']].reset_index()
    df['date'] = df['Date'].dt.date
    df = df.rename(columns={'Close': 'price_sp500'})
    df = df[['date', 'price_sp500']]
    return df










    # Prepare data for model training
def train_and_saved_model():
# Test the fetch_crypto_data function
    try:
        crypto_data = fetch_crypto_data('bitcoin', '365')  # Fetch last 1 years of data for Bitcoin
        print("Crypto Data:\n", crypto_data.head())
    except Exception as e:
        print("Error fetching crypto data:", e)

    # Test the fetch_sp500_data function
    try:
        sp500_data = fetch_sp500_data('2y')  # Fetch 2 years of data for S&P 500
        print("S&P 500 Data:\n", sp500_data.head())

    except Exception as e:
        print("Error fetching S&P 500 data:", e)

    print("Crypto Data Columns:", crypto_data.columns)
    print("S&P 500 Data Columns:", sp500_data.columns)

    try:
        df_merged = pd.merge(crypto_data, sp500_data, on='date', how='inner')
        print("Merged Data:\n", df_merged.head())
    except Exception as e:
        print("Error merging data:", e)

    # Prepare data for model training
    try:
        x = df_merged[['price_sp500']]
        y = df_merged['price']
    except KeyError as e:
        print(f"KeyError: {e}")
        print("Available columns in merged DataFrame:", df_merged.columns)

    # Split data into training and testing sets
    try:
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    except Exception as e:
        print("Error during train-test split:", e)

   
    try:
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
    except Exception as e:
        print("Error during train-test split:", e)



    try:
        model = LinearRegression()
        model.fit(X_train, y_train)
    except Exception as e:
        print("Error during model training:", e) 
        return 

    try: 
        with open('crypto_model.pkl', 'wb') as file: 
            pickle.dump(model, file)
    except Exception as e: 
        print("Error during model Training: ", e)
    # Evaluate the model
    try:
        y_pred = model.predict(X_test)
        print("R^2 score:", r2_score(y_test, y_pred))
        print("Mean Squared Error:", mean_squared_error(y_test, y_pred))
    except Exception as e:
        print("Error during model evaluation:", e)


if __name__ == "__main__":
    train_and_saved_model()
