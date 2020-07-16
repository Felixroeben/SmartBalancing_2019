import csv
import balagrou
import smarbala
import loadload
import generato
import scaling
import pandas as pd


def readarray(filename, arrayname):
    array = []

    with open(filename, mode='r') as csv_file:
        file = csv.DictReader(csv_file, delimiter=';')

        for row in file:
            array.append(float(row[arrayname]))

    return array


# fill the schedule arrays of the BGs with (second) values
def fill_schedule(scenario, balancing_groups, sim_duration):

    count = 0
    # ------getting the power schedule------- #
    gen_schedule = scenario + 'Erzeugung_Soll.csv'
    csv_gen_schedule = open(gen_schedule, mode='r')
    file_gen = csv.DictReader(csv_gen_schedule, delimiter=';')

    for i in range(len(balancing_groups)):
        for row in file_gen:
            if count == sim_duration:
                count = 0
                break
            else:
                count += 1
                balancing_groups[i].array_gen_P_schedule.append(float(row[balancing_groups[i].name]))
        # reset File pointer and skip Header row
        csv_gen_schedule.seek(0)
        csv_gen_schedule.__next__()


    # ------getting the load schedule------- #
    load_schedule = scenario + 'Verbrauch_Soll.csv'
    csv_load_schedule = open(load_schedule, mode='r')
    file_load = csv.DictReader(csv_load_schedule, delimiter=';')
    count = 0

    for i in range(len(balancing_groups)):
        for row in file_load:
            if count == sim_duration:
                count = 0
                break
            else:
                count += 1
                # print(balancing_groups[i].name, row)
                balancing_groups[i].array_load_P_schedule.append(float(row[balancing_groups[i].name]))
        # reset File pointer and skip Header row
        csv_load_schedule.seek(0)
        csv_load_schedule.__next__()

    print('Schedules initialized')


# a CSV with all power and load will be automatically read and the objects created and appended to their belonging BG
def fill_power_load(scenario, balancing_groups, sim_duration):
    # ------getting the power values------- #
    kw_gen_file = scenario + 'Erzeugung_Ist.csv'
    csv_file1 = open(kw_gen_file, mode='r')
    file1 = csv.DictReader(csv_file1, delimiter=';')
    i = 0
    count = 0

    # search through the BG array
    for i in range(len(balancing_groups)):
        # search through the power plant array
        for j in range(len(balancing_groups[i].array_generators)):
            for row1 in file1:
                if count == sim_duration:
                    count = 0
                    break
                else:
                    count += 1
                    balancing_groups[i].array_generators[j].array_gen_P.append(float(row1[balancing_groups[i].array_generators[j].name]))

                # reset File pointer and skip Header row
            csv_file1.seek(0)
            csv_file1.__next__()

    # ------getting the load values------- #
    kw_load_file = scenario + 'Verbrauch_Ist.csv'
    csv_file2 = open(kw_load_file, mode='r')
    file2 = csv.DictReader(csv_file2, delimiter=';')
    # search through the BG array
    for i in range(len(balancing_groups)):
        # search through the load array
        for j in range(len(balancing_groups[i].array_loads)):
            for row2 in file2:
                if count == sim_duration:
                    count = 0
                    break
                else:
                    count += 1
                    balancing_groups[i].array_loads[j].array_load_P.append(float(row2[balancing_groups[i].array_loads[j].name]))

            # reset File pointer and skip Header row
            csv_file2.seek(0)
            csv_file2.__next__()

    print('Power/Loads initialized')


