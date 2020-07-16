import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# New Antecedent/Consequent objects hold universe variables and membership
# functions
imbalance = ctrl.Antecedent(np.arange(-1001, 1001, 1), 'imbalance_MW')
netmargin = ctrl.Antecedent(np.arange(0, 101, 1), 'netmargin_Euro/MWh')

smartbalancing = ctrl.Consequent(np.arange(0, 101, 1), 'smartbalancing_percent')

# Auto-membership function population is possible with .automf(3, 5, or 7)
# imbalance.automf(7)
netmargin.automf(5)
smartbalancing.automf(5)

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
# define imbalance: wording and range
imbalance['neg_very_high'] = fuzz.trimf(imbalance.universe, [-1001, -1001, -700])
imbalance['neg_high'] = fuzz.trimf(imbalance.universe, [-1001, -700, -400])
imbalance['neg_low'] = fuzz.trimf(imbalance.universe, [-700, -400, 0])
imbalance['close_to_zero'] = fuzz.trimf(imbalance.universe, [-200, 0, 200])
imbalance['pos_low'] = fuzz.trimf(imbalance.universe, [0, 400, 700])
imbalance['pos_high'] = fuzz.trimf(imbalance.universe, [400, 700, 1001])
imbalance['pos_very_high'] = fuzz.trimf(imbalance.universe, [700, 1001, 1001])

# You can see how these look with .view()
# plt.figure(20)
# imbalance.view()
# plt.figure(21)
# netmargin.view()
# #flexibility.view()
# plt.figure(22)
# smartbalancing.view()

# to make these triangles useful, we define the fuzzy relationship between input and output variables.
# For the purposes of our example, consider three simple rules:
#  1.If the imbalance is neg_very_high OR the imbalance is pos_very_high, then smartbalancing will be good
#  2.If the imbalance is neg_high OR the imbalance is pos_high, then smartbalancing will be average
#  3.If the imbalance is neg_low OR the imbalance is pos_low, then smartbalancing will be mediocre
#  4.If the imbalance is close_to_zero, then smartbalancing will be poor

#  5.If the netmargin is poor, then smartbalancing will be poor
#  6.If the netmargin is mediocre, then smartbalancing will be mediocre
#  7.If the netmargin is average, then smartbalancing will be average
#  8.If the netmargin is decent, then smartbalancing will be decent
#  9.If the netmargin is good, then smartbalancing will be good


# the rules are fuzzy. Mapping the imprecise rules into a defined, actionable tip is a challenge.
# This is the kind of task at which fuzzy logic excels.
rule1 = ctrl.Rule(imbalance['neg_very_high'] | imbalance['pos_very_high'], smartbalancing['good'])
rule2 = ctrl.Rule(imbalance['neg_high'] | imbalance['pos_high'], smartbalancing['average'])
rule3 = ctrl.Rule(imbalance['neg_low'] | imbalance['pos_low'], smartbalancing['mediocre'])
rule4 = ctrl.Rule(imbalance['close_to_zero'], smartbalancing['poor'])

rule5 = ctrl.Rule(netmargin['poor'], smartbalancing['poor'])
rule6 = ctrl.Rule(netmargin['mediocre'], smartbalancing['mediocre'])
rule7 = ctrl.Rule(netmargin['average'], smartbalancing['average'])
rule8 = ctrl.Rule(netmargin['decent'], smartbalancing['decent'])
rule9 = ctrl.Rule(netmargin['good'], smartbalancing['good'])

# plt.figure(23)
# rule1.view()

# Now that we have our rules defined, we can simply create a control system via:
sb_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])

# In order to simulate this control system, create a ControlSystemSimulation.
# Object represents controller applied to a specific set of cirucmstances.
sb = ctrl.ControlSystemSimulation(sb_ctrl)


