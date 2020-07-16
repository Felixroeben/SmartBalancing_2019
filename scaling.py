from builtins import range


# scale to seconds with the rmap-area method
def scale_to_seconds(value_15_min, ramp):

    power_schedule_sec = []
    f = 900  # sec. (15min.)
    h_null = value_15_min[0]        # anfangswert der Viertelstunde des Vortages

    for i in range(len(value_15_min)):

        # to not run out of index length
        if (i + 1) == len(value_15_min):
            break

        b = value_15_min[i+1] - h_null  # Höhe des Dreiecks
        # ist die Höhe pos/neg
        if b < 0:
            mul = -1
        else:
            mul = 1

        c = b / ramp  # länge des Dreiecks
        A_dreieck = (b * c) / 2  # Fläche des Dreiecks
        d = f - c
        h = (3 * A_dreieck * mul) / d  # Höhe des trapezes

        # Aggregation auf Sekundenwerte
        for j in range(900):
            step = j * ramp * mul

            if b < 0:
                if (h_null + step) > (h + value_15_min[i+1]):
                    power_schedule_sec.append((h_null + step))# / 900)
                else:
                    power_schedule_sec.append((value_15_min[i+1] + h))# / 900)
            else:
                if (h_null + step) < (h + value_15_min[i+1]):
                    power_schedule_sec.append((h_null + step))# / 900)
                else:
                    power_schedule_sec.append((value_15_min[i+1] + h))# / 900)

        # neuen Startwert setzen
        h_null = h + value_15_min[i+1]
        step = 0.0
    #print('List 1:', len(power_schedule_sec), ' 1. Element:', power_schedule_sec[0])
    return power_schedule_sec


# scale the intern 900sec values back to 15min values for the output data
def scale_to_minutes(value_900_sec):

    value_15_min = []
    buffer = 0.0
    n = len(value_900_sec)
    for i in range(n):
        buffer = buffer + value_900_sec[i]
        if (i % 900 == 0) & (i > 0):
            value_15_min.append(buffer/float(900))
            buffer = 0.0

    return value_15_min
