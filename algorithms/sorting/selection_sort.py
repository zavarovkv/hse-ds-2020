# Python program for implementation of Selection Sort


def SelectionSort(array):
    n = len(array)

    # Traverse through all array elements
    for i in range(len(array)):

        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[min_idx] > array[j]:
                min_idx = j

        array[i], array[min_idx] = array[min_idx], array[i]

    return array
