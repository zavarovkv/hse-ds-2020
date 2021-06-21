import bisect
import random
import numpy


def normalize(series):
    series_min = 10000000000
    series_max = -10000000000
    for i in range(len(series)):
        if series[i] != 'NaN':
            if series[i] < series_min:
                series_min = series[i]
            if series[i] > series_max:
                series_max = series[i]
    for i in range(len(series)):
        if series[i] != 'NaN':
            series[i] = 2.0 * (series[i] - (series_min + series_max) / 2) / (series_max - series_min)
    return series, [series_min, series_max]


def unnormalize(series, recovering_values):
    for i in range(len(series)):
        series[i] = ((recovering_values[0] + recovering_values[1]) + series[i] * (recovering_values[1] - recovering_values[0])) / 2.0
    return series
    

MaxArcCount = 2  # 16;
ChainLength = 2
IterCountForBuild = 1000000  # 6000000 10000000 15000000;
StartPhero = 0.1
AntPhero = 0.1
AntiPhero = 0.005
AntStepCount = 3

IntervalCount = 40
IntervalStep = 0.1

SinusStartPoint = 0.0
SinusStep = 0.1  # Math.PI / 12.0; == 0.26
SinusNoise = 0.001
SinusElemCount = 24000

Y = 0.8
X = -1.0
Z = 0.2
LorentzElemCount = 50000
DELTA = 10.0
B = 8.0 / 3.0
R = 28
STEP = 0.1

InterCountForRebuild = 10
ChainCountForReBuild = 15


def get_intervals(interval_number=IntervalCount):
    v = -1
    intervals = [0] * (interval_number - 1)
    for i in range(interval_number - 1):
        v += 2 / interval_number
        intervals[i] = v
    return intervals


def get_intervals_1(series, interval_number=IntervalCount):
    v = 0
    sor = sorted(series)
    #print(sor[:100], sor[-100:])
    intervals = [0] * (interval_number - 1)
    for i in range(interval_number - 1):
        v += round(1 / interval_number * len(series))
        #print(v, 1)
        intervals[i] = sor[v - 1]
    #print(intervals)
    return intervals


def interval_choose(value, intervals):
    return bisect.bisect_left(intervals, value)


