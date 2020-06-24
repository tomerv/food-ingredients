import csv
import numpy
import scipy.optimize


def read_file(f):
    names = []
    amounts = []
    reader = csv.reader(f)
    for i,line in enumerate(reader, start=1):
        if len(line) == 0:
            continue
        try:
            name, amount = line
            if not amount.strip():
                amount = None
            else:
                amount = float(amount)
                if not 0.0 <= amount <= 1.0:
                    raise ValueError(f'the amount {amount} is not between 0.0 and 1.0')
        except ValueError as e:
            raise ValueError(
                f'Error reading line {i}: {e}.'
                f' Each line should contain the name of the ingredient and the amount (if known), separated by a single comma.'
                f' Lines without amounts should end with a comma.'
            )
        names.append(name)
        amounts.append(amount)
    return (names, amounts)


def solve(amounts):
    """
    amounts: a list containing the amount of each ingredient (or None is the amount is not known).
    Amounts are between 0.0 and 1.0. The list is sorted according to the amount, from biggest amount to smallest.
    """
    n = len(amounts)

    # Upper bound:
    # For each i,
    #   x_{i+1} - x_{i} <= 0
    # giving a total of (n-1) constraints
    A_ub = numpy.zeros((n-1, n))
    for i in range(n-1):
        A_ub[i, i]   = -1.0
        A_ub[i, i+1] =  1.0
    b_ub = numpy.zeros(n-1)

    # Equality constraints:
    # If we have the value v_i for ingredient x_i,
    # then we have an equality constraint for it.
    # Additionally, the sum of all amounts is 1.0
    not_none = [amount for amount in amounts if amount is not None]
    A_eq = numpy.zeros((len(not_none)+1, n))
    i = 0
    for j,amount in enumerate(amounts):
        if amount is not None:
            A_eq[i,j] = 1.0
            i += 1
    assert i == len(not_none)
    for j in range(n):
        A_eq[i,j] = 1
    b_eq = numpy.array(not_none + [1.0])

    bounds = (0.0, 1.0)

    allowed_error = 1e-6

    # We solve twice for each unknown amount: min and max
    # Wrapper functions so we don't repeat ourselves
    def linprog(c):
        res = scipy.optimize.linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
        if res.status != 0:
            raise ValueError(res.message)
        # assert that all the known values are (approximately) correct
        for i,amount in enumerate(amounts):
            if amount is not None:
                assert abs(res.x[i] - amount) < allowed_error, res.x
        return res.x

    res = [None] * n
    for i,amount in enumerate(amounts):
        if amount is None:
            c = numpy.zeros(n)
            c[i] = 1
            # c is a vector with 1 in the i'th position and 0 elsewhere
            res[i] = (linprog(c)[i], linprog(-c)[i])
            assert res[i][0] - allowed_error <= res[i][1], (i, res[i])
        else:
            res[i] = (amount, amount)
    return res