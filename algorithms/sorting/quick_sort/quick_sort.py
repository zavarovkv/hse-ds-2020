# Given an array, return it sorted in the increasing order
# using the Quicksort algorithm.


def qsort(array):
    if not array:
        return []
    else:
        pivot = array[0]
        less = [x for x in array if x < pivot]
        more = [x for x in array[1:] if x >= pivot]
        return qsort(less) + [pivot] + qsort(more)


arr = [3, 2, 1, 4]
# check that your code works correctly on provided example
assert qsort(arr) == [1, 2, 3, 4], 'Wrong answer'
