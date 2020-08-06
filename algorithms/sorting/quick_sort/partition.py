# Given an array and a pivot element index, implement the
# partition function: move all the elements smaller than
# pivot element to the left of it and all the elements
# larger than it to the right. Return the array after
# partition.


def partition(array, pivot_index):
    pivot = array[pivot_index]
    left_list, right_list, pivot_list = [], [], []

    for item in array:
        if item < pivot:
            left_list.append(item)
        elif item > pivot:
            right_list.append(item)
        else:
            pivot_list.append(item)

    return left_list + pivot_list + right_list


arr = [3, 2, 1, 4]
pivot_index = 0
# check that your code works correctly on provided example
assert partition(arr, pivot_index) in [[1, 2, 3, 4], [2, 1, 3, 4]], 'Wrong answer'
