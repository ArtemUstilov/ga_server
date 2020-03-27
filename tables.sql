CREATE TABLE task1_aggr_v4
(
    id              SERIAL PRIMARY KEY,
    L               INTEGER,
    N               INTEGER,
    type            varchar(15),
    try_id          INTEGER,
    cur_px          DOUBLE PRECISION,
    runs_succ       BOOLEAN[],
    count_succ      INTEGER,
    is_final        BOOLEAN,
    chosen_for_test BOOLEAN,
    is_result       BOOLEAN
);


CREATE TABLE task1_aggr_v5
(
    id              SERIAL PRIMARY KEY,
    L               INTEGER,
    N               INTEGER,
    type            varchar(15),
    try_id          INTEGER,
    cur_px          DOUBLE PRECISION,
    runs_succ       INTEGER[],
    count_succ      INTEGER,
    is_final        BOOLEAN,
    chosen_for_test BOOLEAN,
    is_result       BOOLEAN
);


CREATE TABLE task1_aggr_test_v4
(
    id            SERIAL PRIMARY KEY,
    record_id     INTEGER REFERENCES task1_aggr_v4 (id),
    L             INTEGER,
    N             INTEGER,
    type          varchar(15),
    test_px       DOUBLE PRECISION,
    runs_succ     BOOLEAN[],
    count_succ    INTEGER,
    test_px120    DOUBLE PRECISION,
    runs_succ120  BOOLEAN[],
    count_succ120 INTEGER,
    test_px80     DOUBLE PRECISION,
    runs_succ80   BOOLEAN[],
    count_succ80  INTEGER
);

CREATE TABLE task1_extended
(
    id              SERIAL PRIMARY KEY,
    L               INTEGER,
    N               INTEGER,
    init            varchar(15),
    estim           varchar(15),
    type            varchar(15),
    try_id          INTEGER,
    cur_px          DOUBLE PRECISION,
    runs_succ       INTEGER[],
    count_succ      INTEGER,
    is_final        BOOLEAN,
    chosen_for_test BOOLEAN,
    is_old          BOOLEAN
);

CREATE TABLE task1_extended_run_details
(
    id              BIGSERIAL PRIMARY KEY,
    run_id          INTEGER REFERENCES task1_extended (id),
    run_number      INTEGER,
    mean_health     DOUBLE PRECISION[],
    polymorphous1_p DOUBLE PRECISION[],
    polymorphous2_p DOUBLE PRECISION[]
);

CREATE TABLE task1_extended_run_details_test
(
    id              BIGSERIAL PRIMARY KEY,
    run_id          INTEGER REFERENCES task1_extended_test (id),
    run_number      INTEGER,
    percent         INTEGER,
    mean_health     DOUBLE PRECISION[],
    polymorphous1_p DOUBLE PRECISION[],
    polymorphous2_p DOUBLE PRECISION[]
);

CREATE TABLE task1_extended_test
(
    id             SERIAL PRIMARY KEY,
    record_id      INTEGER REFERENCES task1_extended (id),
    L              INTEGER,
    N              INTEGER,
    init           varchar(15),
    estim          varchar(15),
    type           varchar(15),
    test_px        DOUBLE PRECISION,
    runs_succ      INTEGER[],
    count_succ     INTEGER,
    test_px120     DOUBLE PRECISION,
    runs_succ120   INTEGER[],
    count_succ120  INTEGER,
    test_px80      DOUBLE PRECISION,
    runs_succ80    INTEGER[],
    count_succ80   INTEGER,
    is_old         BOOLEAN DEFAULT False
);

CREATE TABLE task2_full
(
    id                                 BIGSERIAL PRIMARY KEY,
    init                               CHAR(20),
    estim                              CHAR(20),
    sel_type                           CHAR(20),
    L                                  INTEGER,
    N                                  INTEGER,
    run_id                             INTEGER,
    iteration                          INTEGER,

    pairwise_hamming_distribution_p    DOUBLE PRECISION[],
    pairwise_hamming_distribution_abs  BIGINT[],
    ideal_hamming_distribution_p       DOUBLE PRECISION[],
    ideal_hamming_distribution_abs     BIGINT[],
    wild_type_hamming_distribution_p   DOUBLE PRECISION[],
    wild_type_hamming_distribution_abs BIGINT[],

    expected_value_pair                DOUBLE PRECISION,
    std_pair                           DOUBLE PRECISION,
    expected_value_ideal               DOUBLE PRECISION,
    std_ideal                          DOUBLE PRECISION,
    expected_value_wild                DOUBLE PRECISION,
    std_wild                           DOUBLE PRECISION,

    min_pair                           BIGINT,
    max_pair                           BIGINT,
    min_ideal                          BIGINT,
    max_ideal                          BIGINT,
    min_wild                           BIGINT,
    max_wild                           BIGINT,

    variance_coef_pair                 DOUBLE PRECISION,
    variance_coef_ideal                DOUBLE PRECISION,
    variance_coef_wild                 DOUBLE PRECISION,


    mode_pair                          INTEGER[],
    mode_ideal                         INTEGER[],
    mode_wild                          INTEGER[],

    health                             BIGINT[],
    mean_health                        DOUBLE PRECISION,
    mean_health_diff_0                 DOUBLE PRECISION,
    best_health_diff_0                 DOUBLE PRECISION
);