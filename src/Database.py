import csv
import numpy as np
import gradio as gr
import os

from src.Mouse import Mouse
from src.Utils import Utils


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

    # ------------ [Private methods] ------------
    def __init__(self, csv_path, progress):
        self.__progress_value = 0
        self.__progress_max = 10
        self.__progress = progress

        print("Reading CSV file...")
        self.__read_csv(csv_path)

        self.__progress_value = 1
        self.__progress_max = 10

        print("Sorting lists...")
        self.__sort_lists()

        print("Normalizing lists...")
        self.__normalize(self.__sorted_by_weight, "weight", reverse=True)
        self.__normalize(self.__sorted_by_accuracy, "accuracy")
        self.__normalize(self.__sorted_by_dpi, "dpi")
        self.__normalize(self.__sorted_by_price, "price", reverse=True)

        progress((self.__progress_value, self.__progress_max), "Database loaded!")

        print("Database loaded!")

        self.__data_normalized = self.__data

    def __read_csv(self, csv_path):
        self.__data = []
        self.__data_header = []

        file_size = os.path.getsize(csv_path)
        LINE_SIZE = 30
        estimated_line_count = file_size / LINE_SIZE
        print(f"Estimated line count: {estimated_line_count}")

        self.__progress_max = estimated_line_count

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

                self.__progress_value += 1
                self.__progress((self.__progress_value, self.__progress_max), f"Reading CSV file...")

    def as_dict(self):
        # Return dict with key `data` and `headers`
        return {
            "data": self.__data,
            "headers": self.__data_header,
        }

    def __normalize(self, list: list[tuple], attribute: str, reverse=False):
        minimum = min(list, key=lambda x: x[0])[0]
        maximum = max(list, key=lambda x: x[0])[0]
        attribute = attribute + "_normalized"

        self.__progress((self.__progress_value, self.__progress_max), f"Normalizing {attribute}...")
        self.__progress_value += 1

        for i in range(len(list)):
            before = list[i][0]
            try:
                if reverse:
                    list[i] = self.__update_tuple(list[i], 0, (maximum - before) / (maximum - minimum))
                    setattr(list[i][1], attribute, (maximum - before) / (maximum - minimum))
                else:
                    list[i] = self.__update_tuple(list[i], 0, (before - minimum) / (maximum - minimum))
                    setattr(list[i][1], attribute, (before - minimum) / (maximum - minimum))
            except ZeroDivisionError:
                # If all values are the same, set normalized value to 0.5
                list[i] = self.__update_tuple(list[i], 0, 0.5)
                setattr(list[i][1], attribute, 0.5)

            setattr(list[i][1], "name_normalized", list[i][1].name)

            # print(f"Normalized {before} to {list[i][0]}")

    def __sort_lists(self):
        # Sort lists by 0th column in tuple

        self.__progress((self.__progress_value, self.__progress_max), "Sorting lists by name...")
        self.__progress_value += 1
        self.__sorted_by_name.sort(key=lambda x: x[0])

        self.__progress((self.__progress_value, self.__progress_max), "Sorting lists by weight...")
        self.__progress_value += 1
        self.__sorted_by_weight.sort(key=lambda x: x[0])

        self.__progress((self.__progress_value, self.__progress_max), "Sorting lists by accuracy...")
        self.__progress_value += 1
        self.__sorted_by_accuracy.sort(key=lambda x: x[0], reverse=True)

        self.__progress((self.__progress_value, self.__progress_max), "Sorting lists by dpi...")
        self.__progress_value += 1
        self.__sorted_by_dpi.sort(key=lambda x: x[0], reverse=True)

        self.__progress((self.__progress_value, self.__progress_max), "Sorting lists by price...")
        self.__progress_value += 1
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
