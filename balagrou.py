# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITION FOR BALANCING GROUPS ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

import fuzzlogi_marketdesign
import math

# Objects of class 'BalancingGroups' represent the Balancing Groups of a Control Area.
# 'BalancingGroups' are to be subordinated to objects of class 'ControlArea' only.
# In turn, any object of class 'ControlArea' needs subordinated 'BalancingGroups' to function properly.
class BalancingGroup:

    # CONSTRUCTOR METHOD
    # The constructor method is called to create an object of this class.
    # In the construction of an object of this class, all following variables are initialized...
    def __init__(self, name, read, smart):

        # ...Initialization of name
        self.name = name
        self.read = read
        self.smart = smart

        # ...Definition of load flow parameters
        self.gen_P = 0.0
        self.load_P = 0.0
        self.gen_P_schedule = self.gen_P
        self.load_P_schedule = self.load_P
        self.imba_P_ph = 0.0
        self.imba_P_sc = 0.0
        self.sb_P = 0.0
        self.sb_P_activate = 0.0

        # ...Definition of produced and consumed energies
        self.gen_E = 0.0
        self.load_E = 0.0
        self.gen_E_schedule = self.gen_E
        self.load_E_schedule = self.load_E
        self.imba_E = 0.0
        self.sb_E_pos = 0.0
        self.sb_E_neg = 0.0
        self.sb_E_pos_period = 0.0
        self.sb_E_neg_period = 0.0

        self.gen_E_period = 0.0
        self.load_E_period = 0.0
        self.gen_E_schedule_period = self.gen_E
        self.load_E_schedule_period = self.load_E
        self.imba_E_period = 0.0

        # ...Definition of AEP cost variables
        self.AEP_costs = 0.0
        self.AEP_costs_period = 0.0
        self.sb_costs_pos = 0.0
        self.sb_costs_neg = 0.0
        self.sb_costs_pos_period = 0.0
        self.sb_costs_neg_period = 0.0

        # ...Variables for energy costs and imcome
        self.gen_income = 0.0
        self.load_costs = 0.0
        self.gen_income_period = 0.0
        self.load_costs_period = 0.0

        # ...Definition of arrays containing simulation results
        self.array_gen_P = []
        self.array_load_P = []
        self.array_gen_P_schedule = []
        self.array_load_P_schedule = []
        self.array_gen_E = []
        self.array_load_E = []
        self.array_gen_E_schedule = []
        self.array_load_E_schedule = []
        self.array_gen_E_period = []
        self.array_load_E_period = []
        self.array_gen_E_schedule_period = []
        self.array_load_E_schedule_period = []
        self.array_imba_P_ph = []
        self.array_imba_P_sc = []
        self.array_imba_E = []
        self.array_imba_E_period = []
        self.array_sb_P = []
        self.array_sb_P_activate = []
        self.array_sb_E_pos = []
        self.array_sb_E_neg = []
        self.array_sb_E_pos_period = []
        self.array_sb_E_neg_period = []
        self.array_sb_costs_pos = []
        self.array_sb_costs_neg = []
        self.array_sb_costs_pos_period = []
        self.array_sb_costs_neg_period = []
        self.array_AEP_costs = []
        self.array_AEP_costs_period = []
        self.array_gen_income = []
        self.array_load_costs = []
        self.array_gen_income_period = []
        self.array_load_costs_period = []

        # ...Definition of array containing all subordinated Power Plants and Loads
        self.array_generators = []
        self.array_loads = []

        # ...Definition of array containing Smart Balancing assets
        self.array_sb_assets = []

        # Arrays for positive and negative Smart Balancing assets
        self.array_sb_molpos = []
        self.array_sb_molneg = []

    def schedule_init(self):
        if self.read:
            self.gen_P_schedule = self.array_gen_P_schedule[1]
            self.load_P_schedule = self.array_load_P_schedule[1]
        else:
            self.gen_P_schedule = self.gen_P
            self.load_P_schedule = self.load_P

    def imba_calc(self):
        self.imba_P_ph = self.gen_P - self.load_P + self.sb_P
        self.imba_P_sc = self.gen_P - self.gen_P_schedule - self.load_P + self.load_P_schedule + self.sb_P

    def gen_calc(self):
        self.gen_P = 0.0
        for i in self.array_generators:
            self.gen_P += i.gen_P

    def load_calc(self):
        self.load_P = 0.0
        for i in self.array_loads:
            self.load_P += i.load_P

    # Method calculating the generated and consumed energy for the balancing group.
    # Scheduled energies are also calculated.
    # All energy variables have a version, that gets reset after each ISP
    def afrr_calc(self, t_now, t_step, t_isp, AEP):
        self.gen_E += self.gen_P * t_step / 3600
        self.load_E += self.load_P * t_step / 3600

        self.gen_E_schedule += self.gen_P_schedule * t_step / 3600
        self.load_E_schedule += self.load_P_schedule * t_step / 3600

        self.imba_E += self.imba_P_sc * t_step / 3600

        if self.sb_P > 0:
            self.sb_E_pos += self.sb_P * t_step / 3600
        elif self.sb_P < 0:
            self.sb_E_neg += self.sb_P * t_step / 3600
        else:
            pass

        if (t_now % t_isp) == 0:
            self.gen_E_period = 0.0
            self.load_E_period = 0.0
            self.gen_E_schedule_period = 0.0
            self.load_E_schedule_period = 0.0
            self.imba_E_period = 0.0
            self.sb_E_pos_period = 0.0
            self.sb_E_neg_period = 0.0

        self.gen_E_period += self.gen_P * t_step / 3600
        self.load_E_period += self.load_P * t_step / 3600

        self.gen_E_schedule_period += self.gen_P_schedule * t_step / 3600
        self.load_E_schedule_period += self.load_P_schedule * t_step / 3600

        self.imba_E_period += self.imba_P_sc * t_step / 3600

        if self.sb_P > 0:
            self.sb_E_pos_period += self.sb_P * t_step / 3600
        elif self.sb_P < 0:
            self.sb_E_neg_period += self.sb_P * t_step / 3600
        else:
            pass

        # in the last time step of each ISP, the costs for imbalances are calculated
        if ((t_now + t_step) % t_isp) == 0:
            self.aep_costs_calc(AEP)

    # Method that calculates the costs for imbalances at the end of an ISP...
    # ...using to the "Ausgleichsenergiepreis" (AEP)
    # This method should be called in the last time step of an ISP
    def aep_costs_calc(self, AEP):
        self.AEP_costs_period = - self.imba_E_period * AEP
        self.AEP_costs += self.AEP_costs_period

        self.sb_costs_pos_period = - self.sb_E_pos_period * AEP
        self.sb_costs_pos += self.sb_costs_pos_period

        self.sb_costs_neg_period = - self.sb_E_neg_period * AEP
        self.sb_costs_neg += self.sb_costs_neg_period

    def sb_init(self):
        array_name = []
        array_price = []
        array_power = []
        for i in self.array_sb_assets:
            if not array_price and i.sb_P_max > 0:
                array_name.append(i.name)
                array_price.append(i.sb_costs)
                array_power.append(i.sb_P_max)
            elif array_price and i.sb_P_max > 0:
                j = 0
                while j < len(array_price) and array_price[j] < i.sb_costs:
                    j += 1
                array_name.insert(j, i.name)
                array_price.insert(j, i.sb_costs)
                array_power.insert(j, i.sb_P_max)

        self.array_sb_molpos = {'SB Asset ID': array_name,
                                'Price': array_price,
                                'Power': array_power}

        array_name = []
        array_price = []
        array_power = []
        for i in self.array_sb_assets:
            if not array_price and i.sb_P_min < 0:
                array_name.append(i.name)
                array_price.append(i.sb_costs)
                array_power.append(i.sb_P_min)
            elif array_price and i.sb_P_min < 0:
                j = 0
                while j < len(array_price) and array_price[j] < i.sb_costs:
                    j += 1
                array_name.insert(j, i.name)
                array_price.insert(j, i.sb_costs)
                array_power.insert(j, i.sb_P_min)

        self.array_sb_molneg = {'SB Asset ID': array_name,
                                'Price': array_price,
                                'Power': array_power}

    # This method calculates the Smart Balancing power of the Smart Balancing Assets of the Balancing Group
    def sb_calc(self, FRCE_sb, old_FRCE_sb, d_Imba, old_d_Imba, AEP, t_step, t_now, da_price, windon_mmw, windoff_mmw, pv_mmw, aFRR_E_pos_period, aFRR_E_neg_period, fuzzy, imbalance_clearing):

        ## 13.09.2020 restructure sb_calc to better implement fuzzy logic (FR)
        # delete multiple condition "smart and fuzzy" - ask for fuzzy condition if smart
        #  imbalance clearing ("0" for single and "1" for combined/NL)
        # 1. sb_pot_calc() = individual SB potential in MW - see generato.py / loadload.py
        # 2. if smart -> calculate sb_P, ask if fuzzy and call sb_activation() - see generato.py / loadload.py
        # 3.    if fuzzy -> manipulate sb_P with fuzzilogi_marketdesign.py
        # 4.    activate sb_P according to sb_activate (ramp max)- - see generato.py / loadload.py

        # The positive and negative SB potentials of all assets get updated.
        for i in self.array_sb_assets:
            i.sb_pot_calc()

        # SB remains if ACE between 200 MW and -200 MW
        #if FRCE_sb > -200 and FRCE_sb < 200:
        #    pass
        # Activation of SB Assets
        # using Fuzzy Logic (if fuzzy = true)
        # in case fuzzy is true + NL clearing: check if dual pricing applies
        if self.smart and not (fuzzy and (imbalance_clearing == 1) and ((aFRR_E_neg_period < -50) and (aFRR_E_pos_period > 50))):
            self.sb_P = 0.0

            SB_Asset_ID = []
            SB_per_asset = []

            # Summation of the total positive and negative Smart Balancing potential of the Balancing Group
            # Variables can get used to prevent overshoots in case of FRCE_sb close to zero
            P_max_sum = 0.0
            P_min_sum = 0.0
            for i in self.array_sb_assets:
                P_max_sum += i.sb_pot_pos
                P_min_sum += i.sb_pot_neg

            if fuzzy:
                # Calc time within 15 Min ISP in Minute (between 0 and 14) for fuzzy
                time_in_ISP = (t_now / 60) % 15
                # calc p_average in MW in ISP for fuzzy (from aFRR of ISP in MWh)
                p_average = (aFRR_E_pos_period + aFRR_E_neg_period)/((time_in_ISP + 1)/60)


            # Decision making for Balancing Group "Solar"
            if self.name == 'Solar':
                sb_sum = 0.0
                for i in self.array_sb_assets:
                    sb_activation = 0.0
                    sb_marge = 0.0

                    # Definition of additional margin in EUR/MWh
                    margin = 60.0

                    # Calculation of the current "Marktprämie" for the asset, which is never smaller than zero
                    #sb_costs = "anzulegender Wert" from SB_Asset.csv (value depending on year of construction)
                    mp = i.sb_costs - pv_mmw
                    if mp < 0:
                        mp = 0.0
                    else:
                        pass

                    if AEP < -(mp + margin) and i.sb_pot_neg < 0:
                        #def fuzz(Marge, Imba, Time, p_average, pricing)
                        if fuzzy:
                            # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                            sb_marge = -AEP - (mp + margin)
                            sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba, time_in_ISP,
                                                                    p_average, imbalance_clearing, self.sb_P,
                                                                    P_min_sum)
                            sb_activation = i.sb_pot_neg * sb_percent
                        else:
                            sb_activation = i.sb_pot_neg

                        # Optional limitation of the targeted Smart Balancing power using the total FRCE
                        if sb_sum + sb_activation < FRCE_sb:
                            sb_activation = FRCE_sb - sb_sum

                    else:
                        sb_activation = 0.0

                    SB_Asset_ID.append(i.name)
                    SB_per_asset.append(sb_activation)
                    sb_sum += sb_activation

            # Decision making for Balancing Group "Wind_Onshore"
            elif self.name == 'Wind_Onshore':
                sb_sum = 0.0
                for i in self.array_sb_assets:
                    sb_activation = 0.0

                    # Definition of additional margin in EUR/MWh
                    margin = 40.0

                    # Calculation of the current "Marktprämie" for the asset, which is never smaller than zero
                    mp = i.sb_costs - windon_mmw
                    if mp < 0:
                        mp = 0.0
                    else:
                        pass

                    if AEP < -(mp + margin) and i.sb_pot_neg < 0:
                        if fuzzy:
                            # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                            sb_marge = -AEP - (mp + margin)
                            sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba, time_in_ISP,
                                                                    p_average,imbalance_clearing, self.sb_P,
                                                                    P_min_sum)
                            sb_activation = i.sb_pot_neg * sb_percent
                        else:
                            sb_activation = i.sb_pot_neg

                        # Optional limitation of the targeted Smart Balancing power using the total FRCE
                        if sb_sum + sb_activation < FRCE_sb:
                            sb_activation = FRCE_sb - sb_sum


                    else:
                        sb_activation = 0.0

                    SB_Asset_ID.append(i.name)
                    SB_per_asset.append(sb_activation)
                    sb_sum += sb_activation

            # Decision making for Balancing Group "Wind_Offshore"
            elif self.name == 'Wind_Offshore':
                sb_sum = 0.0
                for i in self.array_sb_assets:
                    sb_activation = 0.0

                    # Definition of additional margin in EUR/MWh
                    margin = 40.0

                    # Calculation of the current "Marktprämie" for the asset, which is never smaller than zero
                    mp = i.sb_costs - windoff_mmw
                    if mp < 0:
                        mp = 0.0
                    else:
                        pass

                    if AEP < -(mp + margin) and i.sb_pot_neg < 0:

                        if fuzzy:
                            #marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                            sb_marge = -AEP - (mp + margin)
                            sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb,old_d_Imba, d_Imba, time_in_ISP,
                                                                    p_average, imbalance_clearing, self.sb_P,
                                                                    P_min_sum)
                            sb_activation = i.sb_pot_neg * sb_percent
                        else:
                            sb_activation = i.sb_pot_neg

                        # Optional limitation of the targeted Smart Balancing power using the total FRCE
                        if sb_sum + sb_activation < FRCE_sb:
                            sb_activation = FRCE_sb - sb_sum

                    else:
                        sb_activation = 0.0

                    SB_Asset_ID.append(i.name)
                    SB_per_asset.append(sb_activation)
                    sb_sum += sb_activation

            # Decision making for Balancing Group "Aluminium" - decrease load in case of high AEP
            elif self.name == 'Aluminium':
                if (AEP - da_price) > 100:
                    for i in self.array_sb_assets:
                        if i.sb_pot_pos > 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = AEP - da_price - 100
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba,time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_max_sum)
                                sb_activation = i.sb_pot_pos * sb_percent
                            else:
                                sb_activation = i.sb_pot_pos

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation > FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                else:
                    for i in self.array_sb_assets:
                        SB_Asset_ID.append(i.name)
                        SB_per_asset.append(0.0)

            # Decision making for Balancing Group "Steel" - decrease load in case of high AEP
            elif self.name == 'Steel':
                if (AEP - da_price) > 250:
                    for i in self.array_sb_assets:
                        if i.sb_pot_pos > 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = AEP - da_price - 250
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba,time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_max_sum)
                                sb_activation = i.sb_pot_pos * sb_percent
                            else:
                                sb_activation = i.sb_pot_pos

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation > FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                else:
                    for i in self.array_sb_assets:
                        SB_Asset_ID.append(i.name)
                        SB_per_asset.append(0.0)

            # Decision making for Balancing Group "Cement" - increase (neg AEP) or decrease (high AEP) of load
            elif self.name == 'Cement':
                if (AEP - da_price) > 250:
                    for i in self.array_sb_assets:
                        if i.sb_pot_pos > 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = AEP - da_price - 250
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb,old_d_Imba, d_Imba, time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_max_sum)
                                sb_activation = i.sb_pot_pos * sb_percent
                            else:
                                sb_activation = i.sb_pot_pos

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation > FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                elif AEP < 10:
                    for i in self.array_sb_assets:
                        if i.sb_pot_neg < 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = 10 - AEP
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb,old_d_Imba, d_Imba, time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_min_sum)
                                sb_activation = i.sb_pot_neg * sb_percent
                            else:
                                sb_activation = i.sb_pot_neg

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation < FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                else:
                    for i in self.array_sb_assets:
                        SB_Asset_ID.append(i.name)
                        SB_per_asset.append(0.0)

            # Decision making for Balancing Group "Paper"
            elif self.name == 'Paper':
                if (AEP - da_price) > 250:
                    for i in self.array_sb_assets:
                        if i.sb_pot_pos > 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = AEP - da_price - 250
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba,time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_max_sum)
                                sb_activation = i.sb_pot_pos * sb_percent
                            else:
                                sb_activation = i.sb_pot_pos

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation > FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                elif AEP < 10:
                    for i in self.array_sb_assets:
                        if i.sb_pot_neg < 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = 10 - AEP
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb,old_d_Imba, d_Imba, time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_min_sum)
                                sb_activation = i.sb_pot_neg * sb_percent
                            else:
                                sb_activation = i.sb_pot_neg

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation < FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                else:
                    for i in self.array_sb_assets:
                        SB_Asset_ID.append(i.name)
                        SB_per_asset.append(0.0)

            # Decision making for Balancing Group "Chlorine"
            elif self.name == 'Chlorine':
                if (AEP - da_price) > 250:
                    for i in self.array_sb_assets:
                        if i.sb_pot_pos > 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = AEP - da_price - 250
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba,time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_max_sum)
                                sb_activation = i.sb_pot_pos * sb_percent
                            else:
                                sb_activation = i.sb_pot_pos

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation > FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                elif AEP < 10:
                    for i in self.array_sb_assets:
                        if i.sb_pot_neg < 0:
                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = 10 - AEP
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb,old_d_Imba, d_Imba, time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_min_sum)
                                sb_activation = i.sb_pot_neg * sb_percent
                            else:
                                sb_activation = i.sb_pot_neg

                            # Optional limitation of the targeted Smart Balancing power using the total FRCE
                            #if sb_activation < FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)
                else:
                    for i in self.array_sb_assets:
                        SB_Asset_ID.append(i.name)
                        SB_per_asset.append(0.0)

            # Other Balancing Groups get triggered by the arithmetic sign of the signal FRCE_sb and AEP
            else:
                if FRCE_sb < 0:
                    for i in self.array_sb_assets:
                        if (i.sb_pot_neg < 0 and (i.sb_costs - 36) > AEP):

                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = i.sb_costs - 35 - AEP
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb,old_d_Imba, d_Imba, time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_min_sum)
                                sb_activation = i.sb_pot_neg * sb_percent
                            else:
                                sb_activation = i.sb_pot_neg

                            #limit SB of each asset to target FRCE
                            #if sb_activation < FRCE_sb:
                            #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)

                # In case of positive FRCE_sb, positive SB assets are triggered
                elif FRCE_sb > 0:
                    for i in self.array_sb_assets:
                        if i.sb_pot_pos > 0 and (i.sb_costs+5)<AEP:

                            if fuzzy:
                                # marge for SB is (negativ) AEP minus (plus) current "Marktprämie" and additional margin
                                sb_marge = AEP - i.sb_costs - 5
                                sb_percent = fuzzlogi_marketdesign.fuzz(sb_marge, FRCE_sb, old_FRCE_sb, old_d_Imba, d_Imba,time_in_ISP,
                                                                        p_average, imbalance_clearing, self.sb_P,
                                                                        P_max_sum)
                                sb_activation = i.sb_pot_pos * sb_percent
                            else:
                                sb_activation = i.sb_pot_pos

                                # limit SB of each asset to target FRCE
                                #if sb_activation > FRCE_sb:
                                #    sb_activation = FRCE_sb

                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(sb_activation)
                        else:
                            SB_Asset_ID.append(i.name)
                            SB_per_asset.append(0.0)

                # In case of FRCE_sb equal to zero, all SB assets are set to zero
                elif FRCE_sb == 0:
                    for i in self.array_sb_assets:
                        SB_Asset_ID.append(i.name)
                        SB_per_asset.append(0.0)
                else:
                    pass

            #todo: this should be last step and not within smart = true condition. otherwise NL combined pricing sets
            #sb_P back too fast if dual pricing applies and sb_B is set zero

            # Activation of SB Assets within physical boundaries of ramp
            # > see sb_activate() in generator.py / loadload.py
            array_sb_activate = {"SB_Asset_ID": SB_Asset_ID, "SB_per_asset": SB_per_asset}

            j = 0
            while j <= len(array_sb_activate['SB_Asset_ID']) - 1:
                for i in self.array_sb_assets:
                    if array_sb_activate.get('SB_Asset_ID')[j] == i.name:
                        i.sb_activate(array_sb_activate.get('SB_per_asset')[j], t_step)
                j += 1


            #todo: SB reduction factor here?
            for i in self.array_sb_assets:
                self.sb_P += i.sb_P
        # smart not true:
        else:
            self.sb_P = 0.0

    # Method calculating the costs for consumed energy and the income of produced energy of the grid element.
    # The method multiplies the consumed and produced amounts of energy per t_step with the current day-ahead price
    def energy_costs_calc(self, k_now, t_now, t_step, t_isp, da_price, windon_mmw, windoff_mmw, pv_mmw):
        # Calculation of income for Balancing Groups "Solar", "Wind_Onshore", and "Wind_Offshore"
        # Using the "Marktprämie" (mp) for each generator
        if self.name == "Solar":
            for i in self.array_sb_assets:
                mp = i.sb_costs - pv_mmw
                if mp < 0:
                    mp = 0.0
                else:
                    pass
                self.gen_income += (i.gen_P + i.sb_P) * mp * t_step / 3600

        elif self.name == "Wind_Onshore":
            for i in self.array_sb_assets:
                mp = i.sb_costs - windon_mmw
                if mp < 0:
                    mp = 0.0
                else:
                    pass
                self.gen_income += (i.gen_P + i.sb_P) * mp * t_step / 3600

        elif self.name == "Wind_Offshore":
            for i in self.array_sb_assets:
                mp = i.sb_costs - windoff_mmw
                if mp < 0:
                    mp = 0.0
                else:
                    pass
                self.gen_income += (i.gen_P + i.sb_P) * mp * t_step / 3600

        # Calculation of costs and income for other Balancing Groups
        else:
            self.gen_income += self.gen_P_schedule * da_price * t_step / 3600
            self.load_costs += self.load_P_schedule * da_price * t_step / 3600




        # Calculation of costs and income per ISP
        # Variables get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.gen_income_period = 0.0
            self.load_costs_period = 0.0

        # Calculation of income for Balancing Groups "Solar", "Wind_Onshore", and "Wind_Offshore"
        # Using the "Monatsmarktwert" and "anzulegender Wert" for each generator (GeneratorFlex)
        if self.name == "Solar":
            for i in self.array_sb_assets:
                mp = i.sb_costs - pv_mmw
                if mp < 0:
                    mp = 0.0
                else:
                    pass
                self.gen_income_period += (i.gen_P + i.sb_P) * mp * t_step / 3600

        elif self.name == "Wind_Onshore":
            for i in self.array_sb_assets:
                mp = i.sb_costs - windon_mmw
                if mp < 0:
                    mp = 0.0
                else:
                    pass
                self.gen_income_period += (i.gen_P + i.sb_P) * mp * t_step / 3600

        elif self.name == "Wind_Offshore":
            for i in self.array_sb_assets:
                mp = i.sb_costs - windoff_mmw
                if mp < 0:
                    mp = 0.0
                else:
                    pass
                self.gen_income_period += (i.gen_P + i.sb_P) * mp * t_step / 3600

        # Calculation of costs and income for other Balancing Groups for each ISP
        else:
            self.gen_income_period += self.gen_P_schedule * da_price * t_step / 3600
            self.load_costs_period += self.load_P_schedule * da_price * t_step / 3600

    def readarray(self, k_now):
        if self.read:
            self.gen_P_schedule = self.array_gen_P_schedule[k_now]
            self.load_P_schedule = self.array_load_P_schedule[k_now]
        for i in self.array_generators:
            i.readarray(k_now=k_now)
        for i in self.array_loads:
            i.readarray(k_now=k_now)

    def write_results(self):
        for i in self.array_generators:
            i.write_results(type='gen')
        for i in self.array_loads:
            i.write_results(type='load')
        for i in self.array_sb_assets:
            i.write_results(type='sb')
        self.array_gen_P.append(self.gen_P)
        self.array_load_P.append(self.load_P)
        if not self.read:
            self.array_gen_P_schedule.append(self.gen_P_schedule)
            self.array_load_P_schedule.append(self.load_P_schedule)
        self.array_gen_E.append(self.gen_E)
        self.array_load_E.append(self.load_E)
        self.array_gen_E_schedule.append(self.gen_E_schedule)
        self.array_load_E_schedule.append(self.load_E_schedule)
        self.array_gen_E_period.append(self.gen_E_period)
        self.array_load_E_period.append(self.load_E_period)
        self.array_gen_E_schedule_period.append(self.gen_E_schedule_period)
        self.array_load_E_schedule_period.append(self.load_E_schedule_period)
        self.array_imba_P_ph.append(self.imba_P_ph)
        self.array_imba_P_sc.append(self.imba_P_sc)
        self.array_imba_E.append(self.imba_E)
        self.array_imba_E_period.append(self.imba_E_period)
        self.array_sb_P.append(self.sb_P)
        self.array_sb_P_activate.append(self.sb_P_activate)
        self.array_sb_E_pos.append(self.sb_E_pos)
        self.array_sb_E_neg.append(self.sb_E_neg)
        self.array_sb_E_pos_period.append(self.sb_E_pos_period)
        self.array_sb_E_neg_period.append(self.sb_E_neg_period)
        self.array_AEP_costs.append(self.AEP_costs)
        self.array_AEP_costs_period.append(self.AEP_costs_period)
        self.array_sb_costs_pos.append(self.sb_costs_pos)
        self.array_sb_costs_neg.append(self.sb_costs_neg)
        self.array_sb_costs_pos_period.append(self.sb_costs_pos_period)
        self.array_sb_costs_neg_period.append(self.sb_costs_neg_period)
        self.array_gen_income.append(self.gen_income)
        self.array_load_costs.append(self.load_costs)
        self.array_gen_income_period.append(self.gen_income_period)
        self.array_load_costs_period.append(self.load_costs_period)
