"""
Chain of operations.
"""

def basic_chain(funcs, init, times):
    """
    Return reduce(lambda a, b: funcs[0](a, b), [init]*(times - 1), init)
    in more efficient manner.
    The funcs[1] is another function satisfying:
      funcs[1](a) == funcs[0](a, a).

    PRECOND: times >= 1 and isinstance(times, (int, long))
             len(funcs) == 2
    """
    # right to left binary.
    result = init
    meta = init
    index = times - 1
    func, meta_func = funcs
    while index:
        if index % 2:
            result = func(result, meta)
        index //= 2
        if index:
            meta = meta_func(meta)
    return result


def multi_chains(funcs, inits, times):
    """
    Return [reduce(lambda a, b: funcs[0](a, b), [init]*(times - 1), init)
            for init in inits]
    in more efficient manner.
    The funcs[1] is another function satisfying:
      funcs[1](a) == funcs[0](a, a).

    PRECOND: times >= 1 and isinstance(times, (int, long))
             len(funcs) == 2
    """
    # right to left binary.
    results = list(inits)
    metas = list(results)
    index = times - 1
    func, meta_func = funcs
    while index:
        if index % 2:
            results = [func(r, m) for (r, m) in zip(results, metas)]
        index //= 2
        if index:
            metas = map(meta_func, metas)
    return results


def oneway_chains(funcs, inits, times):
    """
    Return result of chain.
    funcs is a sequence of 2-tuple of functions.
    i-th tuple's func[0] have 2*(i+1) arguments, and func[1] 2*(i+1)-1.

    The funcs[1] is another function satisfying:
      funcs[i+1][1](a_{i+1}, *p) == funcs[i+1][0](a_{i+1}, a_{i+1}, *p),
    where p = (a_0, b_0, a_1, b_1,..., a_i, b_i).

    PRECOND: times >= 1 and isinstance(times, (int, long))
             len(funcs) == 2 * len(inits)
    """
    # right to left binary.
    results = list(inits)
    metas = list(results)
    index = times - 1
    while index:
        if index % 2:
            new_results, p = [], []
            for (i, (r, m)) in enumerate(zip(results, metas)):
                new_results.append(funcs[i][0](r, m, *p))
                p.expand([r, m])
            results = new_results
        index //= 2
        if index:
            new_metas, p = [], []
            for (i, (r, m)) in enumerate(zip(results, metas)):
                new_results.append(funcs[i][1](m, *p))
                p.expand([r, m])
            metas = new_metas
    return results
