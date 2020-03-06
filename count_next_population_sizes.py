def next_population_size_type_1(iteration):
    if iteration > 10:
        return 2 ** 10
    return 2 ** iteration


def next_population_size_type_2(iteration):
    if iteration > 80:
        return 2048
    return int(1.1 ** iteration)
