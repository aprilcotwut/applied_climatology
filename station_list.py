#!/usr/bin/python
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# This script automatically developes a stationlist to use in RClimDex from
# timeseries csv retrieved from PRISM (Oregon State Climate Group).
#
# Author: April Walker
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import os
import pandas


global_df = pandas.DataFrame(columns=['Fname','Long','Lat','Alt','AWC'])

def stationlist_prep(df):
    filename = input('Input file name of station to add to station list:\n')
    try:
        #open file
        file = open(filename)
        line = file.readline()
        while len(line) !=0:
            line = line.split() #split into a list
            #search for correct line
            if line[0] == 'Location:':
                found = True
                #save necessary data
                lat = float(line[2])
                lon = float(line[4])
                alt = float(line[6][:-1])
                #fname saved as "filename" minus ".csv"
                splitfilename = filename.split('.')
                fname = splitfilename[0]
                #save data to dataframe
                df2 = pandas.DataFrame({'Fname': [fname], 'Long': [lon],
                                        'Lat': [lat],'Alt': [alt], 'AWC': [150]})
                break
            line = file.readline() # read subsequent records
            print(line)
        # close file
        file.close()

        if found:
            print('Data aquired - writing to station list\n')
            df = df.append(df2, ignore_index=True)
            print(df)
            answer = input('Would you like to add another station? (N/y)\n')
            if (answer is 'Y') or (answer is 'y'):
                df = stationlist_prep(df)
            return df
        else:
            print('Error! Data was not gathered\n.')

    except FileNotFoundError:
        print('Error: File not found\n.')

def fix_data(filename):
    #open file
    file = open(filename)
    print(filename)
    #and look for...
    line = file.readline()
    while len(line) !=0:
        word = line.split(',')
        #the first word of the header
        if word[0] == "Date":
                #make a tmp file to save it all in
                tmp = open('tmp.csv', 'w+')
                while line != '':
                    #write
                    tmp.write(line)
                    line = file.readline()
                tmp.close()
        line = file.readline()
    file.close()
    #now lets make a dataframe out of this data
    df = pandas.read_table("tmp.csv", sep=",")
    #split date
    df[['Year', 'Mon']] = df['Date'].str.split('-',1, expand=True)
    df = df.drop('Date', axis=1)
    df['Mon'] = df['Mon'].str.lstrip('0')
    df['Mon'] = df['Mon'].astype(int)
    #put "year" "month" back at the front, switch temp and prec
    new_order = [-3,-2,-1,0]
    df = df[df.columns[new_order]]
    #rename 'ppt (mm)' and 'tmean' columns
    mapping = {df.columns[2]: 'Prec', df.columns[3]: 'Tavg'}
    df.rename(columns=mapping, inplace=True)
    print(df.head(5))

    #write to .wtx
    splitfilename = filename.split('.')
    fname = splitfilename[0]
    filepath = "monthly/" + fname + ".wtx"
    open(filepath, 'w+').close()
    df.to_csv(filepath, sep='\t', index=False)
    data = pandas.read_table(filepath, sep="\t")

    #error checking
    #yeah, yeah, this could have been done sooner - I was having issues w/ that
    for i in range(1895, 2018):
        tmp = data.loc[data['Year'] == i]
        if (tmp.shape[0] != 12):
            print("You may have an error...")
            print(tmp.head())
            answer = input("Continue? (N/y)")
            if (answer is 'Y') or (answer is 'y'):
                print("Continuing...")
            else:
                return 0
    if df.isnull().values.any():
        print("Your data has nulls... Please address and rerun this script")
        return 0

    #change original .csv to reduce confusions
    # newfilename = fname + "orig.csv"
    # print("Renaming " + filename + " to be " + newfilename)
    # os.rename(filename, newfilename)

    return 0
def main():
    if not os.path.exists("monthly"):
        os.mkdir("monthly")

    answer = input('If stationlist.txt exists, can I overwrite it? (N/y)\n')
    if (answer is 'Y') or (answer is 'y'):
        file = open('stationlist.lst', 'w+')
        df = stationlist_prep(global_df)
        df.to_csv(r'stationlist.lst', header=True, index=None, sep='\t', mode='w')
        for i in df.index:
            filename = df.loc[i, 'Fname'] + ".csv"
            fix_data(filename)
        os.remove('tmp.csv')
    else:
        print('Please rename old stationlist.txt or change directories ' +
                'before running this program')
    return 0
main()
