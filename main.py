from task1_db import find_px, test_px, graph_px

if __name__ == '__main__':
    find_px('task1_aggr_gcloud_v1')
    # test_px('task1_aggr_v5', 'task1_aggr_test_v5')

# l=100 n=200 px=0.00002 rws
sql_select = f"""
        SELECT id, type, l, n, cur_px 
        FROM table_from_name
        WHERE chosen_for_test=true AND id NOT IN (SELECT record_id FROM table_to_name
                                                    WHERE  record_id IS NOT NULL)
        ORDER BY type;
    """