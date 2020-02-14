CREATE TABLE task1_aggr_v4 (
    id SERIAL PRIMARY KEY ,
    L INTEGER,
    N INTEGER,
    type varchar(15),
    try_id INTEGER,
    cur_px DOUBLE PRECISION,
    runs_succ BOOLEAN[],
    count_succ INTEGER,
    is_final BOOLEAN,
    chosen_for_test BOOLEAN,
    is_result BOOLEAN
);


CREATE TABLE task1_aggr_v5 (
    id SERIAL PRIMARY KEY ,
    L INTEGER,
    N INTEGER,
    type varchar(15),
    try_id INTEGER,
    cur_px DOUBLE PRECISION,
    runs_succ INTEGER[],
    count_succ INTEGER,
    is_final BOOLEAN,
    chosen_for_test BOOLEAN,
    is_result BOOLEAN
);


CREATE TABLE task1_aggr_test_v4 (
    id SERIAL PRIMARY KEY,
    record_id INTEGER REFERENCES task1_aggr_v4(id),
    L INTEGER,
    N INTEGER,
    type varchar(15),
    test_px DOUBLE PRECISION,
    runs_succ BOOLEAN[],
    count_succ INTEGER,
    test_px120 DOUBLE PRECISION,
    runs_succ120 BOOLEAN[],
    count_succ120 INTEGER,
    test_px80 DOUBLE PRECISION,
    runs_succ80 BOOLEAN[],
    count_succ80 INTEGER
);

CREATE TABLE task1_02_02_20
(
    L INTEGER,
    N INTEGER,
    run_id INTEGER,
    iteration INTEGER,

    pairwise_hamming_distribution_p DOUBLE PRECISION[],
    pairwise_hamming_distribution_abs BIGINT[],
    ideal_hamming_distribution_p DOUBLE PRECISION[],
    ideal_hamming_distribution_abs BIGINT[],
    wild_type_hamming_distribution_p DOUBLE PRECISION[],
    wild_type_hamming_distribution_abs BIGINT[],

    expected_value_pair DOUBLE PRECISION,
    std_pair DOUBLE PRECISION,
    expected_value_ideal DOUBLE PRECISION,
    std_ideal DOUBLE PRECISION,
    expected_value_wild DOUBLE PRECISION,
    std_wild DOUBLE PRECISION,

    mode_pair INTEGER,
    mode_ideal INTEGER,
    mode_wild INTEGER,

    health BIGINT[],
    mean_health DOUBLE PRECISION,
    mean_health_diff_0 DOUBLE PRECISION,
    best_health_diff_0 DOUBLE PRECISION
);

CREATE TABLE task2_full
(
    id SERIAL PRIMARY KEY,
    L INTEGER,
    N INTEGER,
    run_id INTEGER,
    iteration INTEGER,

    pairwise_hamming_distribution_p DOUBLE PRECISION[],
    pairwise_hamming_distribution_abs BIGINT[],
    ideal_hamming_distribution_p DOUBLE PRECISION[],
    ideal_hamming_distribution_abs BIGINT[],
    wild_type_hamming_distribution_p DOUBLE PRECISION[],
    wild_type_hamming_distribution_abs BIGINT[],

    expected_value_pair DOUBLE PRECISION,
    std_pair DOUBLE PRECISION,
    expected_value_ideal DOUBLE PRECISION,
    std_ideal DOUBLE PRECISION,
    expected_value_wild DOUBLE PRECISION,
    std_wild DOUBLE PRECISION,

    mode_pair INTEGER,
    mode_ideal INTEGER,
    mode_wild INTEGER,

    health BIGINT[],
    mean_health DOUBLE PRECISION,
    mean_health_diff_0 DOUBLE PRECISION,
    best_health_diff_0 DOUBLE PRECISION
);