# a CSV with all BGs will be automatically read and the objects created
def get_balancing_groups(scenario, sb_ON, sim_duration):

    obj_balancing_groups = []    # Array with BalancingGroup Objects
    bg_file = scenario + 'bilanzkreise.csv'

    # open CSV
    csv_bgs = open(bg_file, mode='r')
    file = csv.DictReader(csv_bgs, delimiter=';')

    # Einlesen der Zeilen der Datei, je nach dem Namen der Spalte zugeordnet
    # es wird davon ausgegangen, dass jeder BG mind. einen Load und Power besitzt!!!!
    for count, row in enumerate(file):
        if sb_ON:
            if row['smart'] == 'True':
                obj_balancing_groups.append(balagrou.BalancingGroup(name=row['Bilanzkreis'],
                                                                    read=True,
                                                                    smart=True))
            elif row['smart'] == 'False':
                obj_balancing_groups.append(balagrou.BalancingGroup(name=row['Bilanzkreis'],
                                                                    read=True,
                                                                    smart=False))
            else:
                print('Could not determine, if', row['Bilanzkreis'], 'is smart. "self.smart" set to "False"')

        elif not sb_ON:
            obj_balancing_groups.append(balagrou.BalancingGroup(name=row['Bilanzkreis'],
                                                               read=True,
                                                               smart=False))

        if row['Verbraucher'] != '-':
            array_verbraucher = str(row['Verbraucher'])
            # check, if there is more then one consumer in the row, separated by ","
            if array_verbraucher.find(',') == -1:   # no separator in the row
                obj_balancing_groups[count].array_loads.append(loadload.Load(name=row['Verbraucher'],
                                                                            read=True,
                                                                            load_P=0.0))
            else:   # separator "," in the row
                verbraucher_liste = array_verbraucher.split(',')    # separate the row by "," and loop through list
                for counter in range(len(verbraucher_liste)):
                    obj_balancing_groups[count].array_loads.append(loadload.Load(name=str(verbraucher_liste[counter]),
                                                                                read=True,
                                                                                load_P=0.0))

        if row['Flex Verbraucher'] != '-':
             array_verbraucher = str(row['Flex Verbraucher'])
             # check, if there is more then one consumer in the row, separated by ","
             if array_verbraucher.find(',') == -1:  # no separator in the row
                 obj_balancing_groups[count].array_loads.append(loadload.LoadFlex(name=row['Flex Verbraucher'],
                                                                                 read=True,
                                                                                 load_P=0.0,
                                                                                 sb_rate_pos=0.0,
                                                                                 sb_rate_neg=0.0,
                                                                                 sb_P_max=0.0,
                                                                                 sb_P_min=0.0,
                                                                                 sb_costs=0.0,
                                                                                 bg_name=obj_balancing_groups[count].name))
             else:   # separator "," in the row
                 verbraucher_liste = array_verbraucher.split(',')  # separate the row by "," and loop through list
                 for counter in range(len(verbraucher_liste)):
                     obj_balancing_groups[count].array_loads.append(loadload.LoadFlex(name=str(verbraucher_liste[counter]),
                                                                                     read=True,
                                                                                     load_P=0.0,
                                                                                     sb_rate_pos=0.0,
                                                                                     sb_rate_neg=0.0,
                                                                                     sb_P_max=0.0,
                                                                                     sb_P_min=0.0,
                                                                                     sb_costs=0.0,
                                                                                     bg_name=obj_balancing_groups[count].name))

        if row['Erzeuger'] != '-':
            array_erzeuger = str(row['Erzeuger'])
            # check, if there is more then one generator in the row, separated by ","
            if array_erzeuger.find(',') == -1:  # no separator in the row
                obj_balancing_groups[count].array_generators.append(generato.Generator(name=row['Erzeuger'],
                                                                                        read=True,
                                                                                        gen_P=0.0))
            else:   # separator "," in the row
                erzeuger_liste = array_erzeuger.split(',')  # separate the row by "," and loop through list
                for counter in range(len(erzeuger_liste)):
                    obj_balancing_groups[count].array_generators.append(generato.Generator(name=str(erzeuger_liste[counter]),
                                                                                           read=True,
                                                                                           gen_P=0.0))

        if row['Flex Erzeuger'] != '-':
            array_erzeuger = str(row['Flex Erzeuger'])
            # check, if there is more then one generator in the row, separated by ","
            if array_erzeuger.find(',') == -1:  # no separator in the row
                obj_balancing_groups[count].array_generators.append(generato.GeneratorFlex(name=row['Flex Erzeuger'],
                                                                                           read=True,
                                                                                           gen_P=0.0,
                                                                                           sb_rate_pos=0.0,
                                                                                           sb_rate_neg=0.0,
                                                                                           sb_P_max=0.0,
                                                                                           sb_P_min=0.0,
                                                                                           sb_costs=0.0,
                                                                                           bg_name=obj_balancing_groups[count].name))
            else:   # separator "," in the row
                erzeuger_liste = array_erzeuger.split(',')  # separate the row by "," and loop through list
                for counter in range(len(erzeuger_liste)):
                    obj_balancing_groups[count].array_generators.append(generato.GeneratorFlex(name=str(erzeuger_liste[counter]),
                                                                                               read=True,
                                                                                               gen_P=0.0,
                                                                                               sb_rate_pos=0.0,
                                                                                               sb_rate_neg=0.0,
                                                                                               sb_P_max=0.0,
                                                                                               sb_P_min=0.0,
                                                                                               sb_costs=0.0,
                                                                                               bg_name=obj_balancing_groups[count].name))

    print('Balancing Groups initialized')
    # fill the load and power schedule for every BG that has been created
    fill_schedule(scenario, obj_balancing_groups, sim_duration)
    fill_power_load(scenario, obj_balancing_groups, sim_duration)

    return obj_balancing_groups


