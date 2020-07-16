# General class for loads
class Load:

    # CONSTRUCTOR METHOD
    def __init__(self, name, read, load_P):
        self.name = name                    # String for the name of the load
        self.read = read                    # Boolean variable defining, if time series are read from .csv files
        self.load_P = load_P                # Current active power consumption of the load in MW

        # Definition of arrays containing simulation results
        self.array_load_P = []

    def readarray(self, k_now):
        if self.read:
            self.load_P = self.array_load_P[k_now]

    def write_results(self, type):
        if not self.read:
            self.array_load_P.append(self.load_P)



# Class for flexible loads, that can adjust their active power consumption to provide Smart Balancing
class LoadFlex(Load):

    # CONSTRUCTOR METHOD
    def __init__(self, name, read, load_P, sb_rate_pos, sb_rate_neg, sb_P_max, sb_P_min, sb_costs, bg_name):
        self.sb_rate_pos = sb_rate_pos      # Positive ramp rate for Smart Balancing in MW/s
        self.sb_rate_neg = sb_rate_neg      # Negative ramp rate for Smart Balancing in MW/s
        self.sb_P_max = sb_P_max            # Maximum value for the active power consumption in MW
        self.sb_P_min = sb_P_min            # Minimum value for the active power consumption in MW
        self.sb_costs = sb_costs            # Marginal costs in EUR, that need to met to make Smart Balancing economical
        self.bg_name = bg_name              # Name of the Balancing Group, the flexible load is assigned to

        # Other parameters are inherited from the super class 'Load'
        Load.__init__(self,
                      name=name,
                      read=read,
                      load_P=load_P)

        # Variables for the current positive and negative SB potentials.
        self.sb_pot_pos = 0.0
        self.sb_pot_neg = 0.0

        self.array_sb_pot_pos = []
        self.array_sb_pot_neg = []

        # Variable for the current active power consumption, that is activated on top of load_P to provide Smart Balancing
        self.sb_P = 0.0

        self.array_sb_P = []

    # In this method, variables for the current positive and negative SB potentials get updated...
    # ...using the current active power consumption (self.load_P)
    def sb_pot_calc(self):
        # Calculation of potentials for flexible load 'Arcelor_Mittal_Kessel'
        if self.name == 'Arcelor_Mittal_Kessel':
            if self.load_P >= 60:
                self.sb_pot_neg = -self.sb_P_max
                if self.load_P > 70:
                    self.sb_pot_pos = -self.sb_P_min
                else:
                    self.sb_pot_pos = self.load_P - 60
            else:
                self.sb_pot_neg = 0.0
                self.sb_pot_pos = 0.0
        # Default calculation for flexible loads
        elif self.load_P >= self.sb_P_min and self.load_P <= self.sb_P_max:
            if self.sb_P_max >= self.load_P:
                self.sb_pot_neg = -(self.sb_P_max - self.load_P)
            else:
                self.sb_pot_neg = 0.0
            if self.sb_P_min <= self.load_P:
                self.sb_pot_pos = -(self.sb_P_min - self.load_P)
            else:
                self.sb_pot_pos = 0.0
        else:
            self.sb_pot_neg = 0.0
            self.sb_pot_pos = 0.0

    def sb_activate(self, sb_P_activate, t_step):
        if sb_P_activate > self.sb_P:
            sb_P_test = self.sb_P + self.sb_rate_pos * t_step
            if sb_P_test > sb_P_activate:
                sb_P_test = sb_P_activate
            else:
                pass
            if sb_P_test > self.sb_pot_pos:
                 sb_P_test = self.sb_pot_pos
            else:
                pass
            self.sb_P = sb_P_test
        elif sb_P_activate < self.sb_P:
            sb_P_test = self.sb_P - self.sb_rate_neg * t_step
            if sb_P_test < sb_P_activate:
                sb_P_test = sb_P_activate
            else:
                pass
            if sb_P_test < self.sb_pot_neg:
                sb_P_test = self.sb_pot_neg
            else:
                pass
            self.sb_P = sb_P_test
        else:
            pass

    def write_results(self, type):
        if type == 'load':
            if not self.read:
                self.array_load_P.append(self.load_P)
        elif type == 'sb':
            self.array_sb_pot_pos.append(self.sb_pot_pos)
            self.array_sb_pot_neg.append(self.sb_pot_neg)
            self.array_sb_P.append(self.sb_P)
        else:
            print('Invalid save type for object', self.name, '(class LoadFlex)')
