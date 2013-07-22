"""
PSO-ROTO classifier
"""

import sys
import re
from pprint import pprint
from collections import defaultdict
from itertools import chain
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
                            s = set(tuple(it) for it in items)
                            if cond == "null" or eval(cond, {"value": value,
                                                             "column": col}):
                                positive[i] |= s
                                negative[i] -= s
                            else:
                                positive[i] -= s
                                negative[i] |= s
                        except ValueError:
                            pass
    return dict((i, (list(positive[i]), list(negative[i])))
                for i in set(positive.keys() + negative.keys()))


# === Unit tests ===

TEST_SPEC = {
    "A": {
        "value == 1": [
            ["foo"]
            ],
        "int(value) == 2": [
            ["bar"]
            ],
        "3 <= value < 4": [
            ["baz"]
            ]
        },
    "B": {
        "value == 5": [
            ["foobar"],
            ["barbaz"]
            ]
        }
    }

TEST_DATA = {
    "A": [1,    "2.4", 3.4],
    "B": ["5",    3,   5],
    "C": [3.14, "a", True]
    }


def _compare_results(res1, res2):
    for a1, a2 in zip(res1, res2):
        print "a1", a1, "a2", a2
        for row1, row2 in zip(a1, a2):
            print "row1", row1, "row2", row2
            for pos1, pos2 in zip(sorted(row1), sorted(row2)):
                print "pos1", pos1, "pos2", pos2
                for el1, el2 in zip(sorted(pos1), sorted(pos2)):
                    print "el1", el1, "el2", el2
                    assert el1 == el2


def test_classify():
    """Verify that the classifier works."""
    test_result = classify(TEST_SPEC, TEST_DATA)
    print test_result[0]
    _compare_results([test_result[0]], [([('foo',), ('foobar',), ('barbaz',)],
                                         [('bar',), ('baz',)])])
    # assert sorted(test_result[1]) == sorted([("bar",)])
    # assert sorted(test_result[2]) == sorted([("baz",), ("foo",), ("bar",)])


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
        sys.exit("Usage:\n  %s spec.json data.csv [output.json]" % sys.argv[0])

    # Load specification
    spec = json.load(open(spec_file))

    # Load data
    with open(data_file, 'rb') as f:
        reader = csv.reader(f)
        rowdata = [row for row in reader][:5]
    data = dict((name, [rowdata[j][i] for j in range(1, len(rowdata) - 2)])
                for i, name in enumerate(rowdata[0]))

    result = classify(spec, data)
    with out_file if isinstance(out_file, file) else open(out_file, 'wb') as f:
        f.write(json.dumps(result, indent=1,  # ensure_ascii=True,
                           sort_keys=True))
        # writer = csv.writer(f)
        # writer.writerows(result)
