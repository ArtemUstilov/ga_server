from concurrent.futures.thread import ThreadPoolExecutor

from old.database import pop_one_row, TestQueueRecord, Session
from old.task.constants import NUM_PROGONS
from old.task.task import run_test


def run_tester(limit=1):
    with ThreadPoolExecutor(max_workers=20) as executor:
        for _ in range(limit):
            executor.submit(test_record)


def test_record():
    session = Session()
    queue_record = pop_one_row(TestQueueRecord)
    test = run_test(queue_record, session)
    prev_coef = test.params['prev_coef']

    if test.count_succ_80 != NUM_PROGONS and test.count_succ_120 == NUM_PROGONS:
        # Strange case that should not happen, need to rerun
        session.add(TestQueueRecord(record_id=test.record_id, coef=prev_coef))

    if test.count_succ_80 != NUM_PROGONS:
        # The Pmax is too high
        session.add(TestQueueRecord(record_id=test.record_id, coef=prev_coef - 0.1))

    if test.count_succ_120 == NUM_PROGONS:
        # The Pmax is too low
        session.add(TestQueueRecord(record_id=test.record_id, coef=prev_coef + 0.1))

    session.commit()
