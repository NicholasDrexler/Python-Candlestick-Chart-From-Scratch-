"""
Stockmarket Style Candlestick Chart
written by: Nicholas Drexler 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# variables
day_span = 90             # How many days prior to today do you want to see
tb_padding = 100            # How much space do you want above and below graph

# stock choice
# future versions should allow a choice as part of a gui based system. 

# Amazon 
# url = "https://query1.finance.yahoo.com/v7/finance/download/AMZN?period1=1596477899&period2=1628013899&interval=1d&events=history&includeAdjustedClose=true"

# Tesla
url = "https://query1.finance.yahoo.com/v7/finance/download/TSLA?period1=1596478070&period2=1628014070&interval=1d&events=history&includeAdjustedClose=true"

# load the data 
data = pd.read_csv(url)

# bring in columns and have them change length based on day_span
dates = data.Date[-day_span:]
opens = data.Open[-day_span:]
closes = data.Close[-day_span:]
highs = data.High[-day_span:]
lows = data.Low[-day_span:]

# logic for iterations and refferneces
n_range = np.arange((len(data) - day_span),len(data))


def candleMaker(x, oc_ymin, oc_ymax, hl_ymin, hl_ymax, color):
    '''
    Produces both the rectange for the candle representing open and close prices,
    and the thin wick used to represent relative high and low price fluxuations,
    over the course of that particular trading day.
    
    Rectangle2: the thin wick
    Rectangle1: the rectangular candle
    
    '''
    
    rectangle2 = plt.Rectangle((x+(0.25), hl_ymin), 0.2, hl_ymax-hl_ymin, fc='black')
    rectangle1 = plt.Rectangle((x, oc_ymin), 0.75, oc_ymax-oc_ymin, fc=color)
    plt.gca().add_patch(rectangle2)
    plt.gca().add_patch(rectangle1)
    
    
# Begin graphing
plt.figure(figsize=(15,8))

# The min and mix value for any particular day are provided via iteration
ymin_array = []
ymax_array = []
for i in n_range:
    y_min = 0.0
    y_max = 0.0
    y_high = 0.0
    y_low = 0.0
    color = str

    high = highs[i]
    low = lows[i]

    if closes[i] > opens[i]:
        # gain
        y_min = opens[i]
        y_max = closes[i]
        color = 'green'
    elif closes[i] < opens[i]:
        # loss
        y_min = closes[i]
        y_max = opens[i]
        color = 'red'   
    elif closes[i] == opens[i]:
        # no change
        color = 'black'
        y_min = y_max = closes[i]
    
    ymin_array.append(y_min)
    ymax_array.append(y_max)  

    candleMaker(i,y_min,y_max,low,high,color)


plt.title("Stockmarket Style Candlestick Chart")

plt.xlabel("Days")
plt.ylabel("Price")

plt.rc('axes', titlesize=20)
plt.rc('axes', labelsize=20)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

# used to adjust yaxis boundarys and relative padding
the_max = max(ymax_array)
the_min = min(ymin_array)
plt.ylim((the_min-tb_padding,the_max+tb_padding))
plt.xlim(n_range[0],n_range[-1])

# Show the major and minor grid lines
plt.grid()
plt.grid(b=True, which='major', color='#666666', linestyle='-')
plt.minorticks_on()
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

plt.tight_layout()
plt.show()




