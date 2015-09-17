__author__ = 'anton.sorokoumov'


def find_between(string, first, last):
    try:
        start = string.rindex(first) + len(first)
        end = string.rindex(last, start)
        return string[start:end]
    except ValueError:
        return ""