# Function reads all smart balancing assets (class 'SmartBalancingAsset') from a .csv
# creates 'SmartBalancingAsset' objects and returns a list of these objects
def get_assets(scenario):
    obj_assets = []
    asset_file = scenario + 'Assets.csv'
    csv_assets = open(asset_file, mode='r')
    file = csv.DictReader(csv_assets, delimiter=';')

    for row in file:
        if row['class'] == "SmartBalancingAsset":
            obj_assets.append(smarbala.SmartBalancingAsset(row['Asset'],
                                                           float(row['sb_rate_pos']),
                                                           float(row['sb_rate_neg']),
                                                           float(row['sb_P_min']),
                                                           float(row['sb_P_max']),
                                                           float(row['sb_costs']),
                                                           row['bg_name']))
        else:
            pass
    return obj_assets

# Function reads all flexible loads (class 'LoadFlex') from a .csv
# and assigns their smart balancing parameters to the already existing 'LoadFlex'-objects of the control area
# 'LoadFlex'-objects need to be created first
def get_load_flex(scenario, control_area):
    load_flex_file = scenario + 'Assets.csv'
    csv_assets = open(load_flex_file, mode='r')
    file = csv.DictReader(csv_assets, delimiter=';')

    for row in file:
        if row['class'] == "LoadFlex":
            load_flex ={'Asset':         row['Asset'],
                        'sb_rate_pos':   row['sb_rate_pos'],
                        'sb_rate_neg':   row['sb_rate_neg'],
                        'sb_P_min':      row['sb_P_min'],
                        'sb_P_max':      row['sb_P_max'],
                        'sb_costs':      row['sb_costs'],
                        'bg_name':       row['bg_name']}

            for bg in control_area.array_balancinggroups:
                for load in bg.array_loads:
                    if load.name == load_flex['Asset'] and bg.name == load_flex['bg_name']:
                        load.sb_rate_pos = float(load_flex['sb_rate_pos'])
                        load.sb_rate_neg = float(load_flex['sb_rate_neg'])
                        load.sb_P_min = float(load_flex['sb_P_min'])
                        load.sb_P_max = float(load_flex['sb_P_max'])
                        load.sb_costs = float(load_flex['sb_costs'])
                        bg.array_sb_assets.append(load)


