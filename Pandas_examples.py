# example how to crunch data with pandas: create 1s ACE timeseries from 1s aFRR, 15min other reserves timeseries

import pandas as pd

#import csv as pandas DataFrame

# MRL: define index as Timestamp (parse_dates), where to find index (incex_col) and which columns to read (usecols)
#additional functions, if applicable: sep = ";", decimal = ","
MRL = pd.read_csv("15m_historic_data_ACE_AEP_FRR.csv",parse_dates=True,index_col='Timestamp',usecols=['Timestamp','mFRR_down_MW','mFRR_up_MW'])


SRL = pd.read_csv("1s_aFRR_setpoint.csv",parse_dates=True,index_col='Unnamed: 0',decimal=',')


#Zusatzmaßnahmen are available in monthly files, read them all 
df1901 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201901.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1902 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201902.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1903 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201903.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1904 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201904.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1905 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201905.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1906 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201906.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1907 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201907.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1908 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201908.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1909 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201909.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1910 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201910.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1911 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201911.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1912 = pd.read_csv("NothilfenundZusatzmaßnahmen/Zusatzmaßnahmen_201912.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])

#df1911 and df1912 have no values - fill with zeros
df1911['QUAL. POS'] = 0
df1911['QUAL. NEG'] = 0
df1912['QUAL. POS'] = 0
df1912['QUAL. NEG'] = 0

#create new DataFrame with all values
frames = [df1901,df1902,df1903,df1904,df1905,df1906,df1907,df1908,df1909,df1910,df1911,df1912]
Zusatz = pd.concat(frames)

#rename columns
Zusatz.rename(columns={'QUAL. POS': 'Zusatz_up_MW'}, inplace=True)
Zusatz.rename(columns={'QUAL. NEG': 'Zusatz_down_MW'}, inplace=True)

#index as timestamp - only works if range+frequency results in the right amount of values for length of DataFrame
Zusatz.index = pd.date_range(start='00:00 01.01.2019', end = '23:59 31.12.2019',freq='15 min')
#show count, mean, std etc.
Zusatz.describe()
#show first / last 5 rows of DataFrame
#.head() / .tail()

#Nothilfen 
df1901 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201901.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1902 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201902.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1903 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201903.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1904 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201904.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1905 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201905.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1906 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201906.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1907 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201907.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1908 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201908.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1909 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201909.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1910 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201910.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1911 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201911.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])
df1912 = pd.read_csv("NothilfenundZusatzmaßnahmen/Nothilfe_201912.CSV",header=3,sep=';',thousands='.',decimal=',',usecols=['QUAL. POS','QUAL. NEG'])

#df1911 and df1912 have no values - fill with zeros
df1911['QUAL. POS'] = 0
df1911['QUAL. NEG'] = 0
df1912['QUAL. POS'] = 0
df1912['QUAL. NEG'] = 0

frames = [df1901,df1902,df1903,df1904,df1905,df1906,df1907,df1908,df1909,df1910,df1911,df1912]
Nothilfen = pd.concat(frames)

Nothilfen.rename(columns={'QUAL. POS': 'Nothilfen_up_MW'}, inplace=True)
Nothilfen.rename(columns={'QUAL. NEG': 'Nothilfen_down_MW'}, inplace=True)

Nothilfen.index = pd.date_range(start='00:00 01.01.2019', end = '23:59 31.12.2019',freq='15 min')
Nothilfen.describe()


#merge SRL (1s) and MRL etc. (15 min) to ACE in 1s frequency
ACE = pd.DataFrame()
ACE = SRL.join(MRL.resample('1s').ffill())
ACE = ACE.join(Zusatz.resample('1s').ffill())
ACE = ACE.join(Nothilfen.resample('1s').ffill())

#find and show nans in DataFrame:
#ACE[ACE.isna().any(axis=1)]

#fill nans with 0
ACE = ACE.fillna(0)

#calculate ACE, change of sign required for UC3 Simulation..
ACE['ACE'] = (ACE['GERMANY_aFRR_SETPOINT_MW'] + ACE['mFRR_up_MW'] - ACE['mFRR_down_MW'] + ACE['Zusatz_up_MW'] - ACE['Zusatz_down_MW'] + ACE['Nothilfen_up_MW'] - ACE['Nothilfen_down_MW'])*(-1)

#here the awesome function of timestamp: check June event (12.06.19 around 12)
ACE['2019-06-12 11h'].head()

#save monthly ACE timeseries with timestamp as index and ";" as seperator to csv 
for month in range(1,13):
    ACE['ACE']['2019-{0}'.format(month)].to_csv('ACE/{0}_ACE_2019.csv'.format(month),index=True,sep=';',index_label="Timestamp",header="ACE")

#check if 1 min resolution works
ACE['2019-06-12 11h'].resample('1Min').mean().head()

#save ACE in 1 min resolutin to csv
ACE['ACE'].resample('1Min').mean().to_csv('ACE/ACE_2019.csv',index=True,sep=';',index_label="Timestamp",header="ACE")

#save ACE in 1 min resolution of Fieltest week to csv
ACE['ACE']['18.11.2019':'24.11.2019'].resample('1Min').mean().to_csv('ACE/ACE_Feldtest.csv',index=True,sep=';',index_label="Timestamp",header="ACE")
