import re


def problem_1():
    return re.compile(r'(−|-)?\d+(\.\d+)*(\.\d+(e\d+)?)?')


def problem_2():
    return re.compile(r'(?<![.−])\b\d+(\.\d+)?')


def problem_3():
    return re.compile(r'([0-1][0-9]|[2][0-3]|[1-9]):([0-5][0-9])')


def problem_4():
    return re.compile(r'([1-9][0-9]?[0-9]?[0-9]?-(0[1-9]|1[0-2])-([1-2][0-9]|0[1-9]|3[0-1]))')


def problem_5():
    return re.compile(r'\b[a-zA-Z0-9]{3,16}\b')


def problem_6():
    return re.compile(r'([\w\.\-]+)@([\w\-]+)((\.(\w){2,3})+)')


def problem_7():
    return re.compile(r'((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)')


def problem_8():
    return re.compile(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