# Function reads all flexible generators (class 'GeneratorFlex') from a .csv
# and assigns their smart balancing parameters to the already existing 'GeneratorFlex' objects of the control area
# 'GeneratorFlex' objects need to be created first
def get_gen_flex(scenario, control_area):
    gen_flex_file = scenario + 'Assets.csv'
    csv_assets = open(gen_flex_file, mode='r')
    file = csv.DictReader(csv_assets, delimiter=';')

    for row in file:
        if row['class'] == "GeneratorFlex":
            gen_flex ={'Asset':         row['Asset'],
                       'sb_rate_pos':   row['sb_rate_pos'],
                       'sb_rate_neg':   row['sb_rate_neg'],
                       'sb_P_min':      row['sb_P_min'],
                       'sb_P_max':      row['sb_P_max'],
                       'sb_costs':      row['sb_costs'],
                       'bg_name':       row['bg_name']}

            for bg in control_area.array_balancinggroups:
                for gen in bg.array_generators:
                    if gen.name == gen_flex['Asset'] and bg.name == gen_flex['bg_name']:
                        gen.sb_rate_pos = float(gen_flex['sb_rate_pos'])
                        gen.sb_rate_neg = float(gen_flex['sb_rate_neg'])
                        gen.sb_P_min = float(gen_flex['sb_P_min'])
                        gen.sb_P_max = float(gen_flex['sb_P_max'])
                        gen.sb_costs = float(gen_flex['sb_costs'])
                        bg.array_sb_assets.append(gen)

def read_afrr_mol(scenario, t_day, t_mol, day_count):
    # dicts for pos and neg MOL
    molpos_buffer = {'Power': [],
                     'Price': []}
    molneg_buffer = {'Power': [],
                     'Price': []}
    list_nbr = day_count
    hour_tag = '_xx_yy'             # 4 hour block tag
    mol_file = scenario + 'mol_'

    if day_count > 0:
        if t_day < 14400:
            hour_tag = '_00_04'
        elif 14400 <= t_day < 28800:
            hour_tag = '_04_08'
        elif 28800 <= t_day < 43200:
            hour_tag = '_08_12'
        elif 43200 <= t_day < 57600:
            hour_tag = '_12_16'
        elif 57600 <= t_day < 72000:
            hour_tag = '_16_20'
        elif 72000 <= t_day < 86400:
            hour_tag = '_20_24'
    else:
        list_nbr = 0
        hour_tag = '_20_24'

    # create the hour block string
    neg_str = 'NEG' + hour_tag
    pos_str = 'POS' + hour_tag

    # creating the name of the CSV for the day 29.10. = 1, 30.10. = 2
    day_list = mol_file + str(list_nbr) + '.csv'

    csv_handle = open(day_list, mode='r')
    file = csv.DictReader(csv_handle, delimiter=';')

    for row in file:
        if row['ENERGY_PRICE_PAYMENT_DIRECTION'] == 'PROVIDER_TO_GRID':
            pos_prefix = -1.0
            neg_prefix = -1.0
        else:
            pos_prefix = 1.0
            neg_prefix = 1.0

        if row['PRODUCT'] == neg_str:
            molneg_buffer['Price'].append(float(row['ENERGY_PRICE_[EUR/MWh]']) * neg_prefix)
            molneg_buffer['Power'].append(float(row['ALLOCATED_CAPACITY_[MW]']) * (-1))
        elif row['PRODUCT'] == pos_str:
            molpos_buffer['Price'].append(float(row['ENERGY_PRICE_[EUR/MWh]']) * pos_prefix)
            molpos_buffer['Power'].append(float(row['ALLOCATED_CAPACITY_[MW]']))
        else:
            pass

    csv_handle.close()
    # sort the mol-arrays in order of the price (price to capacity belongs together)
    bubble_sort(molpos_buffer)
    bubble_sort(molneg_buffer)

    return molpos_buffer, molneg_buffer

