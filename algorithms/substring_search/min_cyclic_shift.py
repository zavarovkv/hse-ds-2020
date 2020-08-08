# You are given two strings, where the second string is the first
# string that has been cyclically shifted (or has it?). Example of
# a cyclic shift: abcde -> deabc. Output the minimum possible cycle
# shift to obtain the second string from the first, or -1 if it's
# not possible.


def minCyclicShift(original_string, shifted_string):

    if len(original_string) != len(shifted_string):
        return -1

    if original_string == shifted_string:
        return 0

    for shift in range(1, len(shifted_string)):
        shifted = original_string[-shift:] + original_string[:-shift]
        if shifted == shifted_string:
            return shift

    return -1


original_string = 'abcde'
shifted_string = 'deabc'
# check that your code works correctly on provided example
assert minCyclicShift(original_string, shifted_string) == 2, 'Wrong answer'
