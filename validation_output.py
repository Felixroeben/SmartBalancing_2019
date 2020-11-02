# analysis .py file for
# validation of simulated output (without Smart Balancing)
# benefit estimation (with Smart Balancing)
# version 1.1 - 17.08.2020

# validation_output.py can be used for
# (i) Data without Smart Balancing: validation with historic data
# (ii) Data with Smart Balancing: Comparison with (i) for benefit estimation

# - depending on input data:
# - validation_data/15m_historic_data_ACE_AEP_FRR.csv with historic data (i)
# - validation_and_analysis/sim_output_period_no_SB.csv for (i and ii)
# - Feldtest_data/sim_output_period.csv for (ii)

#this merge with Commit "PAPER SIM2: All 4 BGs provide SB. No upper limit" has Data with Smart Balancing contribution -> contains (ii) benefit estimation

import pandas as pd
import matplotlib.pyplot as plt

# historic values for comparison
hist = pd.read_csv("validation_data/15m_historic_data_ACE_AEP_FRR.csv")#,parse_dates=True, index_col='Timestamp')
#columns: Timestamp,ACE_MW,AEP,aFRR_down_MW,aFRR_up_MW,aFRR_down_price,aFRR_up_price,mFRR_down_MW,mFRR_up_MW,mFRR_down_price,mFRR_up_price

# simulation data without Smart Balancing for validation - no mFRR
no_SB_no_mFRR = pd.read_csv("validation_and_analysis/2019, 1min, no mFRR, no SB/WC_Sim_output_period.csv",sep=';')
# simulation data without Smart Balancing for validation - with mFRR
no_SB_with_mFRR = pd.read_csv("validation_and_analysis/2019, 1min, with mFRR, no SB/WC_Sim_output_period.csv",sep=';')

no_SB = pd.read_csv("WC_data/results/1 no SB/WC_Sim_output_period.csv",sep=';')
no_SB_AEP = pd.read_csv("WC_data/results/1 no SB AEP/WC_Sim_output_period.csv",sep=';')

#time [s]	GER pos. energy aFRR [MWh]	GER neg. energy aFRR [MWh]	GER pos. aFRR costs [EUR]	GER neg. aFRR costs [EUR]	GER pos. energy mFRR [MWh]	GER neg. energy mFRR [MWh]	GER pos. mFRR costs [EUR]	GER neg. mFRR costs [EUR]	GER AEP [EUR/MWh]
#Feldt.index = pd.date_range(start='00:00 01.01.2019', end = '23:30 24.11.2019',freq='15 min')


# (i) validation of output data via correlation factor

#Correlation mit Pandas berechnen: 1. Neuen DataFrame bilden mit relevanten Parametern (beliebig viele), 2. DataFrame.corr()

#compare historic aFRR activation with simulation output via correlation factor
Vergleich_aFRR_pow = pd.DataFrame()
Vergleich_aFRR_pow["aFRR_pow_up_sim_hist"] = hist["aFRR_up_MW"]
Vergleich_aFRR_pow["aFRR_pow_up_no_mFRR"] = no_SB_no_mFRR["GER pos. energy aFRR [MWh]"]*4
#correlation factor is 0.73
Vergleich_aFRR_pow["aFRR_pow_up_sim_with_mFRR"] = no_SB_with_mFRR["GER pos. energy aFRR [MWh]"]*4
#correlation factor is 0.85
Vergleich_aFRR_pow["aFRR_pow_up_sim_no_SB"] = no_SB["GER pos. energy aFRR [MWh]"]*4
#correlation factor is 0.86
Vergleich_aFRR_pow["aFRR_pow_up_sim_no_SB_AEP"] = no_SB_AEP["GER pos. energy aFRR [MWh]"]*4
#correlation factor is 0.86

