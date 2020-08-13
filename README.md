# Smart Balancing 2019

New repository. Copy from Feldtest_Scenario 
(Simulation of NEW 4.0 Fieldtest: Smart Balancing by 5 real Balancing Groups in Hamburg / Schleswig-Holstein
in the week 18.11.2019 to 24.11.2019 in 1s resolution and effect on German balancing demand/costs)

The "Smart Balancing 2019" grid model aims at further analyse different balancing market approaches. 
In contrast to the fieldtest, the complete Smart Balancing contribution of all generation units and of the industrie is 
under consideration.

Real data from 2019 is used: 
German ACE in 1 min resolution (www.regelleistung.net - SRL_sollwert + MRL activation + emergency reserves)
Generation per technology in 15 min resolution (www.transparency.entsoe.eu/)
Day-Ahead market price for electrical energy in 1 hour resolution (www.transparency.entsoe.eu/)
Price for gas, oil and coal in 1 day resolution (www.finanzen.net)

Data handling:
For the initialization of the simulation (see fileexch.py), the following csv files must be provided:
Balancing_groups.csv
Consumption_schedule.csv
Consumption.csv
Generation_schedule.csv
Generation.csv
SB_Assets.csv


