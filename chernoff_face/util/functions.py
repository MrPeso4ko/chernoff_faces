def composite_or(*funcs):
    """Returns composition of geometry functions: f_1(x, y) *or* f_2(x, y) *or* ... *or* f_n(x, y)
    :param funcs: functions to composite. Each should take two arguments x, y and return True if point lies
    on figure and False otherwise"""

    def res(x, y):
        for func in funcs:
            if func(x, y):
                return True
        return False

    return res
