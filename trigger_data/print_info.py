#!/usr/bin/env python
"""
Based on `tutorial.py` from: https://dcc.ligo.org/LIGO-P1900392/public

Michael J. Williams 2023
"""
import sys
import h5py


def main(fname):
    # print the properties of the most significant triggers
    print("Properties of most significant triggers in file {0}".format(fname))
    with h5py.File(fname, "r") as trigger_set:
        for i, far in enumerate(trigger_set["false_alarm_rate"]):
            # only consider triggers with false alarm rate < 1/year
            if far < 1.0:
                print("")
                print("Trigger number {0}:".format(i))
                # print all the properties of the found triggers
                for key in trigger_set.keys():
                    print("... {0}: {1}".format(key, trigger_set[key][i]))


if __name__ == "__main__":
    main(sys.argv[1])
