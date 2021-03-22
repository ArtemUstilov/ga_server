select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc, case when ii.health[1] = 100 then 1 else 0 end from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс '
order by ss.created_date






select tt0.id, tt0.sel_type, tt0.sel_param1,
       tt0.iteration, tti0.intc ,
       tt1.iteration, tti1.intc ,
       tt2.iteration, tti2.intc ,
       tt3.iteration, tti3.intc ,
       tt4.iteration, tti4.intc ,
       tt5.iteration, tti5.intc ,
       tt6.iteration, tti6.intc ,
       tt7.iteration, tti7.intc ,
       tt8.iteration, tti8.intc ,
       tt9.iteration, tti9.intc
from (select ss.id, ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=0
order by ss.created_date
) tt0 inner join
(select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=0
group by ss.id, ss.sel_type, ss.sel_param1
) tti0 on tt0.sel_type = tti0.sel_type and tt0.sel_param1 = tti0.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=1
order by ss.created_date
) tt1 on tt0.sel_type = tt1.sel_type and tt0.sel_param1 = tt1.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=1
group by ss.id, ss.sel_type, ss.sel_param1
) tti1 on tt0.sel_type = tti1.sel_type and tt0.sel_param1 = tti1.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=2
order by ss.created_date
) tt2 on tt0.sel_type = tt2.sel_type and tt0.sel_param1 = tt2.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=2
group by ss.id, ss.sel_type, ss.sel_param1
) tti2 on tt0.sel_type = tti2.sel_type and tt0.sel_param1 = tti2.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=3
order by ss.created_date
) tt3 on tt0.sel_type = tt3.sel_type and tt0.sel_param1 = tt3.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=3
group by ss.id, ss.sel_type, ss.sel_param1
) tti3 on tt0.sel_type = tti3.sel_type and tt0.sel_param1 = tti3.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=4
order by ss.created_date
) tt4 on tt0.sel_type = tt4.sel_type and tt0.sel_param1 = tt4.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=4
group by ss.id, ss.sel_type, ss.sel_param1
) tti4 on tt0.sel_type = tti4.sel_type and tt0.sel_param1 = tti4.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=5
order by ss.created_date
) tt5 on tt0.sel_type = tt5.sel_type and tt0.sel_param1 = tt5.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=5
group by ss.id, ss.sel_type, ss.sel_param1
) tti5 on tt0.sel_type = tti5.sel_type and tt0.sel_param1 = tti5.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=6
order by ss.created_date
) tt6 on tt0.sel_type = tt6.sel_type and tt0.sel_param1 = tt6.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=6
group by ss.id, ss.sel_type, ss.sel_param1
) tti6 on tt0.sel_type = tti6.sel_type and tt0.sel_param1 = tti6.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=7
order by ss.created_date
) tt7 on tt0.sel_type = tt7.sel_type and tt0.sel_param1 = tt7.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=7
group by ss.id, ss.sel_type, ss.sel_param1
) tti7 on tt0.sel_type = tti7.sel_type and tt0.sel_param1 = tti7.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=8
order by ss.created_date
) tt8 on tt0.sel_type = tt8.sel_type and tt0.sel_param1 = tt8.sel_param1
inner join
    (select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=8
group by ss.id, ss.sel_type, ss.sel_param1
) tti8 on tt0.sel_type = tti8.sel_type and tt0.sel_param1 = tti8.sel_param1
inner join
(select ss.sel_type, ss.sel_param1, ss.sel_param2, ss.run_id, ii.iteration, round(ii.intensity_prev*1000)/1000 as intc
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id and ii.last_iter=true
where ss.title = 'тиск, інтенс ' and run_id=9
order by ss.created_date
) tt9 on tt0.sel_type = tt9.sel_type and tt0.sel_param1 = tt9.sel_param1
    inner join
(select round(avg(ii.intensity_prev)*1000)/1000 as intc,  ss.sel_type, ss.sel_param1
    from ga_run_settings ss
    inner join ga_run_info ii on ss.id = ii.ga_run_settings_id
where ss.title = 'тиск, інтенс ' and run_id=9
group by ss.id, ss.sel_type, ss.sel_param1
) tti9 on tt0.sel_type = tti9.sel_type and tt0.sel_param1 = tti9.sel_param1