Vergleich_aFRR_pow["aFRR_pow_down_sim_hist"] = -hist["aFRR_down_MW"]
Vergleich_aFRR_pow["aFRR_pow_down_no_mFRR"] = no_SB_no_mFRR["GER neg. energy aFRR [MWh]"]*(4)
#correlation factor is 0.88
Vergleich_aFRR_pow["aFRR_pow_down_sim_with_mFRR"] = no_SB_with_mFRR["GER neg. energy aFRR [MWh]"]*(4)
#correlation factor is 0.90
Vergleich_aFRR_pow["aFRR_pow_down_sim_no_SB"] = no_SB["GER neg. energy aFRR [MWh]"]*(4)
#correlation factor is 0.89
Vergleich_aFRR_pow["aFRR_pow_down_sim_no_SB_AEP"] = no_SB_AEP["GER neg. energy aFRR [MWh]"]*(4)
#correlation factor is 0.89

# calculate and export correlation factors to csv
#Vergleich_aFRR_pow.corr().to_csv("validation_and_analysis/corr/aFRR_pow_validation_via_correlation.csv",sep=';')

#compare historic aFRR costs with simulation output via correlation factor
Vergleich_aFRR_cost = pd.DataFrame()
Vergleich_aFRR_cost["aFRR_cost_up_hist"] = hist["aFRR_up_price"]*hist['aFRR_up_MW']/4
Vergleich_aFRR_cost["aFRR_cost_up_sim_no_mFRR"] = no_SB_no_mFRR["GER pos. aFRR costs [EUR]"]
#correlation factor is 0.77
Vergleich_aFRR_cost["aFRR_cost_up_sim_with_mFRR"] = no_SB_with_mFRR["GER pos. aFRR costs [EUR]"]
#correlation factor is 0.63
Vergleich_aFRR_cost["aFRR_cost_up_sim_no_SB"] = no_SB["GER pos. aFRR costs [EUR]"]
#correlation factor is 0.69
Vergleich_aFRR_cost["aFRR_cost_up_sim_no_SB_AEP"] = no_SB_AEP["GER pos. aFRR costs [EUR]"]
#correlation factor is 0.69

Vergleich_aFRR_cost["aFRR_cost_down_hist"] = hist["aFRR_down_price"]*hist['aFRR_down_MW']/(-4)
Vergleich_aFRR_cost["aFRR_cost_down_sim_no_mFRR"] = no_SB_no_mFRR["GER neg. aFRR costs [EUR]"]
#correlation factor is 0.77
Vergleich_aFRR_cost["aFRR_cost_down_sim_with_mFRR"] = no_SB_with_mFRR["GER neg. aFRR costs [EUR]"]
#correlation factor is 0.82
Vergleich_aFRR_cost["aFRR_cost_down_sim_no_SB"] = no_SB["GER neg. aFRR costs [EUR]"]
#correlation factor is 0.72
Vergleich_aFRR_cost["aFRR_cost_down_sim_no_SB_AEP"] = no_SB_AEP["GER neg. aFRR costs [EUR]"]
#correlation factor is 0.72

# calculate and export correlation factors to csv
#Vergleich_aFRR_cost.corr().to_csv("validation_and_analysis/corr/aFRR_cost_validation_via_correlation.csv",sep=';')

#____________
Vergleich_mFRR_pow = pd.DataFrame()
Vergleich_mFRR_pow["mFRR_pow_up_sim_hist"] = hist["mFRR_up_MW"]
Vergleich_mFRR_pow["mFRR_pow_up_sim_with_mFRR"] = no_SB_with_mFRR["GER pos. energy mFRR [MWh]"]*4
#correlation factor is 0.50
Vergleich_mFRR_pow["mFRR_pow_up_sim_no_SB"] = no_SB["GER pos. energy mFRR [MWh]"]*4
#correlation factor is 0.57
Vergleich_mFRR_pow["mFRR_pow_up_sim_no_SB_AEP"] = no_SB_AEP["GER pos. energy mFRR [MWh]"]*4
#correlation factor is 0.57

