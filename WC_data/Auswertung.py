import pandas as pd

days = 5


gasNLall= pd.read_csv("WC_sim_output_all.csv",sep=';').round(1)
gasNLall.index = pd.date_range(start='00:00 01.01.2019', end = '23:59 01.05.2019',freq='1 min')
gasNLall["2019-01-01 0:00":"2019-01-01 1:30"].drop(['time [s]','f [Hz]','aFRR FRCE (open loop) [MW]','mFRR P [MW]','Unnamed: 11'],axis=1).plot(secondary_y='AEP [EUR/MWh]')


gasNL= pd.read_csv("WC_sim_output_period.csv",sep=';',encoding='latin-1').round(1)
gasNL.index = pd.date_range(start='00:00 01.01.2019', end = '23:30 01.05.2019',freq='15 min')
sum = gasNL.sum()

print('hi')