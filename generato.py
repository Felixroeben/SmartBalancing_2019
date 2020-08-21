# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITIONS FOR GENERATORS ---------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# General class for generators. These objects do not have any other property than generating active power.
# The generated power can be set to a constant value during the construction of the object...
# ...or be externally defined by a time series.
class Generator:

    # CONSTRUCTOR METHOD
    # The constructor method is called to create an object of this class.
    # In the construction of an object of this class, all following variables are initialized...
    def __init__(self, name, read, gen_P):
        self.name = name                    # String for the name of the generator
        self.read = read                    # Boolean variable defining, if time series are read from .csv files
        self.gen_P = gen_P                  # Current active power output of the generator in MW

        # Definition of arrays containing simulation results
        self.array_gen_P = []

    def readarray(self, k_now):
        if self.read:
            self.gen_P = self.array_gen_P[k_now]

    def write_results(self, type):
        if not self.read:
            self.array_gen_P.append(self.gen_P)



# Class for flexible generators, that can adjust their active power output to provide Smart Balancing.
# Objects of class combine the properties of classes 'Generator' and 'SmartBalancingAsset'.
# Firstly, 'GeneratorFlex'-objects generate power, which can be defined by an external time series.
# Secondly, 'GeneratorFlex'-objects do have the potentials to provide Smart Balancing power.
# Therefore, an object of class 'GeneratorFlex' is to be subordinated to both arrays of the object 'BalancingGroup':
# 1. self.array_generators
# 2. self.array_sb_assets
# Their potentials for positive and negative balancing power depend on the currently generated power.
class GeneratorFlex(Generator):

    # CONSTRUCTOR METHOD
    # The constructor method is called to create an object of this class.
    # In the construction of an object of this class, all following variables are initialized...
    def __init__(self, name, read, gen_P, sb_rate_pos, sb_rate_neg, sb_P_max, sb_P_min, sb_costs, bg_name):
        self.sb_rate_pos = sb_rate_pos      # Positive ramp rate for Smart Balancing in MW/s
        self.sb_rate_neg = sb_rate_neg      # Negative ramp rate for Smart Balancing in MW/s
        self.sb_P_max = sb_P_max            # Maximum value for the active power output in MW
        self.sb_P_min = sb_P_min            # Minimum value for the active power output in MW
        self.sb_costs = sb_costs            # Marginal costs in EUR, that need to met to make Smart Balancing economical
        self.bg_name = bg_name              # Name of the Balancing Group, the flexible generator is assigned to

        # Other parameters and variables are inherited from the super class 'Generator'.
        # Therefore, the constructor method of the super class is called to initialize these parameters and variables.
        Generator.__init__(self,
                           name=name,
                           read=read,
                           gen_P=gen_P)

        # Variables for the current positive and negative SB potentials.
        self.sb_pot_pos = 0.0
        self.sb_pot_neg = 0.0

        self.array_sb_pot_pos = []
        self.array_sb_pot_neg = []

        # Variable for the current active power output, that is activated on top of gen_P to provide Smart Balancing
        self.sb_P = 0.0

        self.array_sb_P = []

    # In this method, variables for the current positive and negative SB potentials get updated...
    # ...using the current active power generation (self.gen_P)
    def sb_pot_calc(self):
        # Calculation for flexible generators of Balancing Groups "Solar", "Wind_Onshore", and "Wind_Offshore"
        # Positive SB potential is always set to zero for these generators
        if self.bg_name == "Solar" or self.bg_name == "Wind_Onshore" or self.bg_name == "Wind_Offshore":
            self.sb_pot_pos = 0.0
            if self.gen_P > self.sb_P_min:
                self.sb_pot_neg = self.sb_P_min - self.gen_P
            else:
                self.sb_pot_neg = 0.0

        # Default calculation for flexible generators
        elif self.gen_P > self.sb_P_min and self.gen_P < self.sb_P_max:
            if self.sb_P_max > self.gen_P:
                self.sb_pot_pos = self.sb_P_max - self.gen_P
            else:
                self.sb_pot_pos = 0.0

            if self.sb_P_min < self.gen_P:
                self.sb_pot_neg = self.sb_P_min - self.gen_P
            else:
                self.sb_pot_neg = 0.0
        else:
            self.sb_pot_pos = 0.0
            self.sb_pot_neg = 0.0

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
        if type == 'gen':
            if not self.read:
                self.array_gen_P.append(self.gen_P)
        elif type == 'sb':
            self.array_sb_pot_pos.append(self.sb_pot_pos)
            self.array_sb_pot_neg.append(self.sb_pot_neg)
            self.array_sb_P.append(self.sb_P)
        else:
            print('Invalid save type for object', self.name, '(class GeneratorFlex)')
