create table ga_run_settings
(
    -- Only integer types can be auto increment
    id            varchar not null
        constraint ga_run_settings_pkey
            primary key,
    init          char(20),
    estim         char(20),
    sel_type      char(20),
    l             integer,
    run_id        integer,
    created_date  timestamp default now(),
    size_pop_type char(20),
    chart         bytea
);

alter table ga_run_settings
    owner to artemustilov;

create table ga_run_info
(
    id                                 serial  not null
        constraint task2_variant_2_pkey
            primary key,
    iteration                          integer,
    pairwise_hamming_distribution_p    double precision[],
    pairwise_hamming_distribution_abs  bigint[],
    ideal_hamming_distribution_p       double precision[],
    ideal_hamming_distribution_abs     bigint[],
    wild_type_hamming_distribution_p   double precision[],
    wild_type_hamming_distribution_abs bigint[],
    expected_value_pair                double precision,
    std_pair                           double precision,
    expected_value_ideal               double precision,
    std_ideal                          double precision,
    expected_value_wild                double precision,
    std_wild                           double precision,
    min_pair                           bigint,
    max_pair                           bigint,
    min_ideal                          bigint,
    max_ideal                          bigint,
    min_wild                           bigint,
    max_wild                           bigint,
    variance_coef_pair                 double precision,
    variance_coef_ideal                double precision,
    variance_coef_wild                 double precision,
    mode_pair                          integer[],
    mode_ideal                         integer[],
    mode_wild                          integer[],
    health                             bigint[],
    mean_health                        double precision,
    mean_health_diff_0                 double precision,
    best_health_diff_0                 double precision,
    size_pop_type                      char(20),
    polymorphism                       double precision,
    ga_run_settings_id                 varchar not null
        constraint ga_run_info_ga_run_settings_id_fk
            references ga_run_settings
            on update cascade on delete cascade,
    n                                  integer,
    last_iter                          boolean default false
);

alter table ga_run_info
    owner to postgres;

create table locus_helper
(
    l              integer,
    bad_locuses    boolean[],
    good_locuses   boolean[],
    lethal_locuses boolean[],
    locus_markup   integer[]
);

alter table locus_helper
    owner to artemustilov;

create table px_info
(
    id             serial           not null
        constraint px_info_pk
            primary key,
    initialization varchar,
    selection      varchar,
    l              integer,
    n              integer,
    val            double precision not null
);

alter table px_info
    owner to artemustilov;

create unique index px_info_id_uindex
    on px_info (id);

