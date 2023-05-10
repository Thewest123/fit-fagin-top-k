import csv
import numpy as np

from src.Mouse import Mouse


class Database:
    # ------------ [Private variables] ------------
    __data = []
    __data_header = []
    __data_normalized = []

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

        self.__normalize(self.__sorted_by_weight, reverse=True)
        self.__normalize(self.__sorted_by_accuracy)
        self.__normalize(self.__sorted_by_dpi)
        self.__normalize(self.__sorted_by_price, reverse=True)

        for mouse in self.__data:
            normalized_mouse = mouse

            normalized_mouse.assign_normalized(
                mouse.name,
                self.__get_normalized_value(mouse, self.__sorted_by_weight),
                self.__get_normalized_value(mouse, self.__sorted_by_accuracy),
                self.__get_normalized_value(mouse, self.__sorted_by_dpi),
                self.__get_normalized_value(mouse, self.__sorted_by_price),
            )

            self.__data_normalized.append(normalized_mouse)

    def __get_normalized_value(self, value, list: list[tuple]) -> float:
        # Find value in list
        for i in range(len(list)):
            if list[i][1] == value:
                return list[i][0]

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

    def __normalize(self, list: list[tuple], reverse=False):
        minimum = min(list, key=lambda x: x[0])[0]
        maximum = max(list, key=lambda x: x[0])[0]

        for i in range(len(list)):
            before = list[i][0]
            try:
                if reverse:
                    list[i] = self.__update_tuple(list[i], 0, (maximum - before) / (maximum - minimum))
                else:
                    list[i] = self.__update_tuple(list[i], 0, (before - minimum) / (maximum - minimum))
            except ZeroDivisionError:
                # If all values are the same, set normalized value to 0.5
                list[i] = self.__update_tuple(list[i], 0, 0.5)

            # print(f"Normalized {before} to {list[i][0]}")

    def __sort_lists(self):
        # Sort lists by 0th column in tuple
        self.__sorted_by_name.sort(key=lambda x: x[0])
        self.__sorted_by_weight.sort(key=lambda x: x[0])
        self.__sorted_by_accuracy.sort(key=lambda x: x[0], reverse=True)
        self.__sorted_by_dpi.sort(key=lambda x: x[0], reverse=True)
        self.__sorted_by_price.sort(key=lambda x: x[0])

    def __update_tuple(self, tuple: tuple, index: int, value):
        return tuple[:index] + (value,) + tuple[index + 1 :]

    # ------------ [Public methods] ------------

    def get_header(self):
        return self.__data_header

    def get_data(self):
        return self.__data

    def get_data_normalized(self):
        return self.__data_normalized

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

    def get_sorted_price_mouse_only(self):
        mousecol = [mouse for price, mouse in self.__sorted_by_price]

        # Convert Mouse objects to list of dicts
        data = []
        for mouse in mousecol:
            data.append(mouse.as_list())

        return {
            "data": data,
            "headers": self.__data_header,
        }
