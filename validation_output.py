# analysis .py file to crunch simulation output data of 7 days field test week (18.11.2019 to 24.11.2019)
# version 1.0 - 14.05.2020

# validation_output.py can be used for
# (i) Data without Smart Balancing: validation with historic data
# (ii) Data with Smart Balancing: Comparison with (i) for benefit estimation

# - depending on input data:
# - validation_and_analysis/data4validatin.csv with historic data of fielt dest week for (i)
# - validation_and_analysis/sim_output_period_no_SB.csv for (i and ii)
# - Feldtest_data/sim_output_period.csv for (ii)

#this merge with Commit "PAPER SIM2: All 4 BGs provide SB. No upper limit" has Data with Smart Balancing contribution -> contains (ii) benefit estimation

import pandas as pd
import matplotlib.pyplot as plt


Feldt = pd.read_csv("Feldtest_data/Feldtest_sim_output_period.csv", sep=';')
#columns: time [s];GER pos. Energy aFRR [MWh];GER neg. Energy aFRR [MWh];GER pos. aFRR costs [EUR];GER neg. aFRR costs [EUR];GER AEP [EUR/MWh];ARCELOR load energy [MWh];ARCELOR pos. SB energy [MWh];ARCELOR neg. SB energy [MWh];ARCELOR AEP costs [EUR];ARGE gen energy [MWh];ARGE pos. SB energy [MWh];ARGE neg. SB energy [MWh];ARGE AEP costs [EUR];AURUBIS load energy [MWh];AURUBIS pos. SB energy [MWh];AURUBIS neg. SB energy [MWh];AURUBIS AEP costs [EUR];TRIMET load energy [MWh];TRIMET pos. SB energy [MWh];TRIMET neg. SB energy [MWh];TRIMET AEP costs [EUR];


#Time range: ['00:00 18.11.2019':'23:30 24.11.2019']
#Um den Zeitreihen (15 Min-Werte) aus dem Modell einen Zeitstempel zu geben:
#data 30 min too short
Feldt.index = pd.date_range(start='00:00 18.11.2019', end = '23:30 24.11.2019',freq='15 min')

#read historic data (imbalance, activated reserves etc.)
#Historic = pd.read_csv("validation_and_analysis/data4validation.csv")
#columns: Timestamp,aFRR_pow_up_MW,aFRR_pow_down_MW,aFRR_cost_up_Euro,aFRR_cost_down_Euro,imbalance_price_Euro_per_MWh,mFRR_pow_up_MW,mFRR_pow_down_MW,mFRR_cost_up_Euro,mFRR_cost_down_Euro
#Historic.index = pd.date_range(start='00:00 18.11.2019', end = '23:30 24.11.2019',freq='15 min')

# (ii) benefit estimation

# sum up cost and energy values and save to new csv
#Historic.sum().to_csv("validation_and_analysis/sum_energy_and_costs_historic.csv",header=["historic"])
sum_energy_and_costs = pd.read_csv("validation_and_analysis/sum_energy_and_costs_simulation.csv",index_col=0)
sum_energy_and_costs["SB limit to ACE"] = Feldt.sum()
sum_energy_and_costs.to_csv("validation_and_analysis/sum_energy_and_costs_simulation.csv")


# (i) validation of output data via correlation factor

#Correlation mit Pandas berechnen: 1. Neuen DataFrame bilden mit relevanten Parametern (beliebig viele), 2. DataFrame.corr()

#compare historic aFRR activation with simulation output via correlation factor
#Vergleich_aFRR_pow = pd.DataFrame()
#Vergleich_aFRR_pow["aFRR_pow_up_sim"] = Feldt["GER pos. Energy aFRR [MWh]"]*4
#Vergleich_aFRR_pow["aFRR_pow_up_hist"] = Historic["aFRR_pow_up_MW"]
#correlation factor is 0.9871

#Vergleich_aFRR_pow["aFRR_pow_down_sim"] = Feldt["GER neg. Energy aFRR [MWh]"]*(-4)
#Vergleich_aFRR_pow["aFRR_pow_down_hist"] = Historic["aFRR_pow_down_MW"]
#correlation factor is 0.9931

# calculate and export correlation factors to csv
#Vergleich_aFRR_pow.corr().to_csv("validation_and_analysis/aFRR_pow_validation_via_correlation.csv")

#compare historic aFRR costs with simulation output via correlation factor
#Vergleich_aFRR_cost = pd.DataFrame()
#Vergleich_aFRR_cost["aFRR_cost_up_sim"] = Feldt["GER pos. aFRR costs [EUR]"]
#Vergleich_aFRR_cost["aFRR_cost_up_hist"] = Historic["aFRR_cost_up_Euro"]
#correlation factor is 0.9818

#Vergleich_aFRR_cost["aFRR_cost_down_sim"] = -Feldt["GER neg. aFRR costs [EUR]"]
#Vergleich_aFRR_cost["aFRR_cost_down_hist"] = Historic["aFRR_cost_down_Euro"]
#correlation factor is 0.9184

# calculate and export correlation factors to csv
#Vergleich_aFRR_cost.corr().to_csv("validation_and_analysis/aFRR_cost_validation_via_correlation.csv")


#compare historic imbalance price with simulation output via correlation factor
#Vergleich_AEP_imbalance_price = pd.DataFrame()
#Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_sim"] = Feldt["GER AEP [EUR/MWh]"]
#Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_hist"] = Historic["imbalance_price_Euro_per_MWh"]

# calculate and export correlation factors to csv
#Vergleich_AEP_imbalance_price.corr().to_csv("validation_and_analysis/AEP_imbalance_price_validation_via_correlation.csv")
# correlation factor is 0.5290

#______________________optional________________
#Die Sekundenwerte könnte man auch vergleichen. Dazu habe ich in zwei Schritten für den Vergleich vorbereitet: 1. Zeitstempel geben 2. 15 Min Mittelwerte bilden
#data 2s to short
#Feldt_sec.index = pd.date_range(start='00:00:00 18.11.2019', end = '23:59:58 24.11.2019',freq='S’)
#resample 1s to 15 min
#Feldt_resample = Feldt_sec.resample('15 Min').mean()
#______________________



#plt.figure(1,figsize=(8, 6))
#plt.plot(Vergleich_aFRR_pow["18.11.2019"])
#plt.legend(["aFRR_up_pow_sim","aFRR_up_pow_hist","aFRR_down_pow_sim","aFRR_down_pow_hist"])
#plt.ylabel('aFRR power in MW')
#plt.xlabel('Field test week')

#plt.savefig('validation_and_analysis//aFRR_pow_validation.png')

#plt.figure(2,figsize=(8, 6))
#plt.plot(Vergleich_aFRR_cost["18.11.2019"])
#plt.legend(["aFRR_up_cost_sim","aFRR_up_cost_hist","aFRR_down_cost_sim","aFRR_down_cost_hist"])
#plt.ylabel('aFRR costs in Euro')
#plt.xlabel('Field test week')

#plt.savefig('validation_and_analysis//aFRR_cost_validation.png')

#plt.figure(3,figsize=(8, 6))
#plt.plot(Vergleich_AEP_imbalance_price["18.11.2019"])
#plt.legend(["imbalance_price_sim","imbalance_price_hist"])
#plt.ylabel('imbalance price in Euro per MWh')
#plt.xlabel('Field test week')

#plt.savefig('validation_and_analysis//imbalance_price_validation.png')


#plt.show()