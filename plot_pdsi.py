#!/usr/bin/python
import os
import pandas
import matplotlib
import numpy
from pandas import Series
from matplotlib import pyplot as plt
from matplotlib import dates as mdates
import datetime as dt
from PIL import Image

dateparse = lambda dates: pandas.datetime.strptime(dates, '%Y-%m')

stations = ['SANJQ', 'SANLO', 'SANDI']
# month_spi = ['1', '12', '24']
filenames = []

for i in range(len(stations)):
    filenames.append("monthly_alt/scPDSI_m_" + stations[i] + ".clm")
for i in range(len(filenames)):
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(111)
    df = pandas.read_table(filenames[i], sep="\s+")
    mapping = {df.columns[1]: 'Month'}

    df.rename(columns=mapping, inplace=True)
    df.Month = df.Month.astype(int)

    j = 0
    k = 0
    for it, row, in df.iterrows():
        if row['PDSI'] < 0:
            j = j + 1
            if row['PDSI'] < -4:
                k = k + 1
            if row['Year'] > 2017:
                if row['Month'] > 7:
                    if (j > 36):
                        print("vals less than 0 for over a year"
                            , row['Year'] , row['Month'] , " since " , j ,  "months ago.")
                    if (k > 1):
                        print("Vals less than -4 on"
                            , row['Year'] , row['Month'] , " since " , k ,  "months ago.")
        if row['PDSI'] > 0:
            if (j > 36):
                print("vals less than 0 for over a year"
                    , row['Year'] , row['Month'] , " since " , j ,  "months ago.")
            j = 0
        if row['PDSI'] > -4:
            if (k > 1):
                print("Vals less than -4 on"
                    , row['Year'] , row['Month'] , " since " , k ,  "months ago.")
            k = 0


    # TODO: Change dataframe from month to date to develop timeseries - errased
    # to avoid plagarism/cheating

    print(filenames[i])

    y=-4
    y2=0
    ax1.axhline(y, color='#2f6a50')

    mask = df["PDSI"] > -4
    plt.plot(df['Date'], df['PDSI'], color='#619D82', zorder= 1)
    plt.plot(y, color='green')

    z = numpy.polyfit(df['Date'], df['PDSI'], 1)
    p = numpy.poly1d(z)
    plt.plot(df['Date'],p(df['Date']),color = '#7244d5', linestyle = 'dashed', zorder = 2)

    tmp = (df.loc[df['Date'] >= 1983]).astype(float)
    z = numpy.polyfit(tmp['Date'], tmp['PDSI'], 1)
    p = numpy.poly1d(z)
    plt.plot(tmp['Date'],p(tmp['Date']),"k--")

    # plt.plot(tmp['Date'], tmp['PDSI'], color='green')

    ax1.set_title(stations[i] + " PDSI", fontsize=30)
    ax1.set_xlabel("Year")
    ax1.set_ylabel("PDSI")
    plt.xlim(xmin=1885, xmax=2019)
    plt.show()
