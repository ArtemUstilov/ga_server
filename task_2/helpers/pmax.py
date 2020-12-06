from task_2.helpers.constants import RWS_SEL, TOURNAMENT_SEL_GROUP


def _rws(L, N) -> float:
    return 0.39869718 / (L * N)


def _tournament(L, N) -> float:
    return 0.69157678 / (L * N)


def get_p_max(sel_type: str, L: int, N: int) -> float:
    if sel_type == RWS_SEL:
        return _rws(L, N)

    if sel_type in TOURNAMENT_SEL_GROUP:
        return _tournament(L, N)
