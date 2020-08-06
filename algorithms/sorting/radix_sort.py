# Python program for implementation of Radix Sort

# You are given a list of names, each name is not longer
# than 20 characters. Return them sorted in an increasing
# order, using the Radix Sort algorithm.


def RadixSort(names, i=0):
    if len(names) <= 1:
        return names

    done_bucket = []
    buckets = [[] for x in range(1000)]

    for s in names:
        if i >= len(s):
            done_bucket.append(s)
        else:
            buckets[ord(s[i]) - ord('a')].append(s)

    buckets = [RadixSort(b, i + 1) for b in buckets]

    return done_bucket + [b for blist in buckets for b in blist]


arr = ['Ivan', 'John', 'Anna']
# check that your code works correctly on provided example
assert RadixSort(arr) == ['Anna', 'Ivan', 'John'], 'Wrong answer'
