"""
PSO-ROTO classifier
"""

import sys
import re
from pprint import pprint
from collections import defaultdict
import json
import csv

__author__ = "Johan Forsberg"
__credits__ = ["Johan Forsberg", "Birger Scholz"]
__license__ = "GPL"
__version__ = "0.2"
__email__ = "johan@slentrian.org"
__status__ = "Prototype"


def classify(spec, data):
    """Uses the given specification to classify the given data."""
    positive = defaultdict(set)
    negative = defaultdict(set)
    for col in data:
        for regex, rule in spec.items():
            if re.match(regex + "$", col):
                for i, x in enumerate(data[col]):
                    try:
                        # Try to convert the value to a number
                        value = float(x)
                    except ValueError:  # Not a number; skip it
                        continue
                    for cond, items in rule.items():
                        try:
                            if cond == "null" or eval(cond, {"value": value,
                                                             "column": col}):
                                positive[i] |= set(map(tuple, (map(str, i)
                                                               for i in items)))
                            else:
                                negative[i] |= set(map(tuple, (map(str, i)
                                                               for i in items)))

                        except ValueError:
                            pass
    return map(list, positive.values()), map(list, negative.values())


# === Unit tests ===

TEST_SPEC = {
    "A": {
        "value == 1": [
            ("foo",)
            ],
        "int(value) == 2": [
            ("bar",)
            ],
        "3 <= value < 4": [
            ("baz",)
            ]
        },
    "B": {
        "value == 5": [
            ("foo",),
            ("bar",)
            ]
        }
    }

TEST_DATA = {
    "A": [1,    "2.4", 3.4],
    "B": ["5",    3,   5],
    "C": [3.14, "a", True]
    }


def test_classify():
    """Verify that the classifyer works."""
    test_result = classify(TEST_SPEC, TEST_DATA)
    assert sorted(test_result[0]) == sorted([("foo",), ("bar",)])
    assert sorted(test_result[1]) == sorted([("bar",)])
    assert sorted(test_result[2]) == sorted([("baz",), ("foo",), ("bar",)])


# Runs if the file is used as a script.
if __name__ == "__main__":

    # Do some unit testing
    test_classify()

    # Check arguments
    args = sys.argv[1:]
    if len(args) == 2:
        args.append(sys.stdout)
    try:
        spec_file, data_file, out_file = args
    except ValueError:
        sys.exit("Usage:\n  %s spec.json data.csv output.csv" % sys.argv[0])

    # Load specification
    spec = json.load(open(spec_file))

    # Load data
    with open(data_file, 'rb') as f:
        reader = csv.reader(f)
        rowdata = [row for row in reader]
    data = dict((name, [rowdata[j][i] for j in range(1, len(rowdata) - 2)])
                for i, name in enumerate(rowdata[0]))

    result = classify(spec, data)
    with out_file if isinstance(out_file, file) else open(out_file, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(result)
