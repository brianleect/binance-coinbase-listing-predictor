def durationToSeconds(str_dur):
    unit = str_dur[-1]
    if unit == 's': unit = 1
    elif unit == 'm': unit = 60
    elif unit == 'h': unit = 3600
    elif unit == 'd': unit = 3600*24

    return  int(str_dur[:-1]) * unit