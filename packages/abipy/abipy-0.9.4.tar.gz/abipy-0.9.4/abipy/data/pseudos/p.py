#!/usr/bin/env python

import sys
from abipy.ppcodes.oncv_parser import OncvParser

parser = OncvParser(sys.argv[1])
parser.scan()
print(parser)

# To plot data with matplotlib.
plotter = parser.get_plotter()
#plotter.plot_atanlogder_econv()