def read_mfrr_mol(scenario, t_day, t_mol, day_count):
    # dicts for pos and neg MOL
    molpos_buffer = {'Power': [],
                     'Price': []}
    molneg_buffer = {'Power': [],
                     'Price': []}
    list_nbr = day_count
    hour_tag = '_xx_yy'             # 4 hour block tag
    mol_file = scenario + 'mfrr_mol_'

    if day_count > 0:
        if t_day < 14400:
            hour_tag = '_00_04'
        elif 14400 <= t_day < 28800:
            hour_tag = '_04_08'
        elif 28800 <= t_day < 43200:
            hour_tag = '_08_12'
        elif 43200 <= t_day < 57600:
            hour_tag = '_12_16'
        elif 57600 <= t_day < 72000:
            hour_tag = '_16_20'
        elif 72000 <= t_day < 86400:
            hour_tag = '_20_24'
    else:
        list_nbr = 0
        hour_tag = '_20_24'

    # create the hour block string
    neg_str = 'NEG' + hour_tag
    pos_str = 'POS' + hour_tag

    # creating the name of the CSV for the day 29.10. = 1, 30.10. = 2
    day_list = mol_file + str(list_nbr) + '.csv'

    csv_handle = open(day_list, mode='r')
    file = csv.DictReader(csv_handle, delimiter=';')

    for row in file:
        if row['ENERGY_PRICE_PAYMENT_DIRECTION'] == 'PROVIDER_TO_GRID':
            pos_prefix = -1.0
            neg_prefix = -1.0
        else:
            pos_prefix = 1.0
            neg_prefix = 1.0

        if row['PRODUCT'] == neg_str:
            molneg_buffer['Price'].append(float(row['ENERGY_PRICE_[EUR/MWh]']) * neg_prefix)
            molneg_buffer['Power'].append(float(row['ALLOCATED_CAPACITY_[MW]']) * (-1))
        elif row['PRODUCT'] == pos_str:
            molpos_buffer['Price'].append(float(row['ENERGY_PRICE_[EUR/MWh]']) * pos_prefix)
            molpos_buffer['Power'].append(float(row['ALLOCATED_CAPACITY_[MW]']))
        else:
            pass

    csv_handle.close()
    # sort the mol-arrays in order of the price (price to capacity belongs together)
    bubble_sort(molpos_buffer)
    bubble_sort(molneg_buffer)

    return molpos_buffer, molneg_buffer

def bubble_sort(mol_buffer):
    n = len(mol_buffer['Price'])

    # Traverse through all array elements
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n - i - 1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if mol_buffer['Price'][j] > mol_buffer['Price'][j + 1]:
                mol_buffer['Price'][j], mol_buffer['Price'][j + 1] = mol_buffer['Price'][j + 1], mol_buffer['Price'][j]
                mol_buffer['Power'][j], mol_buffer['Power'][j + 1] = mol_buffer['Power'][j + 1], mol_buffer['Power'][j]


# saving all relevant data to a csv file
def save_data_to_csv(scenario, savefilename, save_dict):

    error = 0
    array_test = ['']
    array_test2 = []
    array_buff = []
    header = ''
    max_len = 0
    save_file = scenario + savefilename

    for i, value in enumerate(save_dict):
        if len(save_dict[value]) % 900 == 0:
            save_dict[value] = scaling.scale_to_minutes(save_dict[value])
        else:
            print('Warning! Size of Array "', value, '" ist not aliquot by 900 (%.0f).' % (len(save_dict[value])))
            error = error + 1
            if error == len(save_dict):
                return -1

    for count, value in enumerate(save_dict):
        header = header + str(value) + ';'      # Überschriften der Spalten einsammeln
        array_test2.append(array_buff)
        array_test2[count] = save_dict[value]   # array aus Dict speichern
        max_len_new = len(save_dict[value])     # länge des arrays prüfen und längstes Speichern
        if max_len_new > max_len:
            max_len = max_len_new

    for i in range(max_len):                    # Buffer auf länge des längsten arrays bringen
        array_test.append('')

    for list2 in array_test2:
        for i in range(max_len):
            if i < len(list2):
                # mit 3 nachkommastellen speichern!!
                array_test[i] = array_test[i] + ('%.3f' % list2[i]) + ' ;'
            else:
                array_test[i] = array_test[i] + ' ;' + ' ;'     # kurze arrays mit leeren Feldern füllen, um Wertverschiebung zu vermeiden

    # write Data to output CSV file
    with open(save_file, "w") as outfile:
        outfile.write(header)
        outfile.write("\n")
        for string in array_test:
            outfile.write(string)
            outfile.write("\n")

    # Macht aus den Punkten von Python-Float Kommata, damit die CSV in Excel richtig geöffnet wird
    in_file = open(save_file, 'r')
    data = in_file.read()
    in_file.close()
    for character in ".":
        data = data.replace(character, ',')

    out_file = open(save_file, 'w')
    out_file.write(data)
    out_file.close()

