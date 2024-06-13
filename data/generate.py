# Generate random CSV data for testing

import csv
import random
import string
import sys

if len(sys.argv) < 2:
    print("Usage: python generate.py <size>")
    exit(1)

size = int(sys.argv[1])
path = "./data/test.random.csv"

with open(path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=",", quotechar='"')

    writer.writerow(["name", "weight", "accuracy", "dpi", "price"])

    for i in range(size):
        writer.writerow(
            [
                "".join(random.choices(string.ascii_letters, k=10)),
                random.randint(1, 1000),
                random.randint(1, 1000),
                float(random.randint(1, 1000)),
                random.randint(1, 1000),
            ]
        )
