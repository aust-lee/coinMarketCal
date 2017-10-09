import re
import urllib.request
import pandas as pd
import numpy as np
import time
import requests


#Get all the Calendar information
def grabCalInfo():
    text = urllib.request.urlopen('http://coinmarketcal.com/').read().decode()

#coins = re.findall('(?<=Coin -->\n\t\t\t\t\t\t\t\t\t<h5><strong>).+(?=</strong>)',text)
    coins = re.findall('(?<=Coin -->\n                            <h5><strong>).+(?=</strong>)',text)
    parts = [coin.split() for coin in coins]

#dates = re.findall('(?<=\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<h5><strong>).+(?=</strong>)', text)
    regDate = """(?<=
                                                            <h5><strong>).+(?=</strong>)"""

    dates = re.findall(regDate, text)

    certainty = re.findall('(?<=aria-valuenow=").+?(?=" role)', text)

    sheet = []
    for i in range(len(coins)):
        if len(parts[i]) == 2:
            if 'By' not in dates[i]:
                sheet.append([parts[i][0], parts[i][1][1:-1], dates[i], int(certainty[i])])


    return sheet

#Get any new ticker symbols
def updateTickers(currentTickers):
    for ticker in set(pd.DataFrame(getCalInfo())[1]):
        if ticker not in currentTickers:
            currentTickers.add(ticker)
    return currentTickers

#get any new events
def checkEvents(currentEvents):
    events = grabCalInfo()
    for event in events:
        if event not in currentEvents:
            currentEvents.append(event)
            print('Adding', event)
    return currentEvents

#get these prices
def getPrices(tickers):
    prices = requests.get('https://api.coinmarketcap.com/v1/ticker/').json()
    for price in prices:
        if price['symbol'] in tickers:
            prices.append([price['symbol'], price['price_usd'], price['price_btc'], time.time()])
    return prices

events = checkEvents([])
tickers = {}
prices = []

"""while True:
    print('Gathering CoinMarketCal Data')
    coinInfo = grabCalInfo()

    print('Updating event list')
    events = checkEvents(events)
    
    print('Updating tickers...')
    tickers = updateTickers(tickers)
    
    print('Getting new prices...')
    prices.append(getPrices(tickers))
    
    events = cleanUpEvents()
    
    time.sleep(3600)   
    
    
#tickers = set(grabCalInfo()[1])
coinInfo = grabCalInfo()

prices = getPrices()"""
                   
                