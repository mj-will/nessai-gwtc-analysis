#!/usr/bin/env python
"""
Convert the ASD to a PSD.

Michael J. Williams 2023
"""
import os
import sys
import numpy as np


def main(filename) -> None:
    psd = np.genfromtxt(filename)
    psd[:, 1] = psd[:, 1] ** 2
    base, extension = os.path.splitext(filename)
    base = base.replace("asd", "psd")
    np.savetxt(base + extension, psd)


if __name__ == "__main__":
    main(sys.argv[1])
