import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# New Antecedent/Consequent objects hold universe variables and membership
# functions
imbalance = ctrl.Antecedent(np.arange(-1001, 1001, 1), 'imbalance_MW')
p_average =ctrl.Antecedent(np.arange(-1001,1001,1), "p_average_MW")
netmargin = ctrl.Antecedent(np.arange(0, 101, 1), 'netmargin_Euro/MWh')
time = ctrl.Antecedent(np.arange(0, 15, 1), 'time_min')
d_Imba = ctrl.Antecedent(np.arange(-1001, 1001, 1), 'd_imba_MW')
s_Imba = ctrl.Antecedent(np.arange(0, 1, 1), 's_imba')

smartbalancing = ctrl.Consequent(np.arange(0, 101, 1), 'smartbalancing_percent')

# Auto-membership function population is possible with .automf(3, 5, or 7)
netmargin.automf(5)
smartbalancing.automf(5)
d_Imba.automf(5)


# Custom membership functions can be built interactively with a familiar,
# Pythonic API

# define time: wording and range
time['early'] = fuzz.trimf(time.universe, [0, 0, 7])
time['middle'] = fuzz.trimf(time.universe, [0,7,14])
time['late'] = fuzz.trimf(time.universe, [7,14,14])

# define imbalance: wording and range
imbalance['neg_high'] = fuzz.trimf(imbalance.universe, [-1001, -1001, -700])
imbalance['neg_average'] = fuzz.trimf(imbalance.universe, [-1001, -500, -200])
imbalance['close_to_zero'] = fuzz.trimf(imbalance.universe, [-300, 0, 300])
imbalance['pos_average'] = fuzz.trimf(imbalance.universe, [200, 500, 1001])
imbalance['pos_high'] = fuzz.trimf(imbalance.universe, [700, 1001, 1001])

# define p_average: wording and range
p_average['neg_high'] = fuzz.trimf(p_average.universe, [-1001, -1001, -700])
p_average['neg_average'] = fuzz.trimf(p_average.universe, [-1001, -500, -200])
p_average['close_to_zero'] = fuzz.trimf(p_average.universe, [-300, 0, 300])
p_average['pos_average'] = fuzz.trimf(p_average.universe, [200, 500, 1001])
p_average['pos_high'] = fuzz.trimf(p_average.universe, [700, 1001, 1001])

# define delta imbalance: wording and range
d_Imba['neg_high'] = fuzz.trimf(d_Imba.universe, [-1001, -1001, -300])
d_Imba['neg_average'] = fuzz.trimf(d_Imba.universe, [-400, -50, 0])
d_Imba['close_to_zero'] = fuzz.trimf(d_Imba.universe, [-50, 0, 50])
d_Imba['pos_average'] = fuzz.trimf(d_Imba.universe, [0, 50, 400])
d_Imba['pos_high'] = fuzz.trimf(d_Imba.universe, [300, 1001, 1001])


# define delta imbalance singe: wording and range
s_Imba['change'] = fuzz.trimf(s_Imba.universe, [0, 1, 1])
s_Imba['nochange'] = fuzz.trimf(s_Imba.universe, [0, 0, 1])


# You can see how these look with .view()
time.view()
plt.figure(1)
imbalance.view()
plt.figure(2)
netmargin.view()
plt.figure(3)
smartbalancing.view()
plt.figure(4)


# to make these triangles useful, we define the fuzzy relationship between input and output variables.
# the rules are fuzzy. Mapping the imprecise rules into a defined, actionable sb contribution is a challenge.
# This is the kind of task at which fuzzy logic excels.

# Netmargin based rules
rule1 = ctrl.Rule(netmargin['poor'], smartbalancing['poor'])
rule2 = ctrl.Rule(netmargin['mediocre'], smartbalancing['mediocre'])
rule3 = ctrl.Rule(netmargin['average'], smartbalancing['average'])
rule4 = ctrl.Rule(netmargin['decent'], smartbalancing['decent'])
rule5 = ctrl.Rule(netmargin['good'], smartbalancing['good'])

# Risk based rules depend on Market design
# Risk means risk of changing sign of the imbalance price! Risk of decreasing imbalance price is neglected
# time and p_average (single price) or imbalance (Dutch approach: combi of single and dual price)
# for dual price, the risk of a changing sign does not exist -> no risk based rules!

# Time dependend risk rules for single price and Dutch approach (combi of single and dual price)
# . . . in the beginning the risk of changing sign is high
# . . . in the end situation is much more certain
rulet1 = ctrl.Rule(time['early'], smartbalancing['mediocre'])
rulet2 = ctrl.Rule(time['middle'], smartbalancing['mediocre'])
# step 3,4 and 5 differ depending on clearing scheme (s single vs. NL combined approach)
rulets3 = ctrl.Rule(time['late']&(p_average['neg_average']|p_average['pos_average']), smartbalancing['mediocre'])
rulets4 = ctrl.Rule(time['late']&(p_average['neg_high']| p_average['pos_high']), smartbalancing['average'])
rulets5 = ctrl.Rule(time['late']&p_average['close_to_zero'],smartbalancing['poor'])
ruletNL3 = ctrl.Rule(time['late']&(imbalance['neg_average']|imbalance['pos_average']), smartbalancing['mediocre'])
ruletNL4 = ctrl.Rule(time['late']&(imbalance['neg_high']| imbalance['pos_high']), smartbalancing['average'])
ruletNL5 = ctrl.Rule(time['late']&imbalance['close_to_zero'],smartbalancing['poor'])

