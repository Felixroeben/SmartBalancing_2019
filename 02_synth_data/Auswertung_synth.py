# ===============================================================================
# Auswertung.py
# Analysis and plots belonging to Smart Balancing Simulation (SBS)
# Define location and name of folders with SBS time series (output csv-files):
# 'WC_sim_output_all.csv' and 'WC_sim_output_period.csv'
# ===============================================================================

import pandas as pd
import matplotlib.pyplot as plt

# ===============================================================================
# define location and name of files to set path
# ===============================================================================

location = "results/"
#location = "results_sin/"
#location = "results_5d/"
#location = "results_1d/"

if location == "results/":
        scenario_files = ['6 no SB PAB','7 DEs', '8 NLs','9 no SB MP','10 BEPP15','11 BEPP1']
        scenario_path = ['6 no SB PAB','7 DEs', '8 NLs','9 no SB MP','10 BEPP15','11 BEPP1']

if location == "results_sin/" or location == "results_1d/":
        scenario_files = ['1 no SB','4 DE'] #['1 no SB','4 DE', '5 NL']
        scenario_path = ['1 no SB','4 DE'] #['1 no SB','4 DE', '5 NL']

# ===============================================================================
#define start and end of example plots
# ===============================================================================
example_plot = True
if location == "results_sin/" or location == "results_1d/" or location == "results/":
        start = ["2019-01-01 5:00","2019-01-01 9:00","2019-01-01 14:25"]
        end = ["2019-01-01 7:45","2019-01-01 9:45","2019-01-01 15:45"]

if location == "results/x":
        start = ["2019-06-12 10:00"]
        end = ["2019-06-12 14:45"]

if location == "XXresults_1d/":
        start = ["2019-01-01 14:25"]
        end = ["2019-01-01 14:45"]
# ===============================================================================
#define start and end of simulation for time stamp index of /WC_sim_output_all.csv'
# ===============================================================================

sim_start = '00:00 01.01.2019'

if location == "results_5d/":
        sim_end_all = '23:59 01.05.2019'
elif location == "results_1d/":
        sim_end_all = '23:59 01.01.2019'
else:
        sim_end_all = '23:59 01.31.2019'


# ===============================================================================
#no further definitions needed
# ===============================================================================
#init lists and dataframe for calculations
# ===============================================================================
scenario_data = list()
#scenario_data_period = list()
scenario_sum = list()
minute_sum = list()

scenario_sum_df = pd.DataFrame()
frequency_df = pd.DataFrame()

for j in range(len(scenario_files)):

        #read "period" csv files with ISP resolution (15min)
        scenario_path[j]= location+scenario_files[j]+'/synth_sim_output_period.csv'

        #print('Scenario: ',scenario_path[j])
        scenario_period = pd.read_csv(scenario_path[j], sep=';', encoding='latin-1').round(1)

        #read "all" csv file with all timesteps in 1 min resolution
        scenario_path[j] = location + scenario_files[j] + '/synth_sim_output_all.csv'
        minute_data = pd.read_csv(scenario_path[j], sep=';', encoding='latin-1')

        print('Data load completed: ', scenario_path[j])

        names = ['Solar', 'Wind onshore', 'Wind offshore', 'Aluminium', 'Steel', 'Cement', 'Paper', 'Chlorine','Gas']

        minute_sum.append(minute_data.sum())
        minute_data.index = pd.date_range(start=sim_start, end=sim_end_all, freq='1 min')
        scenario_data.append(minute_data)

        for name in names:
                Dict_scenario_period = dict()
                Dict_scenario_period['costs'] = scenario_period[name + ' AEP costs [EUR]'].copy()
                Dict_scenario_period['AEP'] = scenario_period['GER AEP [EUR/MWh]'].copy()
                # Kosten / AEP = Energy
                Dict_scenario_period[name] = Dict_scenario_period['costs'] / Dict_scenario_period['AEP']
                scenario_period[name] = Dict_scenario_period[name]

        #scenario_period.index = pd.date_range(start='00:00 01.01.2019', end='23:30 01.05.2019', freq='15 min')
        #scenario_data_period.append(scenario_period)

# # ===============================================================================
# # Show Example Plot with 1 min resolution
# # ===============================================================================
        if example_plot:
                for i in range(len(start)):
                        scenario_data[j][start[i]:end[i]].drop(
                                ['time [s]', 'f [Hz]', 'aFRR FRCE (open loop) [MW]','Unnamed: 20'],
                                axis=1).plot(secondary_y='AEP [EUR/MWh]', title='Scenario ' + scenario_files[j])