Vergleich_mFRR_pow["mFRR_pow_down_sim_hist"] = -hist["mFRR_down_MW"]
Vergleich_mFRR_pow["mFRR_pow_down_sim_with_mFRR"] = no_SB_with_mFRR["GER neg. energy mFRR [MWh]"]*(4)
#correlation factor is 0.55
Vergleich_mFRR_pow["mFRR_pow_down_sim_no_SB"] = no_SB["GER neg. energy mFRR [MWh]"]*(4)
#correlation factor is 0.53
Vergleich_mFRR_pow["mFRR_pow_down_sim_no_SB_AEP"] = no_SB_AEP["GER neg. energy mFRR [MWh]"]*(4)
#correlation factor is 0.53

# calculate and export correlation factors to csv
#Vergleich_mFRR_pow.corr().to_csv("validation_and_analysis/corr/mFRR_pow_validation_via_correlation.csv",sep=';')
#_______________

#compare historic aFRR costs with simulation output via correlation factor
Vergleich_mFRR_cost = pd.DataFrame()
Vergleich_mFRR_cost["mFRR_cost_up_hist"] = hist["mFRR_up_price"]*hist['mFRR_up_MW']/4
Vergleich_mFRR_cost["mFRR_cost_up_sim_no_mFRR"] = no_SB_no_mFRR["GER pos. mFRR costs [EUR]"]
#correlation factor is -
Vergleich_mFRR_cost["mFRR_cost_up_sim_with_mFRR"] = no_SB_with_mFRR["GER pos. mFRR costs [EUR]"]
#correlation factor is 0.51
Vergleich_mFRR_cost["mFRR_cost_up_sim_no_SB"] = no_SB["GER pos. mFRR costs [EUR]"]
#correlation factor is 0.57
Vergleich_mFRR_cost["mFRR_cost_up_sim_no_SB_AEP"] = no_SB_AEP["GER pos. mFRR costs [EUR]"]
#correlation factor is 0.57

Vergleich_mFRR_cost["mFRR_cost_down_hist"] = hist["mFRR_down_price"]*hist['mFRR_down_MW']/(-4)
Vergleich_mFRR_cost["mFRR_cost_down_sim_no_mFRR"] = no_SB_no_mFRR["GER neg. mFRR costs [EUR]"]
#correlation factor is -
Vergleich_mFRR_cost["mFRR_cost_down_sim_with_mFRR"] = -no_SB_with_mFRR["GER neg. mFRR costs [EUR]"]
#correlation factor is 0.23
Vergleich_mFRR_cost["mFRR_cost_down_sim_no_SB"] = -no_SB["GER neg. mFRR costs [EUR]"]
#correlation factor is 0.32
Vergleich_mFRR_cost["mFRR_cost_down_sim_no_SB_AEP"] = -no_SB_AEP["GER neg. mFRR costs [EUR]"]
#correlation factor is 0.32

# calculate and export correlation factors to csv
#Vergleich_mFRR_cost.corr().to_csv("validation_and_analysis/corr/mFRR_cost_validation_via_correlation.csv",sep=';')



#compare historic imbalance price with simulation output via correlation factor
Vergleich_AEP_imbalance_price = pd.DataFrame()
Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_hist"] = hist["AEP"]
Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_sim_no_mFRR"] = no_SB_no_mFRR["GER AEP [EUR/MWh]"]
#correlation factor is 0.48
Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_sim_with_mFRR"] = no_SB_with_mFRR["GER AEP [EUR/MWh]"]
#correlation factor is 0.37
Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_sim_FR"] = no_SB["GER AEP [EUR/MWh]"]
#correlation factor is 0.37
Vergleich_AEP_imbalance_price["imbalance_price_Euro_per_MWh_sim_FR_AEP"] = no_SB_AEP["GER AEP [EUR/MWh]"]
#correlation factor is 0.52

# calculate and export correlation factors to csv
#Vergleich_AEP_imbalance_price.corr().to_csv("validation_and_analysis/corr/AEP_imbalance_price_validation_via_correlation.csv",sep=';')




