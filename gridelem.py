# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITIONS FOR GRID ELEMENTS ------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

import math



# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITION FOR GRID ELEMENTS WITH SUBORDINATED GRID ELEMENTS -----------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# The generic class 'GridElement' can be used for all kinds of grid structures
# like Coordination Centers, Control Blocks, or Control Areas.
# An object of the class 'GridElement' contains subordinated grid elements to which it passes its methods.
# No true calculations are executed in the class 'GridElement'.

class GridElement:

    # CONSTRUCTOR METHOD
    def __init__(self,
                 name):           # name of the grid element            (string)

        # ...Initialization of name
        self.name = name

        # ...Load flow parameters
        self.gen_P = 0.0
        self.load_P = 0.0
        self.gen_P_schedule = self.gen_P
        self.load_P_schedule = self.load_P
        self.imba_P_ph = 0.0
        self.imba_P_sc = 0.0

        self.array_gen_P = []
        self.array_load_P = []
        self.array_gen_P_schedule = []
        self.array_load_P_schedule = []
        self.array_imba_P_ph = []
        self.array_imba_P_sc = []

        # ...FCR constants
        self.FCR_lambda = 0.0

        # ...FCR variables
        self.FCR_P = 0.0

        self.array_FCR_P = []

        # ...aFRR variables
        self.aFRR_P = 0.0
        self.aFRR_P_pos = 0.0
        self.aFRR_P_neg = 0.0

        self.array_aFRR_P = []
        self.array_aFRR_P_pos = []
        self.array_aFRR_P_neg = []

        # ...mFRR variables
        self.mFRR_P = 0.0
        self.mFRR_P_pos = 0.0
        self.mFRR_P_neg = 0.0

        self.array_mFRR_P = []
        self.array_mFRR_P_pos = []
        self.array_mFRR_P_neg = []

        # ...Smart Balancing variables
        self.sb_P = 0.0

        self.array_sb_P = []

        # ...Variables for energy costs and imcome
        self.gen_income = 0.0
        self.load_costs = 0.0
        self.gen_income_period = 0.0
        self.load_costs_period = 0.0

        self.array_gen_income = []
        self.array_load_costs = []
        self.array_gen_income_period = []
        self.array_load_costs_period = []

        # ...Array containing all subordinated grid elements
        self.array_subordinates = []

    # Method calculating the generator power of the grid element.
    # The method sums up the generator power of all subordinated grid elements
    def gen_calc(self):
        self.gen_P = 0.0
        for i in self.array_subordinates:
            i.gen_calc()
            self.gen_P += i.gen_P

    # Method calculating the generation schedule of the grid element.
    # The method sums up the generation schedules of all subordinated balancing groups
    def gen_schedule_calc(self):
        self.gen_P_schedule = 0.0
        for i in self.array_subordinates:
            i.gen_schedule_calc()
            self.gen_P_schedule += i.gen_P_schedule

    # Method calculating the load of the grid element.
    # The method sums up the load of all subordinated grid elements
    def load_calc(self):
        self.load_P = 0.0
        for i in self.array_subordinates:
            i.load_calc()
            self.load_P += i.load_P

    # Method calculating the load schedule of the grid element.
    # The method sums up the load schedules of all subordinated balancing groups
    def load_schedule_calc(self):
        self.load_P_schedule = 0.0
        for i in self.array_subordinates:
            i.load_schedule_calc()
            self.load_P_schedule += i.load_P_schedule

    # Method initializing the schedule for generation and load.
    # The method calls a method of the same name in all subordinated grid elements
    # and sets the current generation and load as the schedule.
    def schedule_init(self):
        for i in self.array_subordinates:
            i.schedule_init()
        self.gen_P_schedule = self.gen_P
        self.load_P_schedule = self.load_P

    # Method calculating the imbalance of the grid element.
    # The method sums up the imbalance of all subordinated grid elements
    def imba_calc(self):
        for i in self.array_subordinates:
            i.imba_calc()
        self.imba_P_ph = self.gen_P - self.load_P + self.aFRR_P + self.mFRR_P + self.sb_P
        self.imba_P_sc = self.imba_P_sc = self.gen_P - self.gen_P_schedule - self.load_P + self.load_P_schedule + self.sb_P

    # Method calculating the FCR parameter 'FCR_lambda' of the grid element.
    # The method sums up 'FCR_lambda' of all subordinated grid elements
    def fcr_init(self):
        self.FCR_lambda = 0.0
        for i in self.array_subordinates:
            i.fcr_init()
            self.FCR_lambda += i.FCR_lambda

    # Method calculating the activated FCR power of the grid element.
    # The method sums up the activated FCR power of all subordinated grid elements
    def fcr_calc(self, f_delta):
        self.FCR_P = 0.0
        for i in self.array_subordinates:
            i.fcr_calc(f_delta=f_delta)
            self.FCR_P += i.FCR_P

    # Method initializing the delay of aFRR activation in all subordinated grid elements.
    def afrr_init(self, t_step):
        for i in self.array_subordinates:
            i.afrr_init(t_step=t_step)

    # Method calculating the activated aFRR power of the grid element.
    # The method sums up the activated aFRR power of all subordinated grid elements
    def afrr_calc(self, f_delta, k_now, t_now, t_step, t_isp):
        self.aFRR_P = 0.0
        self.sb_P = 0.0
        for i in self.array_subordinates:
            i.afrr_calc(f_delta=self.f_delta,
                        k_now=k_now,
                        t_now=t_now,
                        t_step=t_step,
                        t_isp=t_isp)
            self.aFRR_P += i.aFRR_P
            self.sb_P += i.sb_P

    # Method calculating the activated mFRR power of the grid element
    # The method sums up the activated aFRR power of all subordinated grid elements
    def mfrr_calc(self, t_now, t_step, t_isp):
        self.mFRR_P = 0.0
        for i in self.array_subordinates:
            i.mfrr_calc(t_now=t_now,
                        t_step=t_step,
                        t_isp=t_isp)
            self.mFRR_P += i.mFRR_P

    # Method called after an MOL update to trigger further calculations
    def mol_update(self):
        for i in self.array_subordinates:
            i.mol_update()

    # Method calculating the costs for consumed energy and the income of produced energy of the grid element.
    # The method sums up the costs and income of all subordinated grid elements
    def energy_costs_calc(self, k_now, t_now, t_step, t_isp):
        self.gen_income = 0.0
        self.load_costs = 0.0
        self.gen_income_period = 0.0
        self.load_costs_period = 0.0
        for i in self.array_subordinates:
            i.energy_costs_calc(k_now=k_now,
                                t_now=t_now,
                                t_step=t_step,
                                t_isp=t_isp)
            self.gen_income += i.gen_income
            self.load_costs += i.load_costs
            self.gen_income_period += i.gen_income_period
            self.load_costs_period += i.load_costs_period

    def readarray(self, k_now):
        for i in self.array_subordinates:
            i.readarray(k_now=k_now)

    # Method writing all current variables for frequency, load flow, FCR, and aFRR
    # by appending them to the respective arrays.
    # The method further calls the method of the same name in all subordinated grid elements.
    def write_results(self):
        for i in self.array_subordinates:
            i.write_results()
        self.array_gen_P.append(self.gen_P)
        self.array_load_P.append(self.load_P)
        self.array_gen_P_schedule.append(self.gen_P_schedule)
        self.array_load_P_schedule.append(self.load_P_schedule)
        self.array_imba_P_ph.append(self.imba_P_ph)
        self.array_imba_P_sc.append(self.imba_P_sc)
        self.array_FCR_P.append(self.FCR_P)
        self.array_aFRR_P.append(self.aFRR_P)
        self.array_aFRR_P_pos.append(self.aFRR_P_pos)
        self.array_aFRR_P_neg.append(self.aFRR_P_neg)
        self.array_mFRR_P.append(self.mFRR_P)
        self.array_mFRR_P_pos.append(self.mFRR_P_pos)
        self.array_mFRR_P_neg.append(self.mFRR_P_neg)
        self.array_sb_P.append(self.sb_P)
        self.array_gen_income.append(self.gen_income)
        self.array_load_costs.append(self.load_costs)
        self.array_gen_income_period.append(self.gen_income_period)
        self.array_load_costs_period.append(self.load_costs_period)



# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITION FOR GRID ELEMENTS WITHOUT SUBORDINATED GRID ELEMENTS --------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# The class 'CalculatingGridElement' can be used for Coordination Centers, Control Blocks, and Control Areas.
# Variables for load flow, FCR, and aFRR are calculated by the respective methods.
# An object of the class 'CalculatingGridElement' does not have any subordinated grid elements.

class CalculatingGridElement(GridElement):

    # CONSTRUCTOR METHOD
    # The FCR and aFRR constants correspond the UCTE grid code
    def __init__(self,
                 name,              # name of the grid element                      (string)
                 gen_P,             # generator power in MW                         (float)
                 load_P,            # load in MW                                    (float)
                 FCR_lambda,        # FCR parameter 'lambda' in MW/Hz               (float)
                 aFRR_Kr,           # aFRR constant 'Kr' in MW/Hz                   (float)
                 aFRR_T,            # aFRR time constant 'T' in s                   (float)
                 aFRR_beta,         # aFRR constant 'beta' in p.u.                  (float)
                 aFRR_delay):       # delay time for the activation of aFRR in s    (float)

        # Other parameters are inherited from the super class 'GridElement'
        GridElement.__init__(self, name=name)

        # Load flow parameters
        self.gen_P = gen_P
        self.load_P = load_P

        # FCR constants
        self.FCR_lambda = FCR_lambda

        # FRCE signal
        self.FRCE = 0.0

        self.array_FRCE = []

        # aFRR constants
        self.aFRR_Kr = aFRR_Kr
        self.aFRR_T = aFRR_T
        self.aFRR_beta = aFRR_beta
        self.aFRR_delay = aFRR_delay

        # aFRR variables
        self.FRCE_ol = 0.0
        self.FRCE_ol_pos = 0.0
        self.FRCE_ol_neg = 0.0
        self.FRCE_cl_pos = 0.0
        self.FRCE_cl_neg = 0.0
        self.aFRR_ref = 0.0
        self.aFRR_ref_pos = 0.0
        self.aFRR_ref_neg = 0.0

        self.array_FRCE_ol = []
        self.array_FRCE_ol_pos = []
        self.array_FRCE_ol_neg = []
        self.array_FRCE_cl_pos = []
        self.array_FRCE_cl_neg = []
        self.array_aFRR_ref = []
        self.array_aFRR_ref_pos = []
        self.array_aFRR_ref_neg = []

        # Variable for the current day-ahead price
        self.da_price = 0.0

        # Array acting as delay of aFRR activation
        self.aFRR_queue_len = 0
        self.aFRR_queue = []
        self.aFRR_pos_queue = []
        self.aFRR_neg_queue = []

    def gen_calc(self):
        pass

    def gen_schedule_calc(self):
        pass

    def load_calc(self):
        pass

    def load_schedule_calc(self):
        pass

    # Method setting the current generation and load as the schedule
    def schedule_init(self):
        self.gen_P_schedule = self.gen_P
        self.load_P_schedule = self.load_P

    # Method calculating the imbalance of the grid element.
    # The imbalance is defined as a deviation from the schedule.
    # The method further calculates the open loop FRCE signal.
    def imba_calc(self):
        self.imba_P_ph = self.gen_P - self.load_P + self.aFRR_P + self.sb_P
        self.imba_P_sc = self.gen_P - self.gen_P_schedule - self.load_P + self.load_P_schedule + self.aFRR_P + self.mFRR_P
        self.FRCE = - self.imba_P_sc
        self.FRCE_ol = self.gen_P_schedule - self.gen_P + self.load_P - self.load_P_schedule
        if self.FRCE_ol > 0:
            self.FRCE_ol_pos = self.FRCE_ol
            self.FRCE_ol_neg = 0.0
        elif self.FRCE_ol < 0:
            self.FRCE_ol_pos = 0.0
            self.FRCE_ol_neg = self.FRCE_ol
        elif self.FRCE_ol == 0:
            self.FRCE_ol_pos = 0.0
            self.FRCE_ol_neg = 0.0
        else:
            pass

    def fcr_init(self):
        pass

    # Method calculating the activated FCR power
    # as function of a frequency deviation and 'FCR_lambda'.
    def fcr_calc(self, f_delta):
        self.FCR_P = -(self.FCR_lambda * f_delta)

    # Method initializing an array acting as the time delay for the activation of aFRR
    # The array has one element for each time step, that the signal is delayed.
    # All element of the array are set to zero.
    def afrr_init(self, t_step):
        self.aFRR_queue_len = math.ceil(self.aFRR_delay / t_step)
        i = 0
        while i < self.aFRR_queue_len:
            self.aFRR_queue.append(self.aFRR_ref)
            self.aFRR_pos_queue.append(self.aFRR_ref_pos)
            self.aFRR_neg_queue.append(self.aFRR_ref_neg)
            i += 1

    # Method calculating the aFRR using a discrete PI controller.
    # All aFRR related variables except for the open loop FRCE signal are processed in this method.
    def afrr_calc(self, f_delta, k_now, t_now, t_step, t_isp):
        self.FRCE_cl_pos_before = self.FRCE_cl_pos
        self.FRCE_cl_neg_before = self.FRCE_cl_neg

        self.FRCE_cl_pos = self.FRCE_ol_pos - self.aFRR_P_pos
        self.FRCE_cl_neg = self.FRCE_ol_neg - self.aFRR_P_neg

        self.aFRR_ref_pos = (self.aFRR_ref_pos + (1 / t_step)
                         * (self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_pos + (1 / t_step)
                         * (-self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_pos_before)
        self.aFRR_pos_queue.append(self.aFRR_ref_pos)
        self.aFRR_P_pos = self.aFRR_pos_queue.pop(0)

        self.aFRR_ref_neg = (self.aFRR_ref_neg + (1 / t_step)
                         * (self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_neg + (1 / t_step)
                         * (-self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_neg_before)
        self.aFRR_neg_queue.append(self.aFRR_ref_neg)
        self.aFRR_P_neg = self.aFRR_neg_queue.pop(0)

        self.aFRR_P = self.aFRR_P_pos + self.aFRR_P_neg

    # Method calculating the activated mFRR power of the grid element
    # No functionality implemented in this class
    def mfrr_calc(self, t_now, t_step, t_isp):
        pass

    # Method calculating the costs for consumed energy and the income of produced energy of the grid element.
    # The method multiplies the consumed and produced amounts of energy per t_step with the current day-ahead price
    # In this class, day-ahead prices are not implemented, which is why, self.da_price is set to zero...
    # ...resulting in costs and income equal to zero for all objects of this class
    def energy_costs_calc(self, k_now, t_now, t_step, t_isp):
        # Calculation of costs and income for the whole simulation
        self.gen_income += self.gen_P_schedule * self.da_price * t_step / 3600
        self.load_costs += self.load_P_schedule * self.da_price * t_step / 3600

        # Calculation of costs and income per ISP
        # Variables get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.gen_income_period = 0.0
            self.load_costs_period = 0.0

        self.gen_income_period += self.gen_P_schedule * self.da_price * t_step / 3600
        self.load_costs_period += self.load_P_schedule * self.da_price * t_step / 3600


    # Method writing all current variables for frequency, load flow, FCR, and aFRR
    # by appending them to the respective arrays.
    def write_results(self):
        self.array_gen_P.append(self.gen_P)
        self.array_load_P.append(self.load_P)
        self.array_gen_P_schedule.append(self.gen_P_schedule)
        self.array_load_P_schedule.append(self.load_P_schedule)
        self.array_imba_P_ph.append(self.imba_P_ph)
        self.array_imba_P_sc.append(self.imba_P_sc)
        self.array_FCR_P.append(self.FCR_P)
        self.array_FRCE.append(self.FRCE)
        self.array_FRCE_ol.append(self.FRCE_ol)
        self.array_FRCE_ol_pos.append(self.FRCE_ol_pos)
        self.array_FRCE_ol_neg.append(self.FRCE_ol_neg)
        self.array_FRCE_cl_pos.append(self.FRCE_cl_pos)
        self.array_FRCE_cl_neg.append(self.FRCE_cl_neg)
        self.array_aFRR_ref.append(self.aFRR_ref)
        self.array_aFRR_ref_pos.append(self.aFRR_ref_pos)
        self.array_aFRR_ref_neg.append(self.aFRR_ref_neg)
        self.array_aFRR_P.append(self.aFRR_P)
        self.array_aFRR_P_pos.append(self.aFRR_P_pos)
        self.array_aFRR_P_neg.append(self.aFRR_P_neg)
        self.array_mFRR_P.append(self.mFRR_P)
        self.array_mFRR_P_pos.append(self.mFRR_P_pos)
        self.array_mFRR_P_neg.append(self.mFRR_P_neg)
        self.array_gen_income.append(self.gen_income)
        self.array_load_costs.append(self.load_costs)
        self.array_gen_income_period.append(self.gen_income_period)
        self.array_load_costs_period.append(self.load_costs_period)



# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITION FOR SYNCHRONOUS ZONES ---------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# A synchronous zone is made up of subordinated grid elements.
# An object of the class 'SynchronousZone' is not to be subordinated to other grid elements.
# The unique property of a synchronous zone is the system-wide grid frequency f.

class SynchronousZone(GridElement):

    # CONSTRUCTOR METHOD
    def __init__(self,
                 name,                  # name of the synchronous zone                  (string)
                 f_nom):                # nominal frequency in Hz                       (float)

        # Initialization of frequency constants and variables
        self.f_nom = f_nom
        self.f = f_nom
        self.f_delta = 0.0

        self.array_f = []

        # Other parameters are inherited from the super class 'GridElement'
        GridElement.__init__(self,
                             name=name)

    # Method calculating the system frequency and the frequency deviation
    # as a function of the system wide imbalance of generation and load
    # and the FCR constant 'FCR_lambda'.
    def f_calc(self):
        self.f_delta = self.imba_P_ph / self.FCR_lambda
        self.f = self.f_nom + self.f_delta

    # Method calculating the activated FCR power of the system.
    # The method sums up the activated FCR power of all subordinated grid elements
    def fcr_calc(self):
        self.FCR_P = 0.0
        for i in self.array_subordinates:
            i.fcr_calc(f_delta=self.f_delta)
            self.FCR_P += i.FCR_P

    # Method calculating the activated aFRR power of the system
    # The method sums up the activated aFRR power of all subordinated grid elements
    def afrr_calc(self, k_now, t_now, t_step, t_isp):
        self.aFRR_P = 0.0
        self.sb_P = 0.0
        for i in self.array_subordinates:
            i.afrr_calc(f_delta=self.f_delta,
                        k_now=k_now,
                        t_now=t_now,
                        t_step=t_step,
                        t_isp=t_isp)
            self.aFRR_P += i.aFRR_P
            self.sb_P += i.sb_P

    # Method calculating the total activated mFRR power of the system
    # The method sums up the activated aFRR power of all subordinated grid elements
    def mfrr_calc(self, t_now, t_step, t_isp):
        self.mFRR_P = 0.0
        for i in self.array_subordinates:
            i.mfrr_calc(t_now= t_now,
                        t_step=t_step,
                        t_isp=t_isp)
            self.mFRR_P += i.mFRR_P

    # Method writing all current variables for frequency, load flow, FCR, and aFRR
    # by appending them to the respective arrays.
    # The method further calls the method of the same name in all subordinated grid elements.
    def write_results(self):
        for i in self.array_subordinates:
            i.write_results()
        self.array_f.append(self.f)
        self.array_gen_P.append(self.gen_P)
        self.array_load_P.append(self.load_P)
        self.array_gen_P_schedule.append(self.gen_P_schedule)
        self.array_load_P_schedule.append(self.load_P_schedule)
        self.array_imba_P_ph.append(self.imba_P_ph)
        self.array_imba_P_sc.append(self.imba_P_sc)
        self.array_FCR_P.append(self.FCR_P)
        self.array_aFRR_P.append(self.aFRR_P)
        self.array_mFRR_P.append(self.mFRR_P)
        self.array_sb_P.append(self.sb_P)
        self.array_gen_income.append(self.gen_income)
        self.array_load_costs.append(self.load_costs)
        self.array_gen_income_period.append(self.gen_income_period)
        self.array_load_costs_period.append(self.load_costs_period)



# ----------------------------------------------------------------------------------------------------------------------
# --- CLASS DEFINITION FOR CONTROL AREAS -------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# The class 'ControlArea' is to be used for Control Areas with subordinated Balancing Groups.
# The class largely corresponds the class 'CalculatingGridElement'.

class ControlArea(CalculatingGridElement):

    # CONSTRUCTOR METHOD
    # The FCR and aFRR constants correspond the UCTE grid code
    def __init__(self,
                 name,                  # name of the grid element                                  (string)
                 FCR_lambda,            # FCR parameter 'lambda' in MW/Hz                           (float)
                 aFRR_Kr,               # aFRR constant 'Kr' in MW/Hz                               (float)
                 aFRR_T,                # aFRR time constant 'T' in s                               (float)
                 aFRR_beta,             # aFRR constant 'beta' in p.u.                              (float)
                 aFRR_delay,            # delay time for the activation of aFRR in s                (float)
                 mFRR_trigger,          # ratio of aFRR, at which mFRR gets triggered in p.u.       (float)
                 mFRR_target,           # target ratio for aFRR reduction by mFRR in p.u.           (float)
                 mFRR_time,             # time of each ISP in s, at which mFRR decision is taken    (float)
                 sb_delay):             # delay time of the Smart Balancing signal in s             (float)

        # Other parameters are inherited from the super class 'CalculatingGridElement'
        CalculatingGridElement.__init__(self,
                                        name=name,
                                        gen_P=0.0,
                                        load_P=0.0,
                                        FCR_lambda=FCR_lambda,
                                        aFRR_Kr=aFRR_Kr,
                                        aFRR_T=aFRR_T,
                                        aFRR_beta=aFRR_beta,
                                        aFRR_delay=aFRR_delay)

        # Variables for the amount of positive and negative aFRR energy
        self.aFRR_E_pos = 0.0
        self.aFRR_E_neg = 0.0
        self.aFRR_E_pos_period = 0.0
        self.aFRR_E_neg_period = 0.0
        self.aFRR_cap_pos = 0.0
        self.aFRR_cap_neg = 0.0

        self.array_aFRR_E_pos = []
        self.array_aFRR_E_neg = []
        self.array_aFRR_E_pos_period = []
        self.array_aFRR_E_neg_period = []
        self.array_aFRR_cap_pos = []
        self.array_aFRR_cap_neg = []

        # Positive and negative merit order lists for aFRR and price and costs variables
        self.array_aFRR_molpos = []
        self.array_aFRR_molneg = []

        # Various Variables for aFRR prices
        self.aFRR_price = 0.0
        self.aFRR_price_pos = 0.0
        self.aFRR_price_neg = 0.0
        self.aFRR_price_avg = 0.0
        self.aFRR_price_pos_avg = 0.0
        self.aFRR_price_neg_avg = 0.0
        self.aFRR_price_pos_max = 0.0
        self.aFRR_price_neg_max = 0.0

        self.array_aFRR_price = []
        self.array_aFRR_price_pos = []
        self.array_aFRR_price_neg = []
        self.array_aFRR_price_avg = []
        self.array_aFRR_price_pos_avg = []
        self.array_aFRR_price_neg_avg = []
        self.array_aFRR_price_pos_max = []
        self.array_aFRR_price_neg_max = []

        # Various Variables for aFRR costs
        self.aFRR_costs = 0.0
        self.aFRR_costs_pos = 0.0
        self.aFRR_costs_neg = 0.0
        self.aFRR_costs_period = 0.0
        self.aFRR_costs_pos_period = 0.0
        self.aFRR_costs_neg_period = 0.0

        self.array_aFRR_costs = []
        self.array_aFRR_costs_pos = []
        self.array_aFRR_costs_neg = []
        self.array_aFRR_costs_period = []
        self.array_aFRR_costs_pos_period = []
        self.array_aFRR_costs_neg_period = []

        # mFRR constants
        self.mFRR_trigger = mFRR_trigger
        self.mFRR_target = mFRR_target
        self.mFRR_time = mFRR_time

        # Positive and negative merit order lists for mFRR and price and costs variables
        self.array_mFRR_molpos = []
        self.array_mFRR_molneg = []

        # mFRR variables
        self.mFRR_P_pos_setp = 0.0
        self.mFRR_P_neg_setp = 0.0
        self.mFRR_E_pos = 0.0
        self.mFRR_E_neg = 0.0
        self.mFRR_E_pos_period = 0.0
        self.mFRR_E_neg_period = 0.0

        self.array_mFRR_E_pos = []
        self.array_mFRR_E_neg = []
        self.array_mFRR_E_pos_period = []
        self.array_mFRR_E_neg_period = []

        # Various Variables for mFRR prices
        self.mFRR_price = 0.0
        self.mFRR_price_pos = 0.0
        self.mFRR_price_neg = 0.0
        self.mFRR_price_avg = 0.0
        self.mFRR_price_pos_avg = 0.0
        self.mFRR_price_neg_avg = 0.0
        self.mFRR_price_pos_max = 0.0
        self.mFRR_price_neg_max = 0.0

        self.array_mFRR_price = []
        self.array_mFRR_price_pos = []
        self.array_mFRR_price_neg = []
        self.array_mFRR_price_avg = []
        self.array_mFRR_price_pos_avg = []
        self.array_mFRR_price_neg_avg = []
        self.array_mFRR_price_pos_max = []
        self.array_mFRR_price_neg_max = []

        # Various Variables for mFRR costs
        self.mFRR_costs = 0.0
        self.mFRR_costs_pos = 0.0
        self.mFRR_costs_neg = 0.0
        self.mFRR_costs_period = 0.0
        self.mFRR_costs_pos_period = 0.0
        self.mFRR_costs_neg_period = 0.0

        self.array_mFRR_costs = []
        self.array_mFRR_costs_pos = []
        self.array_mFRR_costs_neg = []
        self.array_mFRR_costs_period = []
        self.array_mFRR_costs_pos_period = []
        self.array_mFRR_costs_neg_period = []

        # AEP variables
        self.AEP = 0.0
        self.AEP_max_period = 0.0

        self.array_AEP = []
        self.array_AEP_max_period = []

        # Variable for the smart balancing control signal
        self.FRCE_sb = 0.0

        self.array_FRCE_sb = []

        # Parameter defining the delay time of the Smart Balancing signal
        self.sb_delay = sb_delay

        # Variable for the activated smart balancing power
        self.sb_P = 0.0

        self.array_sb_P = []

        # Array acting as delay of the Smart Balancing signal
        self.sb_queue_len = 0
        self.sb_queue = []

        # Array containing the subordinated Balancing Groups
        self.array_balancinggroups = []

        # Variable and array for DA prices
        self.da_price = 0.0
        self.array_da_prices = []

    # Method initializing the schedule for generation and load.
    # The method calls a method of the same name in all subordinated Balancing Groups
    # and sets the current generation and load as the schedule.
    def schedule_init(self):
        for i in self.array_balancinggroups:
            i.schedule_init()
        self.gen_P_schedule = self.gen_P
        self.load_P_schedule = self.load_P

    # Method initializing an array acting as the time delay for the activation of aFRR
    # The array has one element for each time step, that the signal is delayed.
    # All element of the array are set to zero.
    # Additionally, an equivalent array is initialized for the Smart Balancing signal
    def afrr_init(self, t_step):
        self.aFRR_queue_len = math.ceil(self.aFRR_delay / t_step)
        i = 0
        while i < self.aFRR_queue_len:
            self.aFRR_queue.append(self.aFRR_ref)
            self.aFRR_pos_queue.append(self.aFRR_ref_pos)
            self.aFRR_neg_queue.append(self.aFRR_ref_neg)
            i += 1

        # Initialization of Smart Balancing
        self.sb_queue_len = math.ceil(self.sb_delay / t_step)
        i = 0
        while i < self.sb_queue_len:
            self.sb_queue.append(0)
            i += 1

        # Initialization of arrays for positive and negative Smart Balancing Assets
        for i in self.array_balancinggroups:
            i.sb_init()

    # Method calculating the imbalance of the Control Area.
    # The method sums up the imbalance of all subordinated Balancing Groups
    def imba_calc(self):
        for i in self.array_balancinggroups:
            i.imba_calc()
        self.imba_P_ph = self.gen_P - self.load_P + self.aFRR_P + self.mFRR_P + self.sb_P
        self.imba_P_sc = self.gen_P - self.gen_P_schedule - self.load_P + self.load_P_schedule + self.sb_P
        self.FRCE = - self.imba_P_sc
        self.FRCE_ol = - self.imba_P_sc - self.mFRR_P
        if self.FRCE_ol > 0:
            self.FRCE_ol_pos = self.FRCE_ol
            self.FRCE_ol_neg = 0.0
        elif self.FRCE_ol < 0:
            self.FRCE_ol_pos = 0.0
            self.FRCE_ol_neg = self.FRCE_ol
        elif self.FRCE_ol == 0:
            self.FRCE_ol_pos = 0.0
            self.FRCE_ol_neg = 0.0
        else:
            pass

    # Method calculating the generator power of the grid element.
    # The method sums up the generator power of all subordinated balancing groups
    def gen_calc(self):
        self.gen_P = 0.0
        for i in self.array_balancinggroups:
            i.gen_calc()
            self.gen_P += i.gen_P

    # Method calculating the generation schedule of the grid element.
    # The method sums up the generation schedules of all subordinated balancing groups
    def gen_schedule_calc(self):
        self.gen_P_schedule = 0.0
        for i in self.array_balancinggroups:
            self.gen_P_schedule += i.gen_P_schedule

    # Method calculating the load of the grid element.
    # The method sums up the load of all subordinated balancing groups
    def load_calc(self):
        self.load_P = 0.0
        for i in self.array_balancinggroups:
            i.load_calc()
            self.load_P += i.load_P

    # Method calculating the load schedule of the grid element.
    # The method sums up the load schedules of all subordinated balancing groups
    def load_schedule_calc(self):
        self.load_P_schedule = 0.0
        for i in self.array_balancinggroups:
            self.load_P_schedule += i.load_P_schedule

    # Method calculating the activated aFRR power of the system.
    # Added call of method afrr_price_calc for this class.
    # Added activation of smart balancing in subordinated Balancing Groups
    def afrr_calc(self, f_delta, k_now, t_now, t_step, t_isp):
        self.FRCE_cl_pos_before = self.FRCE_cl_pos
        self.FRCE_cl_neg_before = self.FRCE_cl_neg

        self.FRCE_cl_pos = self.FRCE_ol_pos - self.aFRR_P_pos
        self.FRCE_cl_neg = self.FRCE_ol_neg - self.aFRR_P_neg

        self.aFRR_ref_pos = (self.aFRR_ref_pos + (1 / t_step)
                         * (self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_pos + (1 / t_step)
                         * (-self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_pos_before)
        self.aFRR_pos_queue.append(self.aFRR_ref_pos)
        self.aFRR_P_pos = self.aFRR_pos_queue.pop(0)

        self.aFRR_ref_neg = (self.aFRR_ref_neg + (1 / t_step)
                         * (self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_neg + (1 / t_step)
                         * (-self.aFRR_beta + t_step / 2
                         * (1 / self.aFRR_T * t_step))
                         * self.FRCE_cl_neg_before)
        self.aFRR_neg_queue.append(self.aFRR_ref_neg)
        self.aFRR_P_neg = self.aFRR_neg_queue.pop(0)

        self.aFRR_P = self.aFRR_P_pos + self.aFRR_P_neg

        # Calculation of positive and negative aFRR energy
        self.aFRR_E_pos += self.aFRR_P_pos * t_step / 3600
        self.aFRR_E_neg += self.aFRR_P_neg * t_step / 3600

        # Calculation of positive and negative aFRR energy per ISP
        # Get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.aFRR_E_pos_period = 0.0
            self.aFRR_E_neg_period = 0.0

        self.aFRR_E_pos_period += self.aFRR_P_pos * t_step / 3600
        self.aFRR_E_neg_period += self.aFRR_P_neg * t_step / 3600

        # Calculation of aFRR prices and costs and the AEP
        self.afrr_price_calc(t_now=t_now,
                             t_step=t_step)
        self.afrr_costs_calc(t_now=t_now,
                             t_step=t_step,
                             t_isp=t_isp)

        # Calculation of Smart Balancing price signal
        self.sb_signal()

        # Activate Smart Balancing in subordinated Balancing Groups
        self.da_price = self.array_da_prices[k_now]
        self.sb_P = 0.0
        for i in self.array_balancinggroups:
            i.afrr_calc(t_now=t_now,
                        t_step=t_step,
                        t_isp=t_isp,
                        AEP=self.AEP)
            i.sb_calc(FRCE_sb=self.FRCE_sb,
                      AEP=self.AEP,
                      t_step=t_step,
                      t_now=t_now,
                      da_price=self.da_price)
            self.sb_P += i.sb_P

    # Method calculating a price for aFRR using the merit order lists
    def afrr_price_calc(self, t_now, t_step):
        # Combined aFRR price calculation
        # Depending on the algebraic sign of the area control error (self.FRCE_ol), the positive OR negative MOL is used...
        # ...to calculate one combined aFRR price (self.aFRR_price & self.aFRR_price_avg)
        array_aFRR_prices = []
        array_aFRR_powers = []

        # Negative MOL is used, if FRCE_ol < 0
        if self.FRCE_ol < 0:
            i = 0
            aFRR_demand = 0.0
            array_aFRR_prices = []
            array_aFRR_powers = []

            # Identification of necessary negative aFRR assets to compensate the FRCE_ol
            # Calculation of highest negative aFRR price
            n = len(self.array_aFRR_molneg['Power'])
            while aFRR_demand > self.FRCE_ol:
                if n == i:
                    print('WARNING! Insufficient negative aFRR at t =', t_now,'!')
                    aFRR_demand = self.FRCE_ol
                else:
                    if aFRR_demand + self.array_aFRR_molneg['Power'][i] < self.FRCE_ol:
                        load_factor = abs((aFRR_demand - self.FRCE_ol) / self.array_aFRR_molneg['Power'][i])
                    else:
                        load_factor = 1.0

                    self.aFRR_price = self.array_aFRR_molneg['Price'][i]
                    array_aFRR_prices.append(self.aFRR_price)
                    array_aFRR_powers.append(self.array_aFRR_molneg['Power'][i] * load_factor)
                    aFRR_demand += self.array_aFRR_molneg['Power'][i]
                i += 1

        # Positive MOL is used, if FRCE_ol < 0
        elif self.FRCE_ol > 0:
            i = 0
            aFRR_demand = 0.0
            array_aFRR_prices = []
            array_aFRR_powers = []

            # Identification of necessary positive aFRR assets to compensate the FRCE_ol
            # Calculation of highest positive aFRR price
            n = len(self.array_aFRR_molpos['Power'])
            while aFRR_demand < self.FRCE_ol:
                if n == i:
                    print('WARNING! Insufficient positive aFRR at t =', t_now,'!')
                    aFRR_demand = self.FRCE_ol
                else:
                    if aFRR_demand + self.array_aFRR_molpos['Power'][i] > self.FRCE_ol:
                        load_factor = (self.FRCE_ol - aFRR_demand) / self.array_aFRR_molpos['Power'][i]
                    else:
                        load_factor = 1.0
                    self.aFRR_price = self.array_aFRR_molpos['Price'][i]
                    array_aFRR_prices.append(self.aFRR_price)
                    array_aFRR_powers.append(self.array_aFRR_molpos['Power'][i] * load_factor)
                    aFRR_demand += self.array_aFRR_molpos['Power'][i]
                i += 1
        else:
            array_aFRR_prices = []

        # Calculation of average aFRR price
        number_of_aFRR = 0
        powers_of_aFRR = 0.0
        for k in array_aFRR_powers:
            number_of_aFRR += 1
            powers_of_aFRR += k

        prices_of_aFRR = 0.0
        i = 0
        for k in array_aFRR_prices:
            prices_of_aFRR += k * (array_aFRR_powers[i] / powers_of_aFRR)
            i += 1

        self.aFRR_price_avg = prices_of_aFRR

        # Seperate calculation of positive aFRR price and negative aFRR price
        # Both variables can be greater zero at a given point in time
        # If self.FRCE_ol < 0...
        # ...the negative MOL (self.array_aFRR_molneg) is used to update the negative aFRR price (self.aFRR_price_neg & self.aFRR_price_neg_avg)
        if self.FRCE_ol < 0:
            i = 0
            aFRR_demand = 0.0
            number_of_aFRR = 0
            powers_of_aFRR = 0.0
            prices_of_aFRR = 0.0
            array_aFRR_neg_prices = []
            array_aFRR_neg_powers = []

            # Identification of necessary negative aFRR assets to compensate the FRCE_ol
            # Calculation of highest negative aFRR price
            n = len(self.array_aFRR_molneg['Power'])
            while aFRR_demand > self.FRCE_ol:
                if n == i:
                    #print('WARNING! Insufficient negative aFRR at t =', t_now,'!')
                    aFRR_demand = self.FRCE_ol
                else:
                    if aFRR_demand + self.array_aFRR_molneg['Power'][i] < self.FRCE_ol:
                        load_factor = abs((aFRR_demand - self.FRCE_ol) / self.array_aFRR_molneg['Power'][i])
                    else:
                        load_factor = 1.0
                    self.aFRR_price_neg = self.array_aFRR_molneg['Price'][i]
                    array_aFRR_neg_prices.append(self.aFRR_price_neg)
                    array_aFRR_neg_powers.append(self.array_aFRR_molneg['Power'][i] * load_factor)
                    aFRR_demand += self.array_aFRR_molneg['Power'][i]
                i += 1

            # Calculation of average negative aFRR price
            for k in array_aFRR_powers:
                number_of_aFRR += 1
                powers_of_aFRR += k

            i = 0
            for k in array_aFRR_prices:
                prices_of_aFRR += k * (array_aFRR_powers[i] / powers_of_aFRR)
                i += 1

            self.aFRR_price_neg_avg = prices_of_aFRR

            self.aFRR_price_neg_max = self.aFRR_price_neg
            self.aFRR_price_pos_max = 0.0

        # If self.FRCE_ol > 0...
        # ...the positive MOL (self.array_aFRR_molpos) is used to update the positive aFRR price (self.aFRR_price_pos & self.aFRR_price_pos_avg)
        if self.FRCE_ol > 0:
            i = 0
            aFRR_demand = 0.0
            number_of_aFRR = 0
            powers_of_aFRR = 0.0
            prices_of_aFRR = 0.0
            array_aFRR_pos_prices = []
            array_aFRR_pos_powers = []

            # Identification of necessary positive aFRR assets to compensate the FRCE_ol
            # Calculation of highest positive aFRR price
            n = len(self.array_aFRR_molpos['Power'])
            while aFRR_demand < self.FRCE_ol:
                if n == i:
                    #print('WARNING! Insufficient negative aFRR at t =', t_now,'!')
                    aFRR_demand = self.FRCE_ol
                else:
                    if aFRR_demand + self.array_aFRR_molpos['Power'][i] > self.FRCE_ol:
                        load_factor = (self.FRCE_ol - aFRR_demand) / self.array_aFRR_molpos['Power'][i]
                    else:
                        load_factor = 1.0
                    self.aFRR_price_pos = self.array_aFRR_molpos['Price'][i]
                    array_aFRR_pos_prices.append(self.aFRR_price_pos)
                    array_aFRR_pos_powers.append(self.array_aFRR_molpos['Power'][i] * load_factor)
                    aFRR_demand += self.array_aFRR_molpos['Power'][i]
                i += 1

            # Calculation of average positive aFRR price
            for k in array_aFRR_powers:
                number_of_aFRR += 1
                powers_of_aFRR += k

            i = 0
            for k in array_aFRR_prices:
                prices_of_aFRR += k * (array_aFRR_powers[i] / powers_of_aFRR)
                i += 1

            self.aFRR_price_pos_avg = prices_of_aFRR

            self.aFRR_price_pos_max = self.aFRR_price_pos
            self.aFRR_price_neg_max = 0.0

    # Method calculating the costs of aFRR
    def afrr_costs_calc(self, t_now, t_step, t_isp):
        # Calculation of combined aFRR costs
        self.aFRR_costs += self.aFRR_P * self.aFRR_price_avg * t_step / 3600

        # Calculation of combined aFRR costs per ISP
        # Get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.aFRR_costs_period = 0

        self.aFRR_costs_period += self.aFRR_P * self.aFRR_price_avg * t_step / 3600

        # Calculation of positive and negative aFRR costs
        self.aFRR_costs_pos += self.aFRR_P_pos * self.aFRR_price_pos_avg * t_step / 3600
        self.aFRR_costs_neg += -self.aFRR_P_neg * self.aFRR_price_neg_avg * t_step / 3600

        # Calculation of positive and negative aFRR costs per ISP
        # Get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.aFRR_costs_pos_period = 0
            self.aFRR_costs_neg_period = 0

        self.aFRR_costs_pos_period += self.aFRR_P_pos * self.aFRR_price_pos_avg * t_step / 3600
        self.aFRR_costs_neg_period += -self.aFRR_P_neg * self.aFRR_price_neg_avg * t_step / 3600

    # Method calculating the activated mFRR power of the Control Area
    def mfrr_calc(self, t_now, t_step, t_isp):
        # mFRR activation using the average FRCE
        if t_now == 0:
            self.array_FRCE_avg = []
            self.FRCE_sum = 0.0
            self.FRCE_avg = 0.0
        else:
            if ((t_now + t_step) % t_isp) == 0:
                self.array_FRCE_avg = []
            else:
                self.FRCE_sum = 0.0
                self.array_FRCE_avg.append(self.FRCE)
                n = len(self.array_FRCE_avg)
                i = 1
                while (i <= n):
                    self.FRCE_sum += self.array_FRCE_avg[i - 1]
                    self.FRCE_avg = self.FRCE_sum / i
                    i += 1

        if ((t_now - self.mFRR_time) % t_isp) == 0:
            if self.FRCE_avg > 0 and self.FRCE_avg > self.mFRR_trigger * self.aFRR_cap_pos:
                self.mFRR_P_pos_setp = self.FRCE_avg - self.aFRR_cap_pos * self.mFRR_target
                self.mFRR_P_pos_setp = int((self.mFRR_P_pos_setp + 100) / 100) * 100
                #print(self.mFRR_P_pos_setp, 'of pos. mFRR power to be activated in the next ISP')
            else:
                self.mFRR_P_pos_setp = 0.0

            if self.FRCE_avg < 0 and self.FRCE_avg < self.mFRR_trigger * self.aFRR_cap_neg:
                self.mFRR_P_neg_setp = (self.aFRR_E_neg_period * 3600 / self.mFRR_time) - self.aFRR_cap_neg * self.mFRR_target
                self.mFRR_P_neg_setp = int((self.mFRR_P_neg_setp - 100) / 100) * 100
                #print(self.mFRR_P_neg_setp, 'of neg. mFRR power to be activated in the next ISP')
            else:
                self.mFRR_P_neg_setp = 0.0

        # mFRR activation using the activated aFRR
        # if ((t_now - self.mFRR_time) % t_isp) == 0:
        #     if self.aFRR_E_pos_period > self.mFRR_trigger * self.aFRR_cap_pos * self.mFRR_time / 3600:
        #         self.mFRR_P_pos_setp = XXXX - self.aFRR_cap_pos * self.mFRR_target
        #         self.mFRR_P_pos_setp = int((self.mFRR_P_pos_setp + 100) / 100) * 100
        #     else:
        #         self.mFRR_P_pos_setp = 0.0
        #
        #     if self.aFRR_E_neg_period < self.mFRR_trigger * self.aFRR_cap_neg * self.mFRR_time / 3600:
        #         self.mFRR_P_neg_setp = (self.aFRR_E_neg_period * 3600 / self.mFRR_time) - self.aFRR_cap_neg * self.mFRR_target
        #         self.mFRR_P_neg_setp = int((self.mFRR_P_neg_setp - 100) / 100) * 100
        #     else:
        #         self.mFRR_P_neg_setp = 0.0

        if (t_now % t_isp) == 0:
            self.mFRR_P_pos = self.mFRR_P_pos_setp
            self.mFRR_P_neg = self.mFRR_P_neg_setp
            self.mFRR_P = self.mFRR_P_pos + self.mFRR_P_neg

            # Calculation of the mFRR price
            self.mfrr_price_calc(t_now=t_now,
                                 t_step=t_step)

        # Calculation of positive and negative mFRR energy
        self.mFRR_E_pos += self.mFRR_P_pos * t_step / 3600
        self.mFRR_E_neg += self.mFRR_P_neg * t_step / 3600

        # Calculation of positive and negative mFRR energy per ISP
        # Get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.mFRR_E_pos_period = 0.0
            self.mFRR_E_neg_period = 0.0

        self.mFRR_E_pos_period += self.mFRR_P_pos * t_step / 3600
        self.mFRR_E_neg_period += self.mFRR_P_neg * t_step / 3600

        # Calculation of mFRR costs
        self.mfrr_costs_calc(t_now=t_now,
                             t_step=t_step,
                             t_isp=t_isp)

        # Calculation of the AEP
        self.aep_calc(t_now=t_now,
                      t_step=t_step,
                      t_isp=t_isp)

    # Method calculating the mFRR prices
    # Only called at the beginning of an ISP, since mFRR is static for each ISP
    def mfrr_price_calc(self, t_now, t_step):
        # Combined mFRR price calculation
        # Depending on the algebraic sign of the mFRR power, the positive OR negative MOL is used...
        # ...to calculate one combined mFRR price (self.mFRR_price & self.mFRR_price_avg)
        array_mFRR_prices = []
        array_mFRR_powers = []

        # Negative mFRR MOL is used, if self.mFRR_P < 0
        if self.mFRR_P < 0:
            i = 0
            mFRR_demand = 0.0
            array_mFRR_prices = []
            array_mFRR_powers = []

            # Identification of necessary negative mFRR assets to sum up to the total mFRR power
            # Calculation of highest negative mFRR price
            n = len(self.array_mFRR_molneg['Power'])
            while mFRR_demand > self.mFRR_P:
                if n == i:
                    print('WARNING! Insufficient negative mFRR at t =', t_now,'!')
                    mFRR_demand = self.mFRR_P
                else:
                    if mFRR_demand + self.array_mFRR_molneg['Power'][i] < self.mFRR_P:
                        load_factor = abs((mFRR_demand - self.mFRR_P) / self.array_mFRR_molneg['Power'][i])
                    else:
                        load_factor = 1.0

                    self.mFRR_price = self.array_mFRR_molneg['Price'][i]
                    array_mFRR_prices.append(self.mFRR_price)
                    array_mFRR_powers.append(self.array_mFRR_molneg['Power'][i] * load_factor)
                    mFRR_demand += self.array_mFRR_molneg['Power'][i]
                i += 1

        # Positive mFRR MOL is used, if self.mFRR_P < 0
        elif self.mFRR_P > 0:
            i = 0
            mFRR_demand = 0.0
            array_mFRR_prices = []
            array_mFRR_powers = []

            # Identification of necessary positive mFRR assets to sum up to the total mFRR power
            # Calculation of highest positive mFRR price
            n = len(self.array_mFRR_molpos['Power'])
            while mFRR_demand < self.mFRR_P:
                if n == i:
                    print('WARNING! Insufficient positive mFRR at t =', t_now,'!')
                    mFRR_demand = self.mFRR_P
                else:
                    if mFRR_demand + self.array_mFRR_molpos['Power'][i] > self.mFRR_P:
                        load_factor = (self.mFRR_P - mFRR_demand) / self.array_mFRR_molpos['Power'][i]
                    else:
                        load_factor = 1.0
                    self.mFRR_price = self.array_mFRR_molpos['Price'][i]
                    array_mFRR_prices.append(self.mFRR_price)
                    array_mFRR_powers.append(self.array_mFRR_molpos['Power'][i] * load_factor)
                    mFRR_demand += self.array_mFRR_molpos['Power'][i]
                i += 1

        # All mFRR price signals get set to zero, if no mFRR is activated
        else:
            self.mFRR_price = 0.0
            self.mFRR_price_pos = 0.0
            self.mFRR_price_neg = 0.0
            self.mFRR_price_avg = 0.0
            self.mFRR_price_pos_avg = 0.0
            self.mFRR_price_neg_avg = 0.0
            self.mFRR_price_pos_max = 0.0
            self.mFRR_price_neg_max = 0.0
            array_mFRR_prices = []

        # Calculation of average mFRR price
        number_of_mFRR = 0
        powers_of_mFRR = 0.0
        for k in array_mFRR_powers:
            number_of_mFRR += 1
            powers_of_mFRR += k

        prices_of_mFRR = 0.0
        i = 0
        for k in array_mFRR_prices:
            prices_of_mFRR += k * (array_mFRR_powers[i] / powers_of_mFRR)
            i += 1

        self.mFRR_price_avg = prices_of_mFRR

        # Separate calculation of positive mFRR price and negative mFRR price
        # Both variables can be greater zero at a given point in time
        # If self.mFRR_P < 0...
        # ...the negative MOL (self.array_mFRR_molneg) is used
        # ...to update the negative mFRR price (self.mFRR_price_neg & self.mFRR_price_neg_avg)
        if self.mFRR_P < 0:
            i = 0
            mFRR_demand = 0.0
            number_of_mFRR = 0
            powers_of_mFRR = 0.0
            prices_of_mFRR = 0.0
            array_mFRR_neg_prices = []
            array_mFRR_neg_powers = []

            # Identification of necessary negative mFRR assets to sum up to the total mFRR power
            # Calculation of highest negative mFRR price
            n = len(self.array_mFRR_molneg['Power'])
            while mFRR_demand > self.mFRR_P:
                if n == i:
                    # print('WARNING! Insufficient negative mFRR at t =', t_now,'!')
                    mFRR_demand = self.mFRR_P
                else:
                    if mFRR_demand + self.array_mFRR_molneg['Power'][i] < self.mFRR_P:
                        load_factor = abs((mFRR_demand - self.mFRR_P) / self.array_mFRR_molneg['Power'][i])
                    else:
                        load_factor = 1.0
                    self.mFRR_price_neg = self.array_mFRR_molneg['Price'][i]
                    array_mFRR_neg_prices.append(self.mFRR_price_neg)
                    array_mFRR_neg_powers.append(self.array_mFRR_molneg['Power'][i] * load_factor)
                    mFRR_demand += self.array_mFRR_molneg['Power'][i]
                i += 1

            # Calculation of average negative mFRR price
            for k in array_mFRR_powers:
                number_of_mFRR += 1
                powers_of_mFRR += k

            i = 0
            for k in array_mFRR_prices:
                prices_of_mFRR += k * (array_mFRR_powers[i] / powers_of_mFRR)
                i += 1

            self.mFRR_price_neg_avg = prices_of_mFRR

            self.mFRR_price_neg_max = self.mFRR_price_neg
            self.mFRR_price_pos_max = 0.0

        # If self.mFRR_P > 0...
        # ...the positive MOL (self.array_mFRR_molpos) is used...
        # ...to update the positive mFRR price (self.mFRR_price_pos & self.mFRR_price_pos_avg)
        if self.mFRR_P > 0:
            i = 0
            mFRR_demand = 0.0
            number_of_mFRR = 0
            powers_of_mFRR = 0.0
            prices_of_mFRR = 0.0
            array_mFRR_pos_prices = []
            array_mFRR_pos_powers = []

            # Identification of necessary positive mFRR assets to sum up to the total mFRR power
            # Calculation of highest positive mFRR price
            n = len(self.array_mFRR_molpos['Power'])
            while mFRR_demand < self.mFRR_P:
                if n == i:
                    #print('WARNING! Insufficient negative mFRR at t =', t_now,'!')
                    mFRR_demand = self.mFRR_P
                else:
                    if mFRR_demand + self.array_mFRR_molpos['Power'][i] > self.mFRR_P:
                        load_factor = (self.mFRR_P - mFRR_demand) / self.array_mFRR_molpos['Power'][i]
                    else:
                        load_factor = 1.0
                    self.mFRR_price_pos = self.array_mFRR_molpos['Price'][i]
                    array_mFRR_pos_prices.append(self.mFRR_price_pos)
                    array_mFRR_pos_powers.append(self.array_mFRR_molpos['Power'][i] * load_factor)
                    mFRR_demand += self.array_mFRR_molpos['Power'][i]
                i += 1

            # Calculation of average positive mFRR price
            for k in array_mFRR_powers:
                number_of_mFRR += 1
                powers_of_mFRR += k

            i = 0
            for k in array_mFRR_prices:
                prices_of_mFRR += k * (array_mFRR_powers[i] / powers_of_mFRR)
                i += 1

            self.mFRR_price_pos_avg = prices_of_mFRR

            self.mFRR_price_pos_max = self.mFRR_price_pos
            self.mFRR_price_neg_max = 0.0

    # Method calculating the mFRR costs
    def mfrr_costs_calc(self, t_now, t_step, t_isp):
        # Calculation of combined mFRR costs
        self.mFRR_costs += abs(self.mFRR_P) * self.mFRR_price_avg * t_step / 3600

        # Calculation of combined mFRR costs per ISP
        # Get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.mFRR_costs_period = 0

        self.mFRR_costs_period += abs(self.mFRR_P) * self.mFRR_price_avg * t_step / 3600

        # Calculation of positive and negative mFRR costs
        self.mFRR_costs_pos += abs(self.mFRR_P_pos) * self.mFRR_price_pos_avg * t_step / 3600
        self.mFRR_costs_neg += -abs(self.mFRR_P_neg) * self.mFRR_price_neg_avg * t_step / 3600

        # Calculation of positive and negative mFRR costs per ISP
        # Get set to zero after every ISP
        if (t_now % t_isp) == 0:
            self.mFRR_costs_pos_period = 0
            self.mFRR_costs_neg_period = 0

        self.mFRR_costs_pos_period += abs(self.mFRR_P_pos) * self.mFRR_price_pos_avg * t_step / 3600
        self.mFRR_costs_neg_period += -abs(self.mFRR_P_neg) * self.mFRR_price_neg_avg * t_step / 3600

    # Method calculating the "Ausgleichsenergiepreis" (AEP)
    def aep_calc(self, t_now, t_step, t_isp):
        # Calculation of AEP1
        if self.aFRR_E_pos == 0 and self.aFRR_E_neg == 0 and self.mFRR_E_pos == 0 and self.mFRR_E_neg == 0:
            self.AEP = 0.0
        elif self.aFRR_E_pos + self.aFRR_E_neg + self.mFRR_E_pos + self.mFRR_E_neg == 0:
            self.AEP = 0.0
        else:
            FRR_costs = self.aFRR_costs_pos_period + self.aFRR_costs_neg_period \
                        + self.mFRR_costs_pos_period + self.mFRR_costs_neg_period
            FRR_energy = self.aFRR_E_pos_period + self.aFRR_E_neg_period \
                         + self.mFRR_E_pos_period + self.mFRR_E_neg_period
            if FRR_energy == 0.0:
                self.AEP = 0.0
            else:
                self.AEP = FRR_costs / FRR_energy

        # Calculation of AEP2
        # Limitation of the AEP to the highest absolute value in all activated aFRR and mFRR prices during an ISP
        if abs(self.aFRR_price_pos_max) > abs(self.aFRR_price_neg_max):
            AEP_max = abs(self.aFRR_price_pos_max)
        elif abs(self.aFRR_price_neg_max) > abs(self.aFRR_price_pos_max):
            AEP_max = abs(self.aFRR_price_neg_max)
        elif abs(self.aFRR_price_neg_max) == abs(self.aFRR_price_pos_max):
            AEP_max = abs(self.aFRR_price_pos_max)

        if AEP_max < abs(self.mFRR_price_neg_max):
            AEP_max = abs(self.mFRR_price_neg_max)
        elif AEP_max < abs(self.mFRR_price_pos_max):
            AEP_max = abs(self.mFRR_price_pos_max)

        # The variable self.AEP_max_period saves the highest value value of AEP_max during the ISP
        # self.AEP_max_period gets set to zero after each ISP
        if (t_now % t_isp) == 0:
            self.AEP_max_period = 0.0
        else:
            pass

        if self.AEP_max_period < AEP_max:
            self.AEP_max_period = AEP_max
        else:
            pass

        if self.AEP >= 0 and abs(self.AEP) > abs(self.AEP_max_period):
            self.AEP = self.AEP_max_period
        elif self.AEP <= 0 and abs(self.AEP) > abs(self.AEP_max_period):
            self.AEP = -self.AEP_max_period
        else:
            pass

    # Method processing the FRCE_cl of the Control Area to create a control signal (FRCE_sb) for Smart Balancing
    def sb_signal(self):
        # The currently activated SB power (self.sb_P) is added to the open loop FRCE (self.FRCE_ol) here...
        # ...to prevent a feedback loop for SB which can lead to oscillations
        self.sb_queue.append(self.FRCE_ol + self.sb_P)
        self.FRCE_sb = self.sb_queue.pop(0)

    # Method calculating the costs for consumed energy and the income of produced energy of the grid element.
    # The method sums up the costs and income of all subordinated balancing groups
    def energy_costs_calc(self, k_now, t_now, t_step, t_isp):
        self.gen_income = 0.0
        self.load_costs = 0.0
        self.gen_income_period = 0.0
        self.load_costs_period = 0.0
        for i in self.array_balancinggroups:
            i.energy_costs_calc(k_now=k_now,
                                t_now=t_now,
                                t_step=t_step,
                                t_isp=t_isp,
                                da_price=self.da_price)
            self.gen_income += i.gen_income
            self.load_costs += i.load_costs
            self.gen_income_period += i.gen_income_period
            self.load_costs_period += i.load_costs_period

    def readarray(self, k_now):
        for i in self.array_balancinggroups:
            i.readarray(k_now=k_now)

    # Method called after an MOL update to trigger further calculations
    def mol_update(self):
        self.aFRR_cap_pos = 0.0
        l = len(self.array_aFRR_molpos['Power'])
        i = 0
        while i < l:
            self.aFRR_cap_pos += self.array_aFRR_molpos['Power'][i]
            i += 1

        self.aFRR_cap_neg = 0.0
        l = len(self.array_aFRR_molneg['Power'])
        i = 0
        while i < l:
            self.aFRR_cap_neg += self.array_aFRR_molneg['Power'][i]
            i += 1

    # Method writing all current variables for frequency, load flow, FCR, aFRR, and Smart Balancing
    # by appending them to the respective arrays.
    # The method further calls the method of the same name in all subordinated Balancing Groups.
    def write_results(self):
        for i in self.array_balancinggroups:
            i.write_results()
        self.array_gen_P.append(self.gen_P)
        self.array_load_P.append(self.load_P)
        self.array_gen_P_schedule.append(self.gen_P_schedule)
        self.array_load_P_schedule.append(self.load_P_schedule)
        self.array_imba_P_ph.append(self.imba_P_ph)
        self.array_imba_P_sc.append(self.imba_P_sc)
        self.array_FCR_P.append(self.FCR_P)
        self.array_FRCE.append(self.FRCE)
        self.array_FRCE_ol.append(self.FRCE_ol)
        self.array_FRCE_ol_pos.append(self.FRCE_ol_pos)
        self.array_FRCE_ol_neg.append(self.FRCE_ol_neg)
        self.array_FRCE_cl_pos.append(self.FRCE_cl_pos)
        self.array_FRCE_cl_neg.append(self.FRCE_cl_neg)
        self.array_aFRR_ref.append(self.aFRR_ref)
        self.array_aFRR_ref_pos.append(self.aFRR_ref_pos)
        self.array_aFRR_ref_neg.append(self.aFRR_ref_neg)
        self.array_aFRR_P.append(self.aFRR_P)
        self.array_aFRR_P_pos.append(self.aFRR_P_pos)
        self.array_aFRR_P_neg.append(self.aFRR_P_neg)
        self.array_aFRR_price.append(self.aFRR_price)
        self.array_aFRR_price_pos.append(self.aFRR_price_pos)
        self.array_aFRR_price_neg.append(self.aFRR_price_neg)
        self.array_aFRR_price_avg.append(self.aFRR_price_avg)
        self.array_aFRR_price_pos_avg.append(self.aFRR_price_pos_avg)
        self.array_aFRR_price_neg_avg.append(self.aFRR_price_neg_avg)
        self.array_aFRR_price_pos_max.append(self.aFRR_price_pos_max)
        self.array_aFRR_price_neg_max.append(self.aFRR_price_neg_max)
        self.array_aFRR_costs.append(self.aFRR_costs)
        self.array_aFRR_costs_pos.append(self.aFRR_costs_pos)
        self.array_aFRR_costs_neg.append(self.aFRR_costs_neg)
        self.array_aFRR_costs_period.append(self.aFRR_costs_period)
        self.array_aFRR_costs_pos_period.append(self.aFRR_costs_pos_period)
        self.array_aFRR_costs_neg_period.append(self.aFRR_costs_neg_period)
        self.array_AEP.append(self.AEP)
        self.array_AEP_max_period.append(self.AEP_max_period)
        self.array_sb_P.append(self.sb_P)
        self.array_FRCE_sb.append(self.FRCE_sb)
        self.array_aFRR_E_pos.append(self.aFRR_E_pos)
        self.array_aFRR_E_neg.append(self.aFRR_E_neg)
        self.array_aFRR_E_pos_period.append(self.aFRR_E_pos_period)
        self.array_aFRR_E_neg_period.append(self.aFRR_E_neg_period)
        self.array_aFRR_cap_pos.append(self.aFRR_cap_pos)
        self.array_aFRR_cap_neg.append(self.aFRR_cap_neg)
        self.array_mFRR_P.append(self.mFRR_P)
        self.array_mFRR_P_pos.append(self.mFRR_P_pos)
        self.array_mFRR_P_neg.append(self.mFRR_P_neg)
        self.array_mFRR_E_pos.append(self.mFRR_E_pos)
        self.array_mFRR_E_neg.append(self.mFRR_E_neg)
        self.array_mFRR_E_pos_period.append(self.mFRR_E_pos_period)
        self.array_mFRR_E_neg_period.append(self.mFRR_E_neg_period)
        self.array_mFRR_price.append(self.mFRR_price)
        self.array_mFRR_price_pos.append(self.mFRR_price_pos)
        self.array_mFRR_price_neg.append(self.mFRR_price_neg)
        self.array_mFRR_price_avg.append(self.mFRR_price_avg)
        self.array_mFRR_price_pos_avg.append(self.mFRR_price_pos_avg)
        self.array_mFRR_price_neg_avg.append(self.mFRR_price_neg_avg)
        self.array_mFRR_price_pos_max.append(self.mFRR_price_pos_max)
        self.array_mFRR_price_neg_max.append(self.mFRR_price_neg_max)
        self.array_mFRR_costs.append(self.mFRR_costs)
        self.array_mFRR_costs_pos.append(self.mFRR_costs_pos)
        self.array_mFRR_costs_neg.append(self.mFRR_costs_neg)
        self.array_mFRR_costs_period.append(self.mFRR_costs_period)
        self.array_mFRR_costs_pos_period.append(self.mFRR_costs_pos_period)
        self.array_mFRR_costs_neg_period.append(self.mFRR_costs_neg_period)
        self.array_gen_income.append(self.gen_income)
        self.array_load_costs.append(self.load_costs)
        self.array_gen_income_period.append(self.gen_income_period)
        self.array_load_costs_period.append(self.load_costs_period)