# ===============================================================================
# Calculate Balancers Profit
# ===============================================================================
        # list for calculations in loop
        scenario_sum.append(scenario_period.sum())
        # dataframe for bar plot after loop
        scenario_sum_df[scenario_files[j]] = scenario_period.sum()

        #save values from reference scenario "1 no SB"
        if j == 0 or j == 3:
                reference_sum = scenario_sum[j]

        income_all = {}
        income_all['Solar'] = [scenario_sum[j]['Solar AEP costs [EUR]'] ]#- scenario_sum['Solar Marktprämie [EUR]']]
        income_all['Wind onshore'] = [scenario_sum[j]['Wind onshore AEP costs [EUR]']]# - scenario_sum['Wind onshore Marktprämie [EUR]']]
        income_all['Wind offshore'] = [scenario_sum[j]['Wind offshore AEP costs [EUR]']]# - scenario_sum['Wind offshore Marktprämie [EUR]']]
        income_all['Alu'] = [scenario_sum[j]['Aluminium AEP costs [EUR]']]
        income_all['Alu'] = [scenario_sum[j]['Aluminium AEP costs [EUR]']]
        income_all['Steel'] = [scenario_sum[j]['Steel AEP costs [EUR]']]
        income_all['Cement'] = [scenario_sum[j]['Cement AEP costs [EUR]']]
        income_all['Paper'] = [scenario_sum[j]['Paper AEP costs [EUR]']]
        income_all['Chlorine'] = [scenario_sum[j]['Chlorine AEP costs [EUR]']]
        income_all['Gas'] = [scenario_sum[j]['Gas AEP costs [EUR]']]

        header_energy = []
        header_price = []
        for name in names:
                energy = minute_sum[j][name + ' Power [MW]']
                costs = scenario_sum[j][name+ ' AEP costs [EUR]']
                print(name, ' Profit: ', (-costs/1000).round(1), ' kEUR')
                print(name, ' energy: ', (energy/60).round(1), ' MWh')
                income_all[name+' Energy'] = energy
                income_all[name+ ' spc. costs [EUR/MWh]'] = costs / (energy/60)
                header_price.append(name+ ' spc. costs [EUR/MWh]')
                header_energy.append(name+' Energy')

        #header = ['Solar', 'Wind onshore', 'Wind offshore', 'Alu, Steel', 'Cement', 'Paper', 'Chlorine', 'Gas']
        data = pd.DataFrame.from_dict(income_all) #, orient='index')

        show_data_energy = data[header_energy].T
        show_data_price = data[header_price].T
        print('------------------------------------------------------------------')
        print('Scenario ',scenario_files[j],': PROFITS BY TECHNOLOGY')
        print('------------------------------------------------------------------')
        print('The balancers specific energy purchase costs in EUR/MWh')
        print((show_data_price).round(1))
        print('------------------------------------------------------------------')
        print('The balancers energy purchase in MWh')
        print((show_data_energy).round(1))
        print('------------------------------------------------------------------')


# ===============================================================================
# Calculate Overall System Impact
# ===============================================================================
# compare positive and negative balancing power of ref and sce
        aFRR_pos = scenario_sum[j]['GER pos. energy aFRR [MWh]'] / reference_sum['GER pos. energy aFRR [MWh]']
        aFRR_neg = scenario_sum[j]['GER neg. energy aFRR [MWh]'] / reference_sum['GER neg. energy aFRR [MWh]']
        mFRR_pos = scenario_sum[j]['GER pos. energy mFRR [MWh]'] / reference_sum['GER pos. energy mFRR [MWh]']
        mFRR_neg = scenario_sum[j]['GER neg. energy mFRR [MWh]'] / reference_sum['GER neg. energy mFRR [MWh]']
        print('Scenario ',scenario_files[j],': POWER')
        print('------------------------------------------------------------------')
        print('Positive aFRR could be reduced to: ', aFRR_pos.round(2)*100,'% of the reference simulation')
        print('Negative aFRR could be reduced to: ', aFRR_neg.round(2)*100,'% of the reference simulation')
        print('------------------------------------------------------------------')
        print('Positive mFRR could be reduced to: ', mFRR_pos.round(2)*100,'% of the reference simulation')
        print('Negative mFRR could be reduced to: ', mFRR_neg.round(2)*100,'% of the reference simulation')
        print('------------------------------------------------------------------')

