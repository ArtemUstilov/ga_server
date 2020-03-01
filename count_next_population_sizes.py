def next_population_size_type_1(iteration):
    if iteration > 9:
        return 2 ** 9
    return 2 ** iteration
