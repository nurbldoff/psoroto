import sys
from collections import defaultdict
from pprint import pprint
import json
#import yaml
import pandas


def xml_to_specs(specs):

    """Translate some of Birger's Excel spec into Python data."""

    results = defaultdict(dict)
    for i, spec in specs.T.iteritems():
        ann = spec[1]
        ids = cond = match = None
        if ann is not None:
            if ann.startswith("VMF"):
                if ann[3] == "X":             # all VMF scores
                    match = "[A-R]"
                    cond = None
                elif ann[3] == "A":           # all VMFA scores
                    if ann[4] == "X":
                        match = "A"
                        cond = None
                    else:
                        match = "A"
                        cond = "int(value) == %d" % int(ann[4])
            elif ann.startswith("MF"):
                match = "Mal" + ann[2]
                cond = "int(value) == %d" % int(ann[2])

            if match:
                ids = tuple(spec[8:11])
                if cond in results[match]:
                    results[match][cond].add(ids)
                else:
                    results[match][cond] = set((ids,))

    return dict((m, dict((c, list(i)) for c, i in a.items()))
                for m, a in results.items())


if __name__ == "__main__":

    try:
        xls_file = sys.argv[1]
        out_file = sys.argv[2]
    except IndexError:
        sys.exit("You need to give two arguments: " +
                 "an XLS file and an output file.")

    xls = pandas.ExcelFile(xls_file)
    xls_specs = xls.parse('PSO-ROTO specifications', skiprows=2, header=0,
                          index_col=None, na_values=['NA'])

    f = open(out_file, "w")

    specs = xml_to_specs(xls_specs)
    pprint(specs)
    #yaml.safe_dump(specs, f)
    json.dump(specs, f, indent=4)
