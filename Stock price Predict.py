import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from google.colab import files
uploaded = files.upload()

#read the file
df = pd.read_csv('A2M.AX1.csv')
df = df.set_index(pd.DatetimeIndex(df['Date'].values))
#print the head
df

def EMA(data, period=20, column='Close'):
  return data[column].ewm(span=period, adjust=False).mean()
  

def StochRSI(data, period=14, column='Close'):
  delta = data[column].diff(1)
  delta = delta.dropna()
  up = delta.copy()
  down= delta.copy()
  up[up<0]=0
  down[down>0]=0
  data['up']=up
  data['down']=down
  AVG_Gain = EMA(data, period, column='up')
  AVG_LOSS = abs(EMA(data, period, column='down'))
  RS= AVG_Gain/AVG_LOSS
  RSI = 100.0 - (100.0/(1.0 + RS))

  stockrsi = (RSI - RSI.rolling(period).min())/(RSI.rolling(period).max()-RSI.rolling(period).min())
  return stockrsi

df['StochRSI'] = StochRSI(df)

fig,(ax1, ax2) = plt.subplots(nrows=2, sharex=True)
plt.subplots_adjust(hspace=.0)
ax1.grid
ax2.grid
ax1.plot(df.index, df['Close'], color = 'r')
ax2.plot(df.index, df['StochRSI'], color = 'b', linestyle = '--')
ax2.axhline(0.2, color='orange')
ax2.axhline(0.8, color='orange')
plt.xticks(rotation=45)
