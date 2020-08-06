# Given a text and a pattern find all occurrences of the pattern
# inside the text using the Rabin-Karp algorithm. You should
# output the starting indices of the matches.


def RabinKarp(text, pattern):
    n, m = len(text), len(pattern)
    p, q = 31, 10 ** 9 + 7
    indices = []

    p_pow = 1
    for i in range(m - 1):
        p_pow = (p_pow * p) % q

    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * p + ord(pattern[i]) - ord('a') + 1) % q
        window_hash = (window_hash * p + ord(text[i]) - ord('a') + 1) % q

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            match = True
            for j in range(m):
                if pattern[j] != text[i + j]:
                    match = False
                    break
            if match:
                indices.append(i)

        if i < n - m:
            window_hash = (window_hash - (ord(text[i]) - ord('a') + 1) * p_pow) % q
            window_hash = (window_hash * p + (ord(text[i + m]) - ord('a') + 1)) % q
            window_hash = (window_hash + q) % q

    return indices


text = 'abracadabra'
pattern = 'ab'
# check that your code works correctly on provided example
assert RabinKarp(text, pattern) == [0, 7], 'Wrong answer'
