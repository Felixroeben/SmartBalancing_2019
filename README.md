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

## Data handling:
For the initialization of the simulation (see fileexch.py), the following csv files must be provided:
### General data in the 2019_data folder
ACE_2019.csv in 1 minute resolution in ACE folder
MRL merit order lists in 4 hour resolution in MRL_MOL folder
SRL merit order lists in 4 hour resolution in SRL_MOL folder
Day-ahead Prices_2019.csv 
generation_per_type_2019.csv 

### For each scenario in a scenario folder
#### Balancing_groups.csv
columns: name, name load, name generator, name flex load, name flex generator, bool smart

all balancing groups are defined here (name). (multiple) load, generator, flex load and flex generator can be added 
to each balancing group. bool smart defines if balagroup contributes to smart balancing or not.

#### SB_Assets.csv
columns: name, ramp rate (pos and neg), flex potential (max and min), costs (Euro/MWh), Balancing Group, class

Assets and their behaviour are described. The class is defined (GeneratorFlex, LoadFlex, SmartBalancingAsset)

SB Assets with class GeneratorFlex and LoadFlex do not need further

Consumption_schedule.csv: load schedule for all balancing groups in 1 min resolution (even if allways 0)
Consumption.csv: consumption of balancing groups in 1 min resolution (only if applicable)
Generation_schedule.csv: generation schedule for all balancing groups in 1 min resolution (even if allways 0)
Generation.csv: generation of balancing groups in 1 min resolution (only if applicable)



## object oriented program - introduction of class structure

The tool is programmed object oriented. The class structure is defined in the following parts of the programm:

### gridelem.py
An object of the class 'SynchronousZone' is not to be subordinated to other grid elements.
The unique property of a synchronous zone is the system-wide grid frequency f.
A synchronous zone is made up of subordinated grid elements.

The generic class 'GridElement' can be used for all kinds of grid structures
like Coordination Centers, Control Blocks, or Control Areas.
An object of the class 'GridElement' contains subordinated grid elements to which it passes its methods.
No true calculations are executed in the class 'GridElement'.

'CalculatingGridElement' can be used for Coordination Centers, Control Blocks, and Control Areas.
Variables for load flow, FCR, and aFRR are calculated by the respective methods.
An object of the class 'CalculatingGridElement' does not have any subordinated grid elements.

The class 'ControlArea' is to be used for Control Areas with subordinated Balancing Groups.
The class largely corresponds the class 'CalculatingGridElement'.

### balagroup.py

class BalancingGroup

### generato.py

class Generator
class GeneratorFlex(Generator)

### loadload.py

class Load
class LoadFlex(Load)

### smarbala.py

class SmartBalancingAsset