# (ii) benefit estimation

# sum up cost and energy values and save to new csv
#hist.sum().to_csv("validation_and_analysis/sum_energy_and_costs_historic.csv",header=["historic"])
#sum_energy_and_costs = pd.read_csv("validation_and_analysis/sum_energy_and_costs_simulation.csv",index_col=0)
#sum_energy_and_costs["SB limit to ACE"] = Feldt.sum()
#sum_energy_and_costs.to_csv("validation_and_analysis/sum_energy_and_costs_simulation.csv")




#______________________optional________________
#Die Sekundenwerte könnte man auch vergleichen. Dazu habe ich in zwei Schritten für den Vergleich vorbereitet: 1. Zeitstempel geben 2. 15 Min Mittelwerte bilden
#data 2s to short
#Feldt_sec.index = pd.date_range(start='00:00:00 18.11.2019', end = '23:59:58 24.11.2019',freq='S’)
#resample 1s to 15 min
#Feldt_resample = Feldt_sec.resample('15 Min').mean()
#______________________

Vergleich_aFRR_pow.index = pd.date_range(start='00:00 01.01.2019', end = '23:45 31.12.2019',freq='15 min')
Vergleich_mFRR_pow.index = pd.date_range(start='00:00 01.01.2019', end = '23:45 31.12.2019',freq='15 min')
Vergleich_aFRR_cost.index = pd.date_range(start='00:00 01.01.2019', end = '23:45 31.12.2019',freq='15 min')
Vergleich_AEP_imbalance_price.index = pd.date_range(start='00:00 01.01.2019', end = '23:45 31.12.2019',freq='15 min')


plt.figure(1,figsize=(8, 6))
plt.plot(Vergleich_aFRR_pow["18.11.2019"])
plt.legend(["aFRR_up_pow_hist","aFRR_up_pow_sim_no_mFRR","aFRR_up_pow_sim_with_mFRR","sim_FR","sim_fuzzySolar","sim_Solar","aFRR_down_pow_hist","aFRR_down_pow_sim_no_mFRR","aFRR_down_pow_sim_with_mFRR","sim_FRd","sim_fuzzySolard","sim_Solard"])
plt.ylabel('aFRR power in MW')
plt.xlabel('Field test week')

plt.savefig('validation_and_analysis//aFRR_pow_validation.png')

plt.figure(2,figsize=(8, 6))
plt.plot(Vergleich_aFRR_cost["18.11.2019"])
plt.legend(["aFRR_up_cost_hist","aFRR_up_cost_sim_no_mFRR","aFRR_up_cost_sim_with_mFRR","sim_FR","aFRR_down_cost_hist","aFRR_down_cost_sim_no_mFRR","aFRR_down_cost_sim_with_mFRR","sim_FR"])
plt.ylabel('aFRR costs in Euro')
plt.xlabel('Field test week')

plt.savefig('validation_and_analysis//aFRR_cost_validation.png')

plt.figure(3,figsize=(8, 6))
plt.plot(Vergleich_AEP_imbalance_price["18.11.2019"])
plt.legend(["imbalance_price_hist","imbalance_price_sim_no_mFRR","imbalance_price_sim_with_mFRR", "imbalance_price_sim_FR"])
plt.ylabel('imbalance price in Euro per MWh')
plt.xlabel('Field test week')

plt.savefig('validation_and_analysis//imbalance_price_validation.png')

plt.figure(4,figsize=(8, 6))
plt.plot(Vergleich_mFRR_pow["18.11.2019"])
plt.legend(["mFRR_up_pow_hist","mFRR_up_pow_sim_with_mFRR","sim_FR","mFRR_down_pow_hist","mFRR_down_pow_sim_with_mFRR","sim_FR"])
plt.ylabel('mFRR power in MW')
plt.xlabel('Field test week')

plt.savefig('validation_and_analysis//mFRR_pow_validation.png')

plt.show()