import matplotlib.pyplot as plt

def open_data_file():
    '''returns dictionary with time_tab as float tab ['time'], rr_tab
    (main score) as float tab ['rr'] and control_sum as int tab ['control_sum']'''
    time_tab = []
    rr_tab = []
    flag_tab = []
    file = open("RR.rea", 'r')

    for line in file.readlines():
        line = line.strip().split()
        if line[0] == '#time':
            continue
        time_tab.append(float(line[0]))
        rr_tab.append(float(line[1]))
        flag_tab.append(int(line[2])) #int or bool it's just a flag
    file.close()
    returning_value = {}
    returning_value["time"] = time_tab
    returning_value["rr"] = rr_tab
    returning_value["control_sum"] = flag_tab
    return returning_value

def count_average(dict_with_data):
    sum = 0.0
    for value in dict_with_data['rr']:
        sum += float(value)
    return sum / len(dict_with_data['rr'])

def find_max(dict_with_data):
    max = 0.0
    for value in dict_with_data['rr']:
        if float(value) > max:
            max = float(value)
    return max

def find_min(dict_with_data):
    min = find_max(dict_with_data)
    for value in dict_with_data['rr']:
        if float(value) < min:
            min = float(value)
    return min

def binning(time_lineup, RR_lineup, binning_interval):
    start_time = time_lineup[0]
    sum_RR = 0.0
    time_sum = 0.0
    h_m_samples = 0
    binning_effect = []
    for i in range(len(time_lineup)):
        sum_RR += RR_lineup[i]
        time_sum += time_lineup[i]
        h_m_samples += 1
        if time_lineup[i] >= start_time + binning_interval:
            binning_effect.append((float(time_sum / h_m_samples), float(sum_RR / h_m_samples)))
            h_m_samples = 0
            start_time = time_lineup[i + 1]
            time_sum = 0
            sum_RR = 0
    return binning_effect

def sma_algorithm(time_lineup, RR_lineup, sma_length = 3):
    score_after_sma = []
    h_m_samples = sma_length
    sum = 0.0
    flag = 0
    for i in range(len(time_lineup)):
        for j in range(sma_length):
            if i + j < len(time_lineup):
                sum += RR_lineup[i + j]
            else:
                h_m_samples -= 1
        if time_lineup[i] == time_lineup[0]:
            flag += 1
        if flag == 2:
            break
        score_after_sma.append((time_lineup[i], float(sum / h_m_samples)))
        h_m_samples = sma_length
        sum = 0.0
    return score_after_sma


def set_range(dict_with_data, min_minutes, max_minutes, binning_interval = 0.0, sma_length = 0):
    i = 0
    returning_value = {}
    time_lineup = []
    rr_lineup = []
    while float(dict_with_data['time'][i]) <= max_minutes:
        if float(dict_with_data['time'][i]) >= min_minutes and float(dict_with_data['time'][i]) <= max_minutes:
            time_lineup.append(float(dict_with_data['time'][i]))
            rr_lineup.append(float(dict_with_data['rr'][i]))
        i += 1
    if binning_interval > 0.0:
        returning_value['bin_value_range'] = binning(time_lineup, rr_lineup, binning_interval)
    if sma_length > 0:
        returning_value['sma_val_range'] = sma_algorithm(time_lineup, rr_lineup, sma_length)
    returning_value['time_lineup'] = time_lineup
    returning_value['rr_lineup'] = rr_lineup
    return returning_value

def get_data_from_user(dict_with_data):
    returning_value = {}
    minimal_value = float(input("Give minimal time value (in minutes)... "))
    maximal_value = float(input("Give max time value (in minutes)... "))
    bin_val = float(input("Give binning interval... "))
    sma = int(input("Give length of sma... "))
    maximum_tab_value = find_max(dict_with_data)
    if maximal_value == -1 or maximal_value > maximum_tab_value:
        maximal_value = maximum_tab_value
    returning_value['min_v'] = minimal_value
    returning_value['max_v'] = maximal_value
    returning_value['bin_v'] = bin_val
    returning_value['sma'] = sma
    return returning_value

def plotting(time_lineup, rr_lineup):
    plt.plot(time_lineup, rr_lineup)
    plt.show()

def start():
    file_data = open_data_file()
    user_input = get_data_from_user(file_data)
    range_to_count = set_range(file_data, user_input['min_v'], user_input['max_v'], user_input['bin_v'], user_input['sma'])
    print(count_average(file_data))
    print(find_max(file_data))
    print(find_min(file_data))
    plotting(range_to_count['time_lineup'], range_to_count['rr_lineup']) #first default (without binning or sma)

start()
'''
plt.plot(time_lineup, RR_lineup)
plt.show()


time_next = []
RR_next = []

for i in range(len(next_show[0])):
    time_next.append(next_show[0][i][0])
    RR_next.append(next_show[0][i][1])

plt.plot(time_next, RR_next)
plt.show()
RR_next = []
time_next = []

for i in range(len(next_show[1])):
    time_next.append(next_show[1][i][0])
    RR_next.append(next_show[1][i][1])

plt.plot(time_next, RR_next)
plt.show()
'''
