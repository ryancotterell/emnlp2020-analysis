import numpy as np
import random
import sys


def read(fname):
	lst = []
	with open(fname, 'r') as f:
		for i, line in enumerate(f):
			if i == 0:
				continue
			split = line.strip().split("\t")
			lst.append(int(split[1]))
	return lst

m, f = read(sys.argv[1]), read(sys.argv[2])


def permute(m, f):
	both = m + f
	random.shuffle(both)
	p1, p2 = both[:len(m)], both[len(m):]

	# basic santiy checks
	assert len(p1) + len(p2) == len(m) + len(f)
	assert sum(both) == sum(p1+p2)

	return p1, p2 


def test(m, f, statistic, comp, permutations=10000):
	count = 0.0
	sum1, sum2 = 0.0, 0.0
	for _ in range(permutations):
		p1, p2 = permute(m, f)
		if comp(statistic(p1), statistic(m)):
			count += 1
		sum1 += statistic(p1)
		sum2 += statistic(p2)

	return (count + 1) / (permutations + 1)


# comparison directions
high = lambda x, y: x >= y
low = lambda x, y: y <= x

# other test statistics
gtr5 = lambda x: len(list(filter(lambda e: e >= 5, x))) / float(len(x))
gtr10 = lambda x: len(list(filter(lambda e: e >= 10, x))) / float(len(x))
gtr100 = lambda x: len(list(filter(lambda e: e >= 100, x))) / float(len(x))
gtr200 = lambda x: len(list(filter(lambda e: e >= 200, x))) / float(len(x))

# run the unpaired permutation tests
for (desc, statistic, comp) in [("mean", np.mean, high), ("median", np.median, high), ("std", np.std, low), (">= 5", gtr5, high), (">= 10", gtr10, high), (">= 100", gtr100, high), (">= 200", gtr200, high)]:
	print("{0}\tmain: {1}, findings: {2}, p-value {3}".format(*(desc, statistic(m), statistic(f), test(m, f, statistic, comp))))

