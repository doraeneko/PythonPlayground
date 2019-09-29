# Toying around with primitive bayesian network
#
# X1    X2
#  \    /
#   \  /
#    X3
#


def prob_for_x1(probe):
    positives = 0.0
    for (x1, x2, x3) in probe:
        if x1 == 1:
            positives += 1.0
    return positives / len(probe)


def prob_for_x2(probe):
    positives = 0.0
    for (x1, x2, x3) in probe:
        if x2 == 1:
            positives += 1.0
    return positives / len(probe)


def prob_for_x3(probe):
    positives = 0.0
    for (x1, x2, x3) in probe:
        if x3 == 1:
            positives += 1.0
    return positives / len(probe)


def prob_table_for_x3(probe):
    partition_sizes = {(0, 0): 0.0, (0, 1): 0.0, (1, 0): 0.0, (1, 1): 0.0}
    positives = dict(partition_sizes)
    cond_distribution = dict(partition_sizes)
    for (x1, x2, x3) in probe:
        partition_sizes[(x1, x2)] += 1.0
        if x3 == 1:
            positives[(x1, x2)] += 1.0
    for (x1, x2) in partition_sizes:
        size = partition_sizes[(x1, x2)]
        positive_count = positives[(x1, x2)]
        if size == 0:
            continue
        cond_distribution[(x1, x2)] = positive_count / size
    return cond_distribution


def compute_probability_for_x3_being_1(probe):
    p_x1 = prob_for_x1(probe)
    p_x2 = prob_for_x2(probe)
    distribution = prob_table_for_x3(probe)
    conditional_prob = 0.0
    for (n1, n2) in distribution:
        p1 = p_x1 if n1 else 1 - p_x1
        p2 = p_x2 if n2 else 1 - p_x2
        conditional_prob += distribution[(n1, n2)] * p1 * p2
    return conditional_prob


def compute_probability_for_x3_being_1_if_x1_is_1(probe):
    p_x2 = prob_for_x2(probe)
    distribution = prob_table_for_x3(probe)
    # Pr[x1 == 1] * Sum{i=1,2}(Pr[x2 == i] * Pr[x3 == 1 | x1 == 1, x2 == i])
    conditional_prob = (1 - p_x2) * distribution[(1, 0)] + p_x2 * distribution[(1, 1)]
    return conditional_prob


def compute_probability_for_x3_being_1_if_x2_is_1(probe):
    p_x1 = prob_for_x1(probe)
    p_x2 = prob_for_x2(probe)
    distribution = prob_table_for_x3(probe)
    conditional_prob = (1 - p_x1) * distribution[(0, 1)] + p_x1 * distribution[(1, 1)]
    return conditional_prob


probe = [
    (1, 1, 1),
    (0, 0, 1),
    (1, 0, 0),
    (1, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (0, 0, 0),
    (0, 0, 0),
    (0, 1, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (1, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
    (1, 1, 1),
    (0, 1, 1),
    (1, 1, 1),
    (0, 1, 1),
]

import random

# probe = []
# for i in range(1000):
#   probe.append(
#       ((random.randint(0, 1)), (random.randint(0, 1)), (random.randint(0, 1)))
#   )
print('Pr[ X3==1 ] = %s' % compute_probability_for_x3_being_1(probe))
print('Pr[ X3==1 | X1==1 ] = %s' % compute_probability_for_x3_being_1_if_x1_is_1(probe))
print('Pr[ X3==1 | X2==1 ] = %s' % compute_probability_for_x3_being_1_if_x2_is_1(probe))
