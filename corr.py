#!/usr/bin/python
import os
import pandas
import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns

stations = ['SANJQ', 'SANLO', 'SANDI']
index_type = ['scSPI_1_m_', 'scSPI_12_m_', 'scSPI_24_m_', 'scPDSI_m_']
filenames = []

for i in range(len(stations)):
    for j in range(len(index_type)):
        filenames.append("monthly_alt/" + index_type[j] + stations[i] + ".clm")
    title = stations[i]

    spi1 = pandas.read_table(filenames[0], sep="\s+")
    mapping = {spi1.columns[2]: 'SPI-1'}
    spi1.rename(columns=mapping, inplace=True)
    spi12 = pandas.read_table(filenames[1], sep="\s+")
    mapping = {spi12.columns[2]: 'SPI-12'}
    spi12.rename(columns=mapping, inplace=True)
    spi24 = pandas.read_table(filenames[2], sep="\s+")
    mapping = {spi24.columns[2]: 'SPI-24'}
    spi24.rename(columns=mapping, inplace=True)
    pdsi = pandas.read_table(filenames[3], sep="\s+")

    corr_df = pandas.merge(pandas.merge(pandas.merge(spi1, spi12, on=['Year', 'Per'])
                ,spi24, on=['Year', 'Per'])
                ,pdsi, on=['Year', 'Per'])

    corr_df = corr_df.drop(['Year'], axis=1).drop(['Per'], axis=1)

    print(corr_df)

    corr = corr_df.corr()
    corr.style.background_gradient()

    f, ax = plt.subplots(figsize=(10, 8))
    ax.set_title(title)
    sns.heatmap(corr, annot=True, fmt='f', mask=np.zeros_like(corr, dtype=np.bool), cmap=sns.diverging_palette(150, 275, as_cmap=True),
            square=True, ax=ax)
    plt.show()
