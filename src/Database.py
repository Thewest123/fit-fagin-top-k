import csv
import numpy as np

from src.Mouse import Mouse


class Database:
    # ------------ [Private variables] ------------
    __data = []
    __data_header = []

    __sorted_by_name = []
    __sorted_by_weight = []
    __sorted_by_accuracy = []
    __sorted_by_dpi = []
    __sorted_by_price = []

    # ------------ [Public variables] ------------

    # ------------ [Private methods] ------------
    def __init__(self, csv_path):
        self.__read_csv(csv_path)
        self.__sort_lists()

        self.__normalize(self.__sorted_by_weight)
        self.__normalize(self.__sorted_by_accuracy)
        self.__normalize(self.__sorted_by_dpi)
        self.__normalize(self.__sorted_by_price)

    def __read_csv(self, csv_path):
        self.__data = []
        self.__data_header = []

        with open(csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)

            for row in reader:
                # Read header
                if not self.__data_header:
                    self.__data_header = row
                    continue

                mouse = Mouse()
                mouse.assign(row[0], row[1], row[2], row[3], row[4])

                self.__data.append(mouse)

                self.__sorted_by_name.append((mouse.name, mouse))
                self.__sorted_by_weight.append((mouse.weight, mouse))
                self.__sorted_by_accuracy.append((mouse.accuracy, mouse))
                self.__sorted_by_dpi.append((mouse.dpi, mouse))
                self.__sorted_by_price.append((mouse.price, mouse))

    def as_dict(self):
        # Return dict with key `data` and `headers`
        return {
            "data": self.__data,
            "headers": self.__data_header,
        }

    def __normalize(self, list: list[tuple]):
        minimum = min(list, key=lambda x: x[0])[0]
        maximum = max(list, key=lambda x: x[0])[0]

        for i in range(len(list)):
            before = list[i][0]
            try:
                list[i] = self.__update_tuple(list[i], 0, (before - minimum) / (maximum - minimum))
            except ZeroDivisionError:
                pass

            # print(f"Normalized {before} to {list[i][0]}")

    def __sort_lists(self):
        # Sort lists by 0th column in tuple
        self.__sorted_by_name.sort(key=lambda x: x[0])
        self.__sorted_by_weight.sort(reverse=True, key=lambda x: x[0])
        self.__sorted_by_accuracy.sort(reverse=True, key=lambda x: x[0])
        self.__sorted_by_dpi.sort(reverse=True, key=lambda x: x[0])
        self.__sorted_by_price.sort(reverse=True, key=lambda x: x[0])

    def __update_tuple(self, tuple: tuple, index: int, value):
        return tuple[:index] + (value,) + tuple[index + 1 :]

    # ------------ [Public methods] ------------

    def get_header(self):
        return self.__data_header

    def get_data(self):
        return self.__data

    def get_sorted_name(self):
        return self.__sorted_by_name

    def get_sorted_weight(self):
        return self.__sorted_by_weight

    def get_sorted_accuracy(self):
        return self.__sorted_by_accuracy

    def get_sorted_dpi(self):
        return self.__sorted_by_dpi

    def get_sorted_price(self):
        return self.__sorted_by_price
