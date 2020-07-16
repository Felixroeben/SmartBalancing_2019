# new test scenario - three power plants with 1 GW flexibility each
# Version 1.0 - first functional test run 29.05.2020
#todo: check time dependend rules in fuzzlogi_marketdesign
#todo: number of flexible assets
#todo: calculate imbalance price from MOL (define MOL)

# approach: test fuzzy smart balancing feedback loop j periods of 15 minutes
# and 3 market participants with 1 GW flexibility each

import fuzzlogi_marketdesign
import pandas as pd
import matplotlib.pyplot as plt

#set length of simulation: number of ISPs 1 -> 15 minutes; 4 -> 60 minutes etc.
length = 4

# pricing represents the market design
# "dual" for dual imbalance princing
# "single" for single imbalance pricing and
# "NL" for combination of single and dual imbalance price (in case of overcompensation)
pricing = "single"

#clearing represents the market design
# "marginal" for marginal pricing
# "pay_as_bid" for pay-as-bid
clearing = "marginal"

# not considered is the risk of decreasing imbalance price, wich exists with pay_as_bid pricing scheme
# This risk is neglected, because it is covered by the Netmargin based rules
# only the risk of changing sign is a limiting factor
# pay_as_bid (average of bids define imbalance price -> can decrease)
# marginal costs (highest bid defines imbalance price -> cannot decrease)

# First simple test scenario with constant imbalance: imba = 1 GW
imba = 1000

#SB contribution per cluster is limited to max_ramp (0.2 means 200 MW/min per asset -> 600 MW/min in total)
max_ramp = 0.05

# imaginary MOL with 1000 MW reserves, relevant for pay_as_bid vs. marginal pricing
# 100 MW for 30 Euro/MWh
# 100 MW for 40 Euro/MWh
# ...
# 100 MW for 120 Euro/MWh
if (pricing == "single")|(pricing == "NL"):
    if clearing == "marginal":
        price = 120
        #high MOL
        #price = 390
    if clearing == "pay_as_bid":
        #price = 75
        #high MOL
        price = 210

# this test scenario only consideres upwards flexibility. the imbalance price for upwards contribution is 0
if pricing == "dual":
    price = 0

#time values from min 0 to min 14
time = [i for i in range(15)]

#set imbalance with smart balancing contribution variable for simulation
imba_with_sb = imba
SB_real1 = 0
SB_real2 = 0
SB_real3 = 0

#for single pricing, the average power over the ISP indicates the risk of changing sign of imbalance price, not power
# therefore, average power needs to be tracked (in MW)
p_average = imba

print("Pricing scheme:", pricing, "; Clearing scheme:,",clearing,"; Imbalance :", imba, "MW; Imbalance price",price,"Euro/MWh")

#DataFrame for output
output = pd.DataFrame()
add = [imba,imba_with_sb,p_average,price,0,0,0,0,0,0]
output = output.append([add],ignore_index=True)

#SB contribution is compared to imbalance and warning is given in case of overcompensation.
for j in range(length):
    #test scenario imbalance unlimited -> leaves fuzzy boundaries -> input is set to 1000 MW and 100 EUR/MWh
    #imba = (j +1)*1000

    for i in range(len(time)):

        # update imbalance with market response
        imba_with_sb = round(imba - (SB_real1 + SB_real2 + SB_real3) * 1000)

        # calculate p_average
        p_average = round((p_average * i / (i + 1) + (imba_with_sb) / (i + 1)))

        # calculate new imbalance price, if applicable
        if (clearing == "pay_as_bid"):
            #MOL from 30 to 120
            #price = (price * i / (i + 1)) + ((30+(imba_with_sb-100)/20) / (i + 1))
            #high MOL from 30 to 390
            price = (price * i / (i + 1)) + ((30+(imba_with_sb-100)/5) / (i + 1))

        if ((clearing == "marginal")&((price < (20+(imba_with_sb)/10))|(i==0))):
            # MOL from 30 to 120
            price = (20+(imba_with_sb)/10)

        #if ((clearing == "marginal") & (price < (30 + (imba_with_sb - 100) / 2.5))):
            # high MOL from 30 to 390
            #price = (30+(imba_with_sb-100)/2.5)

