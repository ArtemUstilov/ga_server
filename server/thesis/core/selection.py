import random

import numpy as np


def roulette_help(population, probabilities):
    probabilities = probabilities.clip(min=0)

    sum_val = probabilities.sum()
    if sum_val != 0:
        probabilities = probabilities / sum_val
    else:
        probabilities = np.ones(len(probabilities)) / len(probabilities)

    random_indexes = np.random.choice(len(population), len(population), p=probabilities)

    return population[random_indexes], np.unique(random_indexes).shape[0]


def roulette(population, values, **kwargs):
    return roulette_help(population, values)


def roulette_linear(population, values, sel_param1, sel_param3, **kwargs):
    print(sel_param3)
    probabilities = sel_param1 * values + sel_param3
    return roulette_help(population, probabilities)


def roulette_sigma(population, values, sel_param1, **kwargs):
    probabilities = values - (values.mean() - sel_param1 * np.std(values))
    return roulette_help(population, probabilities)


def roulette_destroy(population, values, **kwargs):
    probabilities = np.abs(values - values.mean())
    return roulette_help(population, probabilities)


def roulette_mixed(population, values, G, iter, **kwargs):
    probabilities = values/(G+1-iter)
    return roulette_help(population, probabilities)


def roulette_power(population, values, sel_param1, **kwargs):
    probabilities = values ** sel_param1
    return roulette_help(population, probabilities)


def tournament_gen(population, values, sel_param1, **kwargs):
    tours = np.random.choice(population.shape[0], (len(population), int(sel_param1)))

    tour_winner = np.argmax(values[tours], axis=1)

    indxes = tours[np.arange(len(population)), tour_winner]

    return population[indxes], np.unique(indxes).shape[0]


def tournament_without_return_gen(population, values, sel_param1, **kwargs):
    size = int(sel_param1)
    ind_res = []
    bad_indx = []
    while len(ind_res) != len(population):
        if len(population) - len(bad_indx) < size:
            bad_indx = []
        tour_indexes = np.random.choice(np.setdiff1d(range(0, len(population)), bad_indx), size)
        winner = tour_indexes[np.argmax(values[tour_indexes])]
        ind_res.append(winner)
        bad_indx.extend(tour_indexes)

    ind_res = np.array(ind_res)

    return population[ind_res], np.unique(ind_res).shape[0]


def sus(population, values, **kwargs):
    sum_val = values.sum()
    if sum_val != 0:
        probabilities = values / sum_val
    else:
        probabilities = 1 / len(values)

    return sus_with_probs(probabilities, population, values)


def sus_with_probs(probabilities, population, values):
    k = random.random()

    res = list()
    probabilities = probabilities * probabilities.shape[0]
    probabilities_matched = np.array([])

    for i in range(0, len(probabilities)):
        if i == 0:
            probabilities_matched = np.append(probabilities_matched, probabilities[i])
        else:
            probabilities_matched = np.append(probabilities_matched, probabilities[i] + probabilities_matched[i - 1])

    cur_sum = k

    indxes = []

    for i in range(0, len(values)):
        find = np.nonzero(probabilities_matched >= cur_sum)
        ind = find[0][0] if len(find) > 0 else find[-1][0]

        res.append(population[ind])
        indxes.append(ind)
        cur_sum += 1

    return np.array(res), np.unique(indxes).shape[0]


def cutting_selection(population, values, sel_param1, **kwargs):
    sel_param1 = int(sel_param1)
    val_copy = np.copy(values)
    val_copy[::-1].sort()
    val_copy = val_copy[0:sel_param1]

    indexes = np.isin(values, val_copy)

    bads = np.argwhere(values == val_copy[-1])
    for i in range(0, indexes[indexes == True].shape[0] - sel_param1):
        indexes[bads[i][0]] = False

    pop, _ = sus(population, indexes*1)

    return pop, sel_param1


def get_range(values):
    N = values.shape[0]
    indx = np.arange(values.shape[0])
    valind = np.array(list(zip(values, indx)))

    ranges = np.sort(valind.view('i8,i8'), order=['f0'], axis=0).view(int)[::-1][:, 1]

    rangs = list(np.zeros(N))
    for i in range(0, N):
        rangs[ranges[i]] = i
    return N - 1 - np.array(rangs)


def linear_rang(population, values, sel_param1, **kwargs):
    N = values.shape[0]
    B = sel_param1

    probabilities = (2 - B) / N + (2 * get_range(values) * (B - 1)) / (N * (N - 1))
    return sus_with_probs(probabilities, population, values)


def not_linear_rang(population, values, sel_param1, sel_param2, **kwargs):
    N = values.shape[0]
    B = sel_param1
    a = sel_param2
    c = ((B - a) * N * (2 * N - 1)) / (6 * (N - 1)) + N * a
    probabilities = a / c + (get_range(values) * get_range(values) * (B - a)) / ((N - 1) * (N - 1) * c)
    return sus_with_probs(probabilities, population, values)


def exp_rang(population, values, sel_param1, **kwargs):
    N = values.shape[0]
    c = sel_param1
    ranges = get_range(values) + 1
    probabilities = (c - 1) / (c ** N - 1) * (c ** (N - ranges))
    return sus_with_probs(probabilities, population, values)


def uniform(population, values, **kwargs):
    minV = values.min()
    maxV = values.max()

    rand = np.random.randint(minV, maxV, values.shape[0]) if minV < maxV else np.ones(values.shape[0]) * minV
    sel_indexes = list(np.zeros(values.shape[0]))
    for i in range(values.shape[0]):
        sel_indexes[i] = np.argmin(np.abs(values - rand[i]))
    sel_indexes = np.array(sel_indexes)
    return population[sel_indexes], np.unique(sel_indexes).shape[0]
