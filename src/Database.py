import csv


class Database:
    # Static variables
    __data = []
    __data_header = []

    def __init__(self, csv_path):
        self.__data = self.read_csv(csv_path)

    def read_csv(self, csv_path):
        with open(csv_path, newline="") as csvfile:
            reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC)

            for row in reader:
                # Read header
                if not self.__data_header:
                    self.__data_header = row
                    continue

                self.__data.append(row)
                print(row)

        return self.__data

    def as_dict(self):
        # Return dict with key `data` and `headers`
        return {
            "data": self.__data,
            "headers": self.__data_header,
        }