def generate_relation_tensor(series, max_step=MaxArcCount, vector_len=ChainLength, interval_number=IntervalCount, max_step_number=100000, initial_pheromone=1, pheromone_transition_number=ChainLength, additional_pheromone=1, max_transition_number=25): # для многомерности добавить dimensions
    series, recovering_values = normalize(series)
    sequences_ = sequence_generator(vector_len, max_step)
    intervals = get_intervals_1(series, interval_number)
    #intervals = get_intervals(interval_number)
    interval_counts = [0] * interval_number
    interval_sum = [0] * interval_number
    average_interval_values = [0.0] * interval_number
    for element in series:
        if element != 'NaN':
            interval_counts[interval_choose(element, intervals)] += 1
            interval_sum[interval_choose(element, intervals)] += element
    for i in range(interval_number):
        average_interval_values[i] = interval_sum[i] / interval_counts[i]
    series = [interval_choose(value, intervals) if value != 'NaN' else value for value in series]
    relation_tensor = {}
    current_pheromone_level = initial_pheromone
    step_counter = 0

    while step_counter < max_step_number:
        if not step_counter % 10000:
            print(step_counter // 10000, '% done', sep='')
        step_counter += 1
        start_position = random.randrange(len(series) - vector_len * max_step)
        while series[start_position] == 'NaN':
            start_position = random.randrange(len(series) - vector_len * max_step)
        current_sequence = select_start_sequence(series, start_position, relation_tensor, current_pheromone_level, sequences_)
        if current_sequence == -1:
            continue
        current_position = start_position + sum(current_sequence[1])
        transition_counter = vector_len
        while current_position + max_step < len(series) and transition_counter < max_transition_number:
            transition_counter += 1

            current_step = select_next_step(series, current_position, current_sequence, relation_tensor, current_pheromone_level, max_step)
            if current_step == -1:
                break
            current_position = current_position + current_step
            current_sequence[0] = current_sequence[0][1:] + [series[current_position]]
            current_sequence[1] = current_sequence[1][1:] + [current_step]
            if not transition_counter % pheromone_transition_number:
                if str(current_sequence) not in relation_tensor.keys():
                    relation_tensor[str(current_sequence)] = current_pheromone_level
                relation_tensor[str(current_sequence)] += additional_pheromone
    for i in relation_tensor.keys():
        relation_tensor[i] -= initial_pheromone
    return relation_tensor, average_interval_values, recovering_values, intervals


def sequence_generator(length, max_step):
    sequences = {}
    step_sequence = [1] * length
    step_sequence[0] = 0
    flag = 1
    counter = 0
    while flag:
        flag = 0
        for i in range(length):
            if step_sequence[i] != max_step:
                flag = 1
                step_sequence[i] += 1
                for j in range(i):
                    step_sequence[j] = 1
                sequences[counter] = ' '.join(map(str, step_sequence))
                counter += 1
                break
    return sequences



def select_start_sequence(series, start_position, relation_tensor, current_pheromone_level, sequences_):
    value_sum = 0
    probabilities = [0] * len(sequences_.keys())
    for i in sequences_.keys():
        current_sequence_steps = list(map(int, sequences_[i].split()))
        current_sequence_intervals = [series[start_position]]
        current_position = start_position
        for j in current_sequence_steps:
            current_position += j
            current_sequence_intervals.append(series[current_position])
        relation = str([current_sequence_intervals, current_sequence_steps])
        if relation in relation_tensor.keys():
            value_sum += relation_tensor[relation]
            probabilities[i] = relation_tensor[relation]
        elif relation.find('NaN') != -1:
            probabilities[i] = 0
        else:
            value_sum += current_pheromone_level
            probabilities[i] = current_pheromone_level
    if value_sum == 0:
        return -1
    probabilities = [probability / value_sum for probability in probabilities]
    sequence_steps = list(map(int, sequences_[numpy.random.choice(numpy.arange(len(sequences_.keys())), p=probabilities)].split()))
    sequence_intervals = [series[start_position]]
    current_position = start_position
    for j in sequence_steps:
        current_position += j
        sequence_intervals.append(series[current_position])
    return [sequence_intervals, sequence_steps]


def select_next_step(series, current_position, current_sequence, relation_tensor, current_pheromone_level, max_step):
    value_sum = 0
    probabilities = []
    for step in range(1, max_step + 1):
        if series[current_position + step] == "NaN":
            probabilities.append(0)
            continue
        relation = str([current_sequence[0] + [series[current_position + step]], current_sequence[1] + [step]])
        if relation in relation_tensor.keys():
            value_sum += relation_tensor[relation]
            probabilities.append(relation_tensor[relation])
        else:
            value_sum += current_pheromone_level
            probabilities.append(current_pheromone_level)
    if value_sum == 0:
        return -1
    probabilities = [probability / value_sum for probability in probabilities]
    step = numpy.random.choice(numpy.arange(1, max_step + 1), p=probabilities)
    return step


def select_next_restoring_step(current_sequence, relation_tensor, max_step, interval_number=IntervalCount):
    options = []
    probabilities = []
    for i in range(max_step):
        for j in range(interval_number):
            possible_sequence = [current_sequence[0][:], current_sequence[1][:]]
            possible_sequence[0].append(j)
            possible_sequence[1].append(i)
            if str(possible_sequence) in relation_tensor.keys():
                options.append([j, i])
                probabilities.append(relation_tensor[str(possible_sequence)])
    if not options:
        return -1
    sum_probabilities = sum(probabilities)
    probabilities = [probability / sum_probabilities for probability in probabilities]
    option_number = numpy.random.choice(len(options), p=probabilities)
    step = options[option_number]
    return step





def restore_series(relation_tensor, average_interval_values, recovering_values, intervals, start_values, length=10000, max_step=MaxArcCount, vector_len=ChainLength, max_step_number=1000, max_iter=100000, interval_number=IntervalCount):
    series = ['NaN'] * (length + vector_len * max_step)
    for i in range(len(start_values)):
        series[i] = start_values[i]
    current_elem_counts = [0] * len(series)
    step_counter = 0

    #f = open('log.txt', 'w')
    for i in range(max_step_number):
        if not step_counter % 100:
            print(step_counter // 100, '% done', sep='')
        #print(i)
        step_counter += 1
        current_position = random.randrange(5)
        current_sequence = [[interval_choose(series[current_position], intervals)], numpy.random.randint(max_step, size=vector_len - 1).tolist()]
        for j in range(vector_len - 1):
            current_position += current_sequence[1][j]
            current_sequence[0].append(interval_choose(series[current_position], intervals))

        #f.write('step = ' + str(i) + '\n')
        #f.write('current_position ' + str(current_position) + '\n')
        #f.write('current_sequence ' + str(current_sequence) + '\n')
        for iteration in range(max_iter):
            if current_position >= length:
                break
            next_step = select_next_restoring_step(current_sequence, relation_tensor, max_step)
            if next_step == -1:
                break
            current_position += next_step[1]
            current_elem_counts[current_position] += 1
            if series[current_position] == 'NaN':
                series[current_position] = average_interval_values[next_step[0]]
            else:
                series[current_position] = (series[current_position] * (current_elem_counts[current_position] - 1) + average_interval_values[next_step[0]]) / current_elem_counts[current_position]
            current_sequence[0] = current_sequence[0][1:] + [interval_choose(series[current_position], intervals)]
            current_sequence[1] = current_sequence[1][1:] + [next_step[1]]
            #f.write('   iteration = ' + str(i) + '\n')
            #f.write('   current_position ' + str(current_position) + '\n')
            #f.write('   current_sequence ' + str(current_sequence) + '\n')

    print('done')
    bad_counter = 0
    good_counter = 0
    real_series = []
    for i in range(length):
        if series[i] != 'NaN':
            real_series.append(series[i])

        if series[i] == 'NaN' and 0:
            print(i)
            for j in [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]:
                seq = j
                prob = [0] * interval_number
                vector = [0] * vector_len
                curr_pos = i
                counter = vector_len
                flag = 0
                for k in seq:
                    counter -= 1
                    curr_pos -= k
                    #print(interval_choose(series[curr_pos], intervals), counter, seq)
                    vector[counter] = interval_choose(series[curr_pos], intervals)
                for i1 in range(interval_number):
                    if str([seq, vector + [i1]]) in relation_tensor:
                        print('oooh')
                        prob[i1] = relation_tensor[str([vector + [i1], seq])]
                        flag = 1
                    else:
                        print(str([vector + [i1], seq]))
                        pass
                if flag:
                    good_counter += 1
                    series[i] = numpy.random.choice(numpy.arange(interval_number), p=prob)
                    break

        if series[i] == 'NaN' and 0:
            print(i)
            for j in [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]:
                seq = j
                prob = [0] * interval_number
                vector = [0] * vector_len
                curr_pos = i
                counter = 0
                flag = 0
                for k in seq:
                    counter += 1
                    curr_pos += k
                    # print(interval_choose(series[curr_pos], intervals), counter, seq)
                    vector[counter] = interval_choose(series[curr_pos], intervals)
                for i1 in range(interval_number):
                    if str([seq, [i1] + vector]) in relation_tensor:
                        print('oooh')
                        prob[i1] = relation_tensor[str([vector + [i1], seq])]
                        flag = 1
                    else:
                        #print(str([[i1] + vector, seq]))
                        pass
                if flag:
                    good_counter += 1
                    series[i] = numpy.random.choice(numpy.arange(interval_number), p=prob)
                    break

        if series[i] == 'NaN' and 0:
            print(i)
            for j in [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]:
                seq = j
                prob = [0] * interval_number

                for i1 in range(interval_number):
                    if str([seq, [interval_choose(series[i - seq[0]], intervals), i1, interval_choose(series[i + seq[1]], intervals)]]) in relation_tensor:
                        print('oooh')
                        prob[i1] = relation_tensor[str([vector + [i1], seq])]
                        flag = 1
                    else:
                        #print(str([[i1] + vector, seq]))
                        pass
                if flag:
                    good_counter += 1
                    series[i] = numpy.random.choice(numpy.arange(interval_number), p=prob)
                    break

        if series[i] == 'NaN' and 0:
            bad_counter += 1
            #print('oooh')
            if i != 0 and i != len(series) - 1 and series[i - 1] != 'NaN' and series[i + 1] != 'NaN':
                series[i] = (series[i - 1] + series[i + 1]) / 2
            else:
                series[i] = 0
    series = series[:length]
    #print(min(series), max(series), recovering_values, bad_counter, good_counter)
    unnormalize(real_series, recovering_values)
    return real_series