# p_average based risk rules for single pricing
rules1 = ctrl.Rule(p_average['neg_high'] | p_average['pos_high'], smartbalancing['good'])
rules2 = ctrl.Rule(p_average['neg_average'] | p_average['pos_average'], smartbalancing['decent'])
rules3 = ctrl.Rule(p_average['close_to_zero'], smartbalancing['poor'])

# Imbalance based risk rules for Dutch approach
ruleNL1 = ctrl.Rule(imbalance['neg_high'] | imbalance['pos_high'], smartbalancing['good'])
ruleNL2 = ctrl.Rule(imbalance['neg_average'] | imbalance['pos_average'], smartbalancing['decent'])
ruleNL3 = ctrl.Rule(imbalance['close_to_zero'], smartbalancing['poor'])

# delta imba rules: if change is high, SB is poor (uncertanty)
rulei1 = ctrl.Rule(d_Imba['neg_high'] | d_Imba['pos_high'], smartbalancing['poor'])
rulei2 = ctrl.Rule(d_Imba['neg_average'] | d_Imba['pos_average'], smartbalancing['decent'])
rulei3 = ctrl.Rule(d_Imba['close_to_zero'], smartbalancing['good'])

# delta imba sign rules: if change is high, SB is poor (uncertanty)
rulesg1 = ctrl.Rule(s_Imba['change'] , smartbalancing['poor'])
#rulesg2 = ctrl.Rule(s_Imba['nochange'] , smartbalancing['good'])


# Now that we have our rules defined, we can create a control system per pricing scheme (single vs. dual vs. NL) via:
# for dual pricing
sb_ctrl_dual = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])

# for single pricing
sb_ctrl_single = ctrl.ControlSystem([ rulet1, rulet2, rulets3, rulets4, rulets5, rules1, rules2, rules3])
#rule1, rule2, rule3, rule4, rule5,

# for Dutch approach
sb_ctrl_NL = ctrl.ControlSystem([rulet1, rulet2, ruletNL3, ruletNL4, ruletNL5, ruleNL1, ruleNL2, ruleNL3,rulei1,rulei2,rulei3, rulesg1])
#rule1, rule2, rule3, rule4, rule5,

# In order to simulate this control system, create a ControlSystemSimulation.
# Object represents controller applied to a specific set of cirucmstances.
sb_dual = ctrl.ControlSystemSimulation(sb_ctrl_dual)
sb_single = ctrl.ControlSystemSimulation(sb_ctrl_single)
sb_NL = ctrl.ControlSystemSimulation(sb_ctrl_NL)

# Function to call fuzzy
def fuzz(Marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba, Time, p_average, pricing, sb_P, Flexpotential):
#def fuzz(Marge, Imba, Time, p_average, pricing): #imba, price, GKL):
    # Pass inputs to the FUZZY ControlSystem using Antecedent labels with Pythonic API

    #Vorzeichen bestimmen
    if old_d_Imba > 0 and d_Imba > 0:
        s_Imba = 0
    elif old_d_Imba < 0 and d_Imba < 0:
        s_Imba = 0
    else:
        s_Imba = 1

    #calculate individual parameter
    Imba = FRCE_sb - sb_P

#calculate ratio to limit SB of assets with Flexpotential higher Imba
    if Imba == 0:
        ratio = 1
    else:
        ratio = (Flexpotential)/Imba

    if ratio < 1:
        ratio = 1

 # change input data, in case values are out of fuzzy membership functions
    if Marge > 100:
        Marge = 100

    if Marge < 0:
        Marge = 0

    if Imba >1000:
        Imba = 1000

    if Imba < -1000:
        Imba = -1000

    if p_average > 1000:
        p_average = 1000

    if p_average < -1000:
        p_average = -1000

#classical dual pricing does not include the risk of decreasing imbalance price or changing sign of imbalance price
#therefore, only the netmergin is considered as profit. no risk evalution via imbalance or time
    if pricing == "dual":
        #sb_dual.input['imbalance_MW'] = Imba
        sb_dual.input['netmargin_Euro/MWh'] = Marge
        #sb_dual.input['time_min'] = Time

        # Crunch the numbers in FUZZY
        sb_dual.compute()

        return(sb_dual.output['smartbalancing_percent'] / 100)

    if pricing == 0:
        #sb_single.input['imbalance_MW'] = Imba
        #sb_single.input['netmargin_Euro/MWh'] = Marge
        sb_single.input['time_min'] = Time
        sb_single.input['p_average_MW'] = p_average

        # Crunch the numbers in FUZZY
        sb_single.compute()

        return (sb_single.output['smartbalancing_percent'] / (100*ratio))

    if pricing == 1:
        #sb_NL.input['imbalance_MW'] = Imba
        #sb_NL.input['netmargin_Euro/MWh'] = Marge
        sb_NL.input['time_min'] = Time
        sb_NL.input['imbalance_MW'] = Imba
        sb_NL.input['d_imba_MW'] = d_Imba
        sb_NL.input['s_imba'] = s_Imba
        # Crunch the numbers in FUZZY
        sb_NL.compute()

        return (sb_NL.output['smartbalancing_percent'] / (100*ratio))

#plt.show()