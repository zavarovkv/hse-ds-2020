# Python program for implementation of Counting Sort

# Given an array of integers, and the bounds for values in the array,
# return the array sorted in an increasing order using the Counting
# Sort algorithm.


def CountingSort(array, lowerbound, upperbound):
    sorted_array = []
    count = [0 for i in range(lowerbound, upperbound + 1)]

    for number in array:
        if lowerbound <= number <= upperbound:
            count[number - lowerbound] += 1

    for i in range(len(count)):
        for j in range(0, count[i]):
            sorted_array.append(i + lowerbound)

    return sorted_array


assert CountingSort([3, 2, 1], 1, 3) == [1, 2, 3], 'Wrong answer'
