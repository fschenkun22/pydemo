import yfinance as yf
dat = yf.Ticker("MSFT")
print(dat.history(period="1d"))