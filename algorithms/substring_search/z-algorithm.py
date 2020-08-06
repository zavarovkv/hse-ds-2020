# Given a text and a pattern find all occurrences of the
# pattern inside the text using the Z-algorithm. You should
# output the starting indices of the matches.


def zFunction(text):
    n = len(text)
    z_func = [0 for i in range(n)]
    l, r, k = 0, 0, 0

    for i in range(1, n):
        if i > r:
            l, r = i, i
            while r < n and text[r - l] == text[r]:
                r += 1
            z_func[i] = r - l
            r -= 1
        else:
            k = i - l
            if z_func[k] < r - i + 1:
                z_func[i] = z_func[k]
            else:
                l = i
                while r < n and text[r - l] == text[r]:
                    r += 1
                z_func[i] = r - l
                r -= 1

    return z_func


def zAlgorithm(text, pattern):
    concat = pattern + "#" + text
    indices = []
    l = len(concat)

    z = zFunction(concat)

    for i in range(l):
        if z[i] == len(pattern):
            indices.append(i - len(pattern) - 1)

    return indices


text = 'abracadabra'
pattern = 'ab'
# check that your code works correctly on provided example
assert zAlgorithm(text, pattern) == [0, 7], 'Wrong answer'
