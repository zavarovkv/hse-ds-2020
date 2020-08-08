# String S has been written over and over and over, and you are
# presented with a result: "SSSSSSS...". Find the length of
# the shortest possible S.


def shortestCycle(cyclic_string):
    if not cyclic_string:
        return 0

    nxt = [0] * len(cyclic_string)
    for i in range(1, len(nxt)):
        k = nxt[i - 1]
        while True:
            if cyclic_string[i] == cyclic_string[k]:
                nxt[i] = k + 1
                break
            elif k == 0:
                nxt[i] = 0
                break
            else:
                k = nxt[k - 1]

    small_string = len(cyclic_string) - nxt[-1]

    if len(cyclic_string) % small_string != 0:
        return len(cyclic_string)

    return len(cyclic_string[0:small_string])


cyclic_string = 'ababab'
# check that your code works correctly on provided example
assert shortestCycle(cyclic_string) == 2, 'Wrong answer'
