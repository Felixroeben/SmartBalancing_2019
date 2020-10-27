import pandas as pd
import matplotlib.pyplot as plt
import os

# ===============================================================================
# Identify location of files and set path
# ===============================================================================
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path_1 = "results/1 no SB/WC_sim_output_period.csv"
rel_path_2 = "results/1 no SB/WC_sim_output_all.csv"
abs_file_path_period = os.path.join(script_dir, rel_path_1)
abs_file_path_all = os.path.join(script_dir, rel_path_2)

# ===============================================================================
# Load reference scenario 15 min (period)
# ===============================================================================
reference_data = pd.read_csv(abs_file_path_period,sep=';',encoding='latin-1').round(1)
reference_data.index = pd.date_range(start='00:00 01.01.2019', end = '23:30 12.31.2019',freq='15 min')
reference_sum = reference_data.sum()

# ===============================================================================
# Load reference scenario 1 min (all)
# ===============================================================================
reference_data_all = pd.read_csv(abs_file_path_all,sep=';',encoding='latin-1').round(1)
reference_data_all.index = pd.date_range(start='00:00 01.01.2019', end = '23:59 12.31.2019',freq='1 min')

# ===============================================================================
# Load scenario 15 min (
# ===============================================================================
scenario_data = pd.read_csv("results/2 All NL/WC_sim_output_period.csv",sep=';',encoding='latin-1').round(1)
scenario_data.index = pd.date_range(start='00:00 01.01.2019', end = '23:30 12.31.2019',freq='15 min')

# ===============================================================================
# Load scenario 1 min
# ===============================================================================
scenario_data_all = pd.read_csv("results/2 All NL/WC_sim_output_all.csv",sep=';',encoding='latin-1').round(1)
scenario_data_all.index = pd.date_range(start='00:00 01.01.2019', end = '23:59 12.31.2019',freq='1 min')

# ===============================================================================
# Show scenario
# ===============================================================================

start = ["2019-01-01 0:00", "2019-02-01 0:00"]
end = ["2019-01-01 1:30", "2019-02-01 1:30"]

for i in range(len(start)):
        scenario_data_all[start[i]:end[i]].drop(['time [s]','f [Hz]','aFRR FRCE (open loop) [MW]','mFRR P [MW]','Unnamed: 11'],axis=1).plot(secondary_y='AEP [EUR/MWh]')
        reference_data_all[start[i]:end[i]].drop(['time [s]','f [Hz]','aFRR FRCE (open loop) [MW]','mFRR P [MW]','Unnamed: 11'],axis=1).plot(secondary_y='AEP [EUR/MWh]')


# ===============================================================================
# Calculate Balancers Profit
# ===============================================================================
scenario_sum = scenario_data.sum()

income_all = {}
income_all['Solar'] = [scenario_sum['Solar AEP costs [EUR]'] ]#- scenario_sum['Solar Marktprämie [EUR]']]
income_all['Wind onshore'] = [scenario_sum['Wind onshore AEP costs [EUR]']]# - scenario_sum['Wind onshore Marktprämie [EUR]']]
income_all['Wind offshore'] = [scenario_sum['Wind offshore AEP costs [EUR]']]# - scenario_sum['Wind offshore Marktprämie [EUR]']]
income_all['Alu'] = [scenario_sum['Aluminium AEP costs [EUR]']]
income_all['Alu'] = [scenario_sum['Aluminium AEP costs [EUR]']]
income_all['Steel'] = [scenario_sum['Steel AEP costs [EUR]']]
income_all['Cement'] = [scenario_sum['Cement AEP costs [EUR]']]
income_all['Paper'] = [scenario_sum['Paper AEP costs [EUR]']]
income_all['Chlorine'] = [scenario_sum['Chlorine AEP costs [EUR]']]
income_all['Gas'] = [scenario_sum['Gas AEP costs [EUR]']]

#header = ['Solar', 'Wind onshore', 'Wind offshore', 'Alu, Steel', 'Cement', 'Paper', 'Chlorine', 'Gas']
data = pd.DataFrame.from_dict(income_all, orient='index')
print('------------------------------------------------------------------')
print('PROFITS BY TECHNOLOGY')
print('------------------------------------------------------------------')
print('The balancers profit in kEUR')
print((data/1000).round(1))
print('------------------------------------------------------------------')


# ===============================================================================
# Calculate Overall System Impact
# ===============================================================================
# compare positive and negative balancing power of ref and sce
aFRR_pos = scenario_sum['GER pos. energy aFRR [MWh]'] / reference_sum['GER pos. energy aFRR [MWh]']
aFRR_neg = scenario_sum['GER neg. energy aFRR [MWh]'] / reference_sum['GER neg. energy aFRR [MWh]']
mFRR_pos = scenario_sum['GER pos. energy mFRR [MWh]'] / reference_sum['GER pos. energy mFRR [MWh]']
mFRR_neg = scenario_sum['GER neg. energy mFRR [MWh]'] / reference_sum['GER neg. energy mFRR [MWh]']
print('POWER')
print('------------------------------------------------------------------')
print('Positive aFRR could be reduced by: ', aFRR_pos.round(2))
print('Negative aFRR could be reduced by: ', aFRR_neg.round(2))
print('------------------------------------------------------------------')
print('Positive mFRR could be reduced by: ', mFRR_pos.round(2))
print('Negative mFRR could be reduced by: ', mFRR_neg.round(2))
print('------------------------------------------------------------------')
# ===============================================================================
# Calculate Overall System Costs
# ===============================================================================
# compare balancing costs of ref and sce
#todo: Warum sind die Kosten für neg manchmal positiv und manchmal negativ?
# Bekomme Energie und bezahle dafür? Sind das dann die negativen Kosten? Also hauptsächlich Einnahmen auf dieser Seite? oO
# Erwartet wird dann ein
costs_pos = (scenario_sum['GER pos. aFRR costs [EUR]'] + scenario_sum['GER pos. mFRR costs [EUR]']) / (reference_sum['GER pos. aFRR costs [EUR]'] + reference_sum['GER pos. mFRR costs [EUR]'])
costs_neg = (scenario_sum['GER neg. aFRR costs [EUR]'] + scenario_sum['GER neg. mFRR costs [EUR]']) / (reference_sum['GER neg. aFRR costs [EUR]'] + reference_sum['GER neg. mFRR costs [EUR]'])
costs_tot = (scenario_sum['GER pos. aFRR costs [EUR]'] + scenario_sum['GER pos. mFRR costs [EUR]'] + scenario_sum['GER neg. aFRR costs [EUR]'] + scenario_sum['GER neg. mFRR costs [EUR]']) / (reference_sum['GER pos. aFRR costs [EUR]'] + reference_sum['GER pos. mFRR costs [EUR]'] + reference_sum['GER neg. aFRR costs [EUR]'] + reference_sum['GER neg. mFRR costs [EUR]'])
print('COSTS')
print('------------------------------------------------------------------')
print('Pos balancing costs could be reduced by: ', costs_pos.round(2))
print('Neg balancing costs could be reduced by: ', costs_neg.round(2))
print('Total balancing costs could be reduced by: ', costs_tot.round(2))
print('------------------------------------------------------------------')

# ===============================================================================
# Calculate Balancers System Impact
# ===============================================================================
# compare signe of imba and contribution
#todo: Woher kommen die Inputs zur Analyse, welche Technologie wann richtig stand?
print('The impact of the single technologies on system stability is as follows: ')
print('Income.sum()')

plt.show()
print('hi')