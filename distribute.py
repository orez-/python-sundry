def distribute2(available, weights):
    distributed_amounts = []
    total_weights = sum(weights)
    for weight in weights:
        weight = float(weight)
        p = weight / total_weights
        distributed_amount = round(p * available)
        distributed_amounts.append(int(distributed_amount))
        total_weights -= weight
        available -= distributed_amount
    return distributed_amounts

lst = [95, 95, 145]
for x in xrange(sum(lst) + 1):
    d = distribute2(x, lst)
    print x, d
    if x != sum(d):
        raise Exception("NO, GOD, NO.")