# ... Function integrated in grid model
def fuzz(imba, price, GKL):
    # new Function with GKL, use of FUZZY is implemented

    # define lists to buffer potential power and price of SB assets
    sb_pot = []
    sb_margin = []
    # define lists for output dictionary
    sb_activated_assets = []
    sb_real = []

    # iterate through input dictionary, find and store relevant sb assets
    for i, gk in enumerate(GKL.get('Price')):
        # print('Grenzkosten sind '+ str(gk)+' Euro')
        if gk < price:
            sb_margin.append(GKL.get('Power')[i] * (price - gk))
            sb_pot.append(GKL.get('Power')[i])

    # check if any relevant sb assets exist
    if sum(sb_pot) > 0:
        # Pass inputs to the FUZZY ControlSystem using Antecedent labels with Pythonic API
        sb.input['imbalance_MW'] = imba
        sb.input['netmargin_Euro/MWh'] = sum(sb_margin) / sum(sb_pot)
        # Crunch the numbers in FUZZY
        sb.compute()
        # print(sb_pot)
        sb_power = sum(sb_pot) * sb.output['smartbalancing_percent'] / 100
        # print(sb_power)

        # activation sb assets, full activation of cheap asset first until sb_power is reached
        for i, asset_power in enumerate(GKL.get('Power')):
            if sb_power > asset_power:
                sb_activated_assets.append(GKL.get('SB Asset ID')[i])
                sb_real.append(GKL.get('Power')[i])
                sb_power = sb_power - asset_power
            elif sb_power > 0:
                sb_activated_assets.append(GKL.get('SB Asset ID')[i])
                sb_real.append(sb_power)
                sb_power = 0

    # test some functionalities
    # for key,values in GKL.items():
    #    print('key ist "'+ key + '", mit den values' + str(values)+ ', die Anzahl ist also ' + str(len(values)))
    #    for i, value in enumerate(values):
    #        print('Value ' + str(i) +' ist ' +str(value))

    # define output dictionary
    SB_per_asset = {}
    SB_per_asset['SB Asset ID'] = sb_activated_assets
    SB_per_asset['SB_per_asset'] = sb_real

    return SB_per_asset





# ... Function integrated in grid model: Worst Case Scenario, including solely spread between AEP and DA prices
def Worst_case_Spread(imba, price, GKL, DA_price): # todo: insert
    # new Function with GKL, use of FUZZY is implemented

    # define lists to buffer potential power and price of SB assets
    sb_pot = []
    sb_margin = []
    # define lists for output dictionary
    sb_activated_assets = []
    sb_real = []

    # iterate through input dictionary, find and store relevant sb assets
    for i, gk in enumerate(GKL.get('Price')):
        # print('Grenzkosten sind '+ str(gk)+' Euro')
        spread = price - DA_price # price is AEP - todo: check
        if gk < spread:
            sb_margin.append(GKL.get('Power')[i] * (spread - gk)) #todo: check
            sb_pot.append(GKL.get('Power')[i])

    # check if any relevant sb assets exist
    if sum(sb_pot) > 0:
        # Pass inputs to the FUZZY ControlSystem using Antecedent labels with Pythonic API
        sb.input['imbalance_MW'] = imba
        sb.input['netmargin_Euro/MWh'] = sum(sb_margin) / sum(sb_pot)
        # Crunch the numbers in FUZZY
        sb.compute()
        # print(sb_pot)
        sb_power = sum(sb_pot) * sb.output['smartbalancing_percent'] / 100
        # print(sb_power)

        # activation sb assets, full activation of cheap asset first until sb_power is reached
        for i, asset_power in enumerate(GKL.get('Power')):
            if sb_power > asset_power:
                sb_activated_assets.append(GKL.get('SB Asset ID')[i])
                sb_real.append(GKL.get('Power')[i])
                sb_power = sb_power - asset_power
            elif sb_power > 0:
                sb_activated_assets.append(GKL.get('SB Asset ID')[i])
                sb_real.append(sb_power)
                sb_power = 0

    # test some functionalities
    # for key,values in GKL.items():
    #    print('key ist "'+ key + '", mit den values' + str(values)+ ', die Anzahl ist also ' + str(len(values)))
    #    for i, value in enumerate(values):
    #        print('Value ' + str(i) +' ist ' +str(value))

    # define output dictionary
    SB_per_asset = {}
    SB_per_asset['SB_Asset_ID'] = sb_activated_assets
    SB_per_asset['SB_per_asset'] = sb_real

    return SB_per_asset




# ... Berechnung der zusätzlichen Kosten aus Lastverschiebung
def Costs_Lastverschiebung_calc(ID, t_start, t_end, P_old, P_new):
    t_old = t_end - t_start
    E = P_old * t_old
    t_new = E/(P_new)
    K_old = Costs_calc(ID, t_start, t_end, P_old)
    K_new = Costs_calc(ID, t_start, t_start + t_new, P_new)
    dK = K_new - K_old
    return dK



def Costs_calc(ID, t_start, t_end, P):
    dt = 1
    K_t = list()
    for i in range(t_start,t_end):
        K_t[i] = ID[i] * P * dt
        K = K_t[i] + K
    return K

