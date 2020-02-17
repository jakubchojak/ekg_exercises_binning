import matplotlib.pyplot as plt

def analyze():
    val = []
    t = []
    RR = []
    V = []
    i = 0
    end_score = []
    num_of_samples = 0
    file = open("RR.rea", 'r')
    while True:
        val.append(file.readline())
        if val[i] == '':
            break
        num_of_samples += 1
        i += 1
        
    file.close()

    for j in range(1, i):
        x = 0
        ch = '0'
        t.append('')
        RR.append('')
        V.append('')
        while ord(ch) >= ord('0') and ord(ch) <= ord('9') or ch == '.':
            ch = val[j][x]
            t[j - 1] += ch
            x += 1

        while not(ord(ch) >= ord('0') and ord(ch) <= ord('9') or ch == '.'):
            ch = val[j][x]
            x += 1
        x -= 1
        while ord(ch) >= ord('0') and ord(ch) <= ord('9') or ch == '.':
            ch = val[j][x]
            RR[j - 1] += ch
            x += 1

        while not(ord(ch) >= ord('0') and ord(ch) <= ord('9') or ch == '.'):
            ch = val[j][x]
            x += 1
        x -= 1
        while ord(ch) >= ord('0') and ord(ch) <= ord('9') or ch == '.':
            ch = val[j][x]
            V[j - 1] += ch
            x += 1

        if V[j - 1] == '0\n':
            end_score.append((t[j - 1].strip(), RR[j - 1].strip()))

        returning_value = []
        returning_value.append(end_score)
        returning_value.append(t)
        returning_value.append(RR)
    return returning_value

def count_average(our_tuple):
    sum = 0.0
    for x in range(len(our_tuple)):
        sum += float(our_tuple[x][1])
    return sum / len(our_tuple)

def find_max(our_tuple):
    max = 0.0
    for x in range(len(our_tuple)):
        if float(our_tuple[x][1]) > max:
            max = float(our_tuple[x][1])
    return max

def find_min(our_tuple):
    min = find_max(our_tuple)
    for x in range(len(our_tuple)):
        if float(our_tuple[x][1]) < min:
            min = float(our_tuple[x][1])
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
        print(time_lineup[i])
        print("\t" + str(float(sum / h_m_samples)))
        h_m_samples = sma_length
        sum = 0.0
    return score_after_sma


def set_range(tup_gen, min_minutes, max_minutes, time_lineup, RR_lineup, binning_interval = 0.0, sma_length = 0):
    i = 0
    returning_value = []
    while float(tup_gen[1][i]) <= max_minutes:
        if float(tup_gen[1][i]) >= min_minutes and float(tup_gen[1][i]) <= max_minutes:
            time_lineup.append(float(tup_gen[1][i]))
            RR_lineup.append(float(tup_gen[2][i]))
        i += 1
    if binning_interval > 0.0:
        returning_value.append(binning(time_lineup, RR_lineup, binning_interval))
    if sma_length > 0:
        returning_value.append(sma_algorithm(time_lineup, RR_lineup, sma_length))
    return returning_value

def get_data_from_user(tuple_with_end):
    returning_value = []
    minimal_value = float(input("Give minimal time value (in minutes)... "))
    maximal_value = float(input("Give max time value (in minutes)... "))
    bin_val = float(input("Give binning interval... "))
    sma = int(input("Give length of sma... "))
    if maximal_value == -1:
        maximal_value = find_max(tuple_with_end)
    returning_value.append(minimal_value)
    returning_value.append(maximal_value)
    returning_value.append(bin_val)
    returning_value.append(sma)
    return returning_value

tup_gen = analyze()
tuple_with_end_score = tup_gen[0]
time_lineup = []
RR_lineup = []

data = get_data_from_user(tuple_with_end_score)
min_v = data[0]
max_v = data[1]
bin_interval = data[2]
sma_length = data[3]

set_range(tup_gen, min_v, max_v, time_lineup, RR_lineup)

print(count_average(tuple_with_end_score))
print(find_max(tuple_with_end_score))
print(find_min(tuple_with_end_score))

plt.plot(time_lineup, RR_lineup)
plt.show()


next_show = set_range(tup_gen, min_v, max_v, time_lineup, RR_lineup, bin_interval, sma_length)

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