# Function to save simulation results of every ISP
# All arrays, that are passed to this function, get reduced to the last value of the period
# All last values of all periods of all arrays are then saved as a .csv-file
def save_period_data(scenario, save_file_name, save_dict, t_step, t_isp, t_stop):

    # Dictionary, that is the same as save_dict with the exception...
    # ...that it does not have one value for every t_step, but only one per ISP
    save_dict_t_isp = {}

    # Variable saving all column heads as a comma-separated string
    heads = str()

    # Variable saving all values of a row of save_dict_t_isp as a comma-separated string
    values = str()

    # Array saving every row of save_dict_t_isp as a comma-separated string
    array_values = []

    save_file = scenario + save_file_name

    # For every item in save_dict, the last value of each ISP is saved in an item of save_dict_t_isp
    for i in save_dict:
        head = i
        array_t_step = save_dict[i]
        array_t_isp = []
        t = t_isp
        k_price = int(int(t_isp) / int(t_step))
        j = 1

        while t <= t_stop:
            value = array_t_step[j * k_price - 1]
            array_t_isp.append(value)
            t += t_isp
            j += 1

        heads = heads + head + ';'
        save_dict_t_isp[head] = array_t_isp
        if array_values == []:
            for k in array_t_isp:
                array_values.append(str(k))
        else:
            rows = len(array_t_isp)
            row = 0
            while row < rows:
                values = array_values[row]
                values = values + ';' + str(array_t_isp[row])
                array_values[row] = values
                row += 1

    # Data is saved in a .csv-file using the string "heads" and the array of strings "array_values"
    with open(save_file, "w") as outfile:
        outfile.write(heads)
        for l in array_values:
            outfile.write("\n")
            outfile.write(l)

# Function to save simulation results of every t_step
# All arrays, that are passed to this function get saved as a .csv-file
def save_t_step_data(scenario, save_file_name, save_dict, t_step, t_isp, t_stop):

    # Dictionary, that is the same as save_dict with the exception...
    # ...that it does not have one value for every t_step, but only one per ISP
    save_dict_t_isp = {}

    # Variable saving all column heads as a comma-separated string
    heads = str()

    # Variable saving all values of a row of save_dict_t_isp as a comma-separated string
    values = str()

    # Array saving every row of save_dict_t_isp as a comma-separated string
    array_values = []

    save_file = scenario + save_file_name

    for i in save_dict:
        head = i
        array_t_step = save_dict[i]
        j = 1

        heads = heads + head + ';'
        save_dict_t_isp[head] = array_t_step
        if array_values == []:
            for k in array_t_step:
                array_values.append(str(k))
        else:
            rows = len(array_t_step)
            row = 0
            while row < rows:
                values = array_values[row]
                values = values + ';' + str(array_t_step[row])
                array_values[row] = values
                row += 1

    # Data is saved in a .csv-file using the string "heads" and the array of strings "array_values"
    with open(save_file, "w") as outfile:
        outfile.write(heads)
        for l in array_values:
            outfile.write("\n")
            outfile.write(l)

def get_da_price_data(sim_duration_uct):
    prices = pd.read_csv('Price_Data/Day-ahead Prices_2019.csv', sep=',')
    prices = prices.set_index('MTU (CET)')
    prices_scenario = prices[sim_duration_uct[0]+ ' 00:00 - ' + sim_duration_uct[0] + ' 01:00' : sim_duration_uct[1]+ ' 23:00 - ' + sim_duration_uct[2] + ' 00:00' ]
    return prices_scenario

