# Given a string, compute a z-function array for it.


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


text = 'abracadabra'
# check that your code works correctly on provided example
assert zFunction(text) == [0, 0, 0, 1, 0, 1, 0, 4, 0, 0, 1], 'Wrong answer'