# change sign of imbalance price in case of overcompensation
#todo: price = 0 disappears in next loop -> should stay 0 until end of ISP
        if pricing == "NL":
            if imba_with_sb < 0:
                price = 0
        if pricing == "single":
            if p_average < 0:
                price = 0

        print("Fuzzy Input Minute", time[i],': Imbalance with SB =',round(imba_with_sb), "MW, p_average =", round(p_average,1),"MW, Imbalance price =",round(price),"Euro/MWh")

        # calculate market participants fuzzy Smart Balancing contributiuon
        # Plant 70 has variable costs of 70 €/MWh - marge is 50 €/MWh with imbalance price of 120.. etc.
        marge = price - 70
        if marge > 0:
            Output_fuzz1 = round(fuzzlogi_marketdesign.fuzz(marge, imba_with_sb, time[i], p_average, pricing),3)
        else:
            Output_fuzz1 = 0

        if abs(Output_fuzz1 - SB_real1) < max_ramp:
            SB_real1 = Output_fuzz1
        elif (Output_fuzz1 - SB_real1) > 0:
            SB_real1 = SB_real1 + max_ramp
        elif (Output_fuzz1 - SB_real1) < 0:
            SB_real1 = SB_real1 - max_ramp

        print('[Plant 70 SB set-point in %]:', Output_fuzz1)
        print('[Plant 70 SB contribution in %]:', SB_real1)

        marge = price - 90
        if marge > 0:
            Output_fuzz2 = round(fuzzlogi_marketdesign.fuzz(marge, imba_with_sb, time[i], p_average, pricing),3)
        else:
            Output_fuzz2 = 0

        if abs(Output_fuzz2 - SB_real2) < max_ramp:
            SB_real2 = Output_fuzz2
        elif (Output_fuzz2 - SB_real2) > 0:
            SB_real2 = SB_real2 + max_ramp
        elif (Output_fuzz2 - SB_real2) < 0:
            SB_real2 = SB_real2 - max_ramp

        print('[Plant 90 SB set-point in %]:', Output_fuzz2)
        print('[Plant 90 SB contribution in %]:', SB_real2)


        marge = price - 110
        if marge > 0:
            Output_fuzz3 = round(fuzzlogi_marketdesign.fuzz(marge, imba_with_sb, time[i], p_average, pricing),3)
        else:
            Output_fuzz3 = 0

        #limitation to max_ramp
        if abs(Output_fuzz3 - SB_real3) < max_ramp:
            SB_real3 = Output_fuzz3
        elif (Output_fuzz3 - SB_real3) > 0:
            SB_real3 = SB_real3 + max_ramp
        elif (Output_fuzz3 - SB_real3) < 0:
            SB_real3 = SB_real3 - max_ramp

        print('[Plant 110 SB set-point in %]:', Output_fuzz3)
        print('[Plant 110 SB contribution in %]:', SB_real3)



        #save to output DataFrame: "imbalance","imbalance price","SB Plant 70", "SB Plant 90", "SB Plant 110"
        add = [imba,imba_with_sb, p_average,price, Output_fuzz1,SB_real1, Output_fuzz2,SB_real2, Output_fuzz3,SB_real3]
        output = output.append([add], ignore_index=True)

        # give notice if sb of three 1 GW plants led to overcompensation
        #if imba_with_sb < 0:
        #    print("SB led to overcompensation of imbalance! Imbalance is",imba_with_sb,"MW             <---------")

    #print("___________________________End of ISP:", j+1,"__________________________")


#give columns name, save as csv and print
output.columns = ["ACE","ACE with market response", "ACE_average","price in EUR/MWh", "Output_fuzz1","SB_real1", "Output_fuzz2","SB_real2", "Output_fuzz3","SB_real3"]

#save to csv
#output.to_csv("Sc1_single_marginal.csv")

#print(output.drop(columns={"imbalance","Output_fuzz3","SB_real3"}))

ax = output.drop(columns=["Output_fuzz1","SB_real1","Output_fuzz2","SB_real2","Output_fuzz3","SB_real3"]).plot(secondary_y=['price in EUR/MWh'])

ax.right_ax.set_ylim(0,126)
#ax.set_ylim(0, 1050)

ax.set_ylabel('MW')
ax.set_xlabel('minute')
ax.right_ax.set_ylabel('EUR/MWh')

plt.show()