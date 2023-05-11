from bisect import bisect_left


class Utils:
    @staticmethod
    def binary_search(list, value, key):
        i = bisect_left(list, value, key=key)
        if i != len(list) and list[i] == value:
            return i
        else:
            return -1
