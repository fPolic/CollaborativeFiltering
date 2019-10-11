import operator
import sys

from decimal import Decimal, ROUND_HALF_UP
from functools import reduce


# ========== HELPERS ==========

def filter_empty(row):
    return list(filter(lambda x: x != 'X', row))


def filter_with_zeros(row):
    return list(map(lambda x: x if x != 'X' else 0, row))


def round_decimal(x):
    return Decimal(Decimal(x).quantize(Decimal('.001'), rounding=ROUND_HALF_UP))


def mean(numbers):
    numbers = filter_empty(numbers)
    return float(sum(numbers)) / len(numbers)


def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def sim(A, B):
    t = reduce(operator.add, map(lambda x, y: x * y, A, B))
    a = reduce(operator.add, map(lambda x: x ** 2, A)) ** (1 / 2)
    b = reduce(operator.add, map(lambda x: x ** 2, B)) ** (1 / 2)

    return t / (a * b)


def create_row_means(matrix, means):
    ret = []
    for row in range(len(matrix)):
        m = means[row]
        normalized = list(map(lambda x: x - m if x != 'X' else 0, matrix[row]))
        ret.append(normalized)
    return ret


# ========== STRATEGY ==========

def strategy(I, J, K, matrix, normalised_matrix):
    sims = []
    base = normalised_matrix[I]

    for ind, item in enumerate(normalised_matrix):
        if ind == I: pass
        similarity = sim(item, base)
        sims.append((similarity, filter_with_zeros(matrix[ind])[J]))

    sims = sorted(sims, key=lambda x: x[0], reverse=True)
    sims = list(filter(lambda x: x[0] > 0 and x[1] != 0, sims))[:K]

    a = reduce(operator.add, [t[0] * t[1] for t in sims])
    b = reduce(operator.add, [t[0] for t in sims])

    return a / b


def main():
    N, M = [int(i.strip()) for i in sys.stdin.readline().split(' ')]
    
    item_matrix = []
    item_means = []

    for i in range(N):
        line = [i if i == 'X' else int(i) for i in sys.stdin.readline().strip().split(' ')]
        item_matrix.append(line)
        item_means.append(mean(line))

    user_matrix = transpose(item_matrix)
    user_means = [mean(line) for line in user_matrix]

    item_mean_matrix = create_row_means(item_matrix, item_means)
    user_mean_matrix = create_row_means(user_matrix, user_means)

    Q = int(sys.stdin.readline().strip())

    for i in range(Q):
        I, J, T, K = [int(i) for i in sys.stdin.readline().split(' ')]

        if T == 1:
            r = strategy(J - 1, I - 1, K, user_matrix, user_mean_matrix)
        else:
            r = strategy(I - 1, J - 1, K, item_matrix, item_mean_matrix)

        print(round_decimal(r))


if __name__ == '__main__':
    main()