# ===============================================================================
# Calculate Overall System Costs
# ===============================================================================
# compare balancing costs of ref and sce
        costs_pos = (scenario_sum[j]['GER pos. aFRR costs [EUR]'] + scenario_sum[j]['GER pos. mFRR costs [EUR]']) / (reference_sum['GER pos. aFRR costs [EUR]'] + reference_sum['GER pos. mFRR costs [EUR]'])
        costs_neg = (scenario_sum[j]['GER neg. aFRR costs [EUR]'] + scenario_sum[j]['GER neg. mFRR costs [EUR]']) / (reference_sum['GER neg. aFRR costs [EUR]'] + reference_sum['GER neg. mFRR costs [EUR]'])
        costs_tot = (scenario_sum[j]['GER pos. aFRR costs [EUR]'] + scenario_sum[j]['GER pos. mFRR costs [EUR]'] + scenario_sum[j]['GER neg. aFRR costs [EUR]'] + scenario_sum[j]['GER neg. mFRR costs [EUR]']) / (reference_sum['GER pos. aFRR costs [EUR]'] + reference_sum['GER pos. mFRR costs [EUR]'] + reference_sum['GER neg. aFRR costs [EUR]'] + reference_sum['GER neg. mFRR costs [EUR]'])
        print('Scenario ',scenario_files[j],': COSTS')
        print('------------------------------------------------------------------')
        print('Pos balancing costs could be reduced to: ', costs_pos.round(2)*100,'% of the reference simulation')
        print('Neg balancing costs could be reduced to: ', costs_neg.round(2)*100,'% of the reference simulation')
        print('Total balancing costs could be reduced to: ', costs_tot.round(2)*100,'% of the reference simulation')
        print('------------------------------------------------------------------')

# ===============================================================================
# Calculate Balancers Impact on System Frequency (Rest of Europe = 300 GW and balanced)
# ===============================================================================
# compare contribution to frequency deviation
        # dataframe for bar plot after loop
        frequency_df[scenario_files[j]] = scenario_data[j].std()
        # save values from reference scenario "1 no SB"
        if j == 0:
                frequency_ref = scenario_data[j]['f [Hz]'].std()

        frequency_all = {}
        frequency_all[scenario_files[j], ' f Mean in Hz'] = scenario_data[j]['f [Hz]'].mean()
        frequency_all[scenario_files[j],' f std in Hz']= scenario_data[j]['f [Hz]'].std()
        frequency_all[scenario_files[j], ' f min in Hz'] = scenario_data[j]['f [Hz]'].min()
        frequency_all[scenario_files[j], ' f max in Hz'] = scenario_data[j]['f [Hz]'].max()

        print('Scenario ', scenario_files[j], ': FREQUENCY')
        print('------------------------------------------------------------------')
        print('f Mean: ', frequency_all[scenario_files[j], ' f Mean in Hz'], ' Hz')
        print('f Std: ', frequency_all[scenario_files[j], ' f std in Hz'].round(6), ' Hz')
        print('f min: ', frequency_all[scenario_files[j], ' f min in Hz'].round(3), ' Hz')
        print('f max: ', frequency_all[scenario_files[j], ' f max in Hz'].round(3), ' Hz')
        print('------------------------------------------------------------------')
        print('------------------------------------------------------------------')
# ===============================================================================
#todo: Inputs zur Analyse, welche Technologie wann richtig stand?
#todo: sign of imba vs. sign of SB per technology
#print('The impact of the single technologies on system stability is as follows: ')
#print('Income.sum()')

# ===============================================================================
# Bar-Plot with Comparison of all Scenarios (balancing energy and costs)
# ===============================================================================
Energie_Summen = scenario_sum_df.filter(['GER pos. energy aFRR [MWh]', 'GER neg. energy aFRR [MWh]', 'GER pos. energy mFRR [MWh]', 'GER neg. energy mFRR [MWh]'], axis=0)/1000
Energie_Summen.plot.bar(title='Comparison of Balancing Energy')
plt.ylabel('balancing energy in GWh')

Kosten_Summen = scenario_sum_df.filter(['GER pos. aFRR costs [EUR]','GER neg. aFRR costs [EUR]', 'GER pos. mFRR costs [EUR]','GER neg. mFRR costs [EUR]'], axis=0)/1000000
Kosten_Summen.plot.bar(title='Comparison of Costs')
plt.ylabel('costs in mio. €')

plt.show()
