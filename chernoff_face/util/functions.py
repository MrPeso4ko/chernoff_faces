def _composite_two_or(func1, func2):
    def or_func(x, y):
        return func1(x, y) or func2(x, y)

    return or_func


def composite_or(*funcs):
    """Returns composition of geometry functions: f_1(x, y) *or* f_2(x, y) *or* ... *or* f_n(x, y)
    :param funcs: functions to composite. Each should take two arguments x, y and return True if point lies
    on figure and False otherwise"""
    if not funcs:
        return lambda x, y: False
    if len(funcs) == 1:
        return funcs[0]
    res = _composite_two_or(funcs[0], funcs[1])
    for func in funcs[2:]:
        res = _composite_two_or(res, func)
    return res
