# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITION FOR SMART BALANCING ASSETS ----------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# Objects of this class represent flexible assets of Balancing Groups.
# Their potentials for positive and negative balancing power are independent of other variables.
class SmartBalancingAsset:

    # CONSTRUCTOR METHOD
    # The constructor method is called to create an object of this class.
    # In the construction of an object of this class, all following variables are initialized...
    def __init__(self, name, sb_rate_pos, sb_rate_neg, sb_P_min, sb_P_max, sb_costs, bg_name):
        self.name = name

        # ...Initialization of Smart Balancing parameters
        self.sb_rate_pos = sb_rate_pos
        self.sb_rate_neg = sb_rate_neg
        self.sb_P_min = sb_P_min
        self.sb_P_max = sb_P_max
        self.sb_costs = sb_costs
        self.bg_name = bg_name

        # Parameters for the current positive and negative SB potentials.
        # In this class, these are not variable
        self.sb_pot_pos = sb_P_max
        self.sb_pot_neg = sb_P_min

        self.array_sb_pot_pos = []
        self.array_sb_pot_neg = []

        # ...Initialization of activated Smart Balancing power
        self.sb_P = 0.0

        # ...Definition of arrays containing simulation results
        self.array_sb_P = []

    # In this method, variables for the current positive and negative SB potentials should get updated.
    # Since the SB potentials are static for this class, the method is a dud.
    def sb_pot_calc(self):
        pass

    def sb_activate(self, sb_P_activate, t_step):
        if sb_P_activate > self.sb_P:
            sb_P_test = self.sb_P + self.sb_rate_pos * t_step
            if sb_P_test > sb_P_activate:
                sb_P_test = sb_P_activate
            else:
                pass
            if sb_P_test > self.sb_P_max:
                sb_P_test = self.sb_P_max
            else:
                pass
            self.sb_P = sb_P_test
        elif sb_P_activate < self.sb_P:
            sb_P_test = self.sb_P - self.sb_rate_neg * t_step
            if sb_P_test < sb_P_activate:
                sb_P_test = sb_P_activate
            else:
                pass
            if sb_P_test < self.sb_P_min:
                sb_P_test = self.sb_P_min
            else:
                pass
            self.sb_P = sb_P_test
        else:
            pass

    def write_results(self, type):
        self.array_sb_pot_pos.append(self.sb_pot_pos)
        self.array_sb_pot_neg.append(self.sb_pot_neg)
        self.array_sb_P.append(self.sb_P)
