def next_population_size_type_1(iteration, _):
    if iteration > 10:
        return 2 ** 10
    return 2 ** iteration


def next_population_size_type_2(iteration, _):
    if iteration > 80:
        return 2048
    return int(1.1 ** iteration)


def next_population_size_type_3(_, prev_size):
    return int(min(2000, max(prev_size+1, prev_size*1.005)))


def next_population_size_type_4(iteration, _):
    return min(iteration+1, 2000)


def next_population_size_type_3_init_200(iteration, prev_size):
    if iteration == 0:
        return 200
    return int(min(2000, max(prev_size+1, prev_size*1.005)))


def next_population_size_type_3_init_200_increase_from_500(iteration, prev_size):
    if iteration < 200:
        return 200
    return int(min(2000, max(prev_size+1, prev_size*1.005)))

