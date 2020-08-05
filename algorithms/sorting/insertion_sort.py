# Python program for implementation of Insertion Sort


def InsertionSort(array):
    n = len(array)

    # Traverse through 1 to len(array)
    for i in range(1, len(array)):

        key = array[i]
        j = i - 1

        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j -= 1
        array[j + 1] = key

    return array
