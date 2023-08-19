#!/usr/bin/env python
"""
Script to analyze performance
"""
from __future__ import annotations

import sys
import os
import argparse
import subprocess
import abipy.tools.cli_parsers as cli

from pprint import pprint
from shutil import which
from monty.termcolor import cprint
from monty.functools import prof_main
from abipy import abilab


def get_epilog() -> str:
    s = """\
======================================================================================================
Usage example:

    abiopen.py FILE          => Open file in ipython shell.

======================================================================================================

"""
    return s


def get_parser(with_epilog=False):
    parser = argparse.ArgumentParser(epilog=get_epilog() if with_epilog else "",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('--loglevel', default="ERROR", type=str,
        help="Set the loglevel. Possible values: CRITICAL, ERROR (default), WARNING, INFO, DEBUG")
    parser.add_argument('-V', '--version', action='version', version=abilab.__version__)

    parser.add_argument('-v', '--verbose', default=0, action='count', # -vv --> verbose=2
        help='verbose, can be supplied multiple times to increase verbosity')

    parser.add_argument("filepath", help="File to open. See table below for the list of supported extensions.")

    # notebook options.
    #parser.add_argument('-nb', '--notebook', action='store_true', default=False, help="Open file in jupyter notebook")
    #parser.add_argument('--classic-notebook', "-cnb", action='store_true', default=False,
    #                    help="Use classic jupyter notebook instead of jupyterlab.")
    #parser.add_argument('--no-browser', action='store_true', default=False,
    #                    help=("Start the jupyter server to serve the notebook "
    #                          "but don't open the notebook in the browser.\n"
    #                          "Use this option to connect remotely from localhost to the machine running the kernel"))
    #parser.add_argument('--foreground', action='store_true', default=False,
    #                    help="Run jupyter notebook in the foreground.")

    # Expose option.
    #parser.add_argument('-e', '--expose', action='store_true', default=False,
    #    help="Open file and generate matplotlib figures automatically by calling expose method.")
    #parser.add_argument("-s", "--slide-mode", default=False, action="store_true",
    #    help="Iterate over figures. Expose all figures at once if not given on the CLI.")
    #parser.add_argument("-t", "--slide-timeout", type=int, default=None,
    #    help="Close figure after slide-timeout seconds (only if slide-mode). Block if not specified.")
    #parser.add_argument('-sns', "--seaborn", const="paper", default=None, action='store', nargs='?', type=str,
    #    help='Use seaborn settings. Accept value defining context in ("paper", "notebook", "talk", "poster").')
    #parser.add_argument('-mpl', "--mpl-backend", default=None,
    #    help=("Set matplotlib interactive backend. "
    #          "Possible values: GTKAgg, GTK3Agg, GTK, GTKCairo, GTK3Cairo, WXAgg, WX, TkAgg, Qt4Agg, Qt5Agg, macosx."
    #          "See also: https://matplotlib.org/faq/usage_faq.html#what-is-a-backend."))
    #parser.add_argument("-ew", "--expose-web", default=False, action="store_true",
    #        help='Generate matplotlib plots in $BROWSER instead of X-server. WARNING: Not all the features are supported.')
    #parser.add_argument("-ply", "--plotly", default=False, action="store_true",
    #        help='Generate plotly plots in $BROWSER instead of matplotlib. WARNING: Not all the features are supported.')

    return parser


@prof_main
def main():
    def show_examples_and_exit(err_msg=None, error_code=1):
        """Display the usage of the script."""
        sys.stderr.write(get_epilog())
        if err_msg:
            sys.stderr.write("Fatal Error\n" + err_msg + "\n")
        sys.exit(error_code)

    parser = get_parser(with_epilog=True)

    # Parse the command line.
    try:
        options = parser.parse_args()
    except Exception:
        show_examples_and_exit(error_code=1)

    cli.set_loglevel(options.loglevel)

    ##############################################################################################
    # Handle meta options i.e. options that set other options.
    # OK, it's not very clean but I haven't find any parse API to express this kind of dependency.
    ##############################################################################################
    if options.plotly: options.expose = True
    if options.expose_web: options.expose = True

    if options.verbose > 2: print(options)

    # Set matplotlib backend
    if options.mpl_backend is not None:
        import matplotlib
        matplotlib.use(options.mpl_backend)

    # Use seaborn settings.
    if options.seaborn:
        import seaborn as sns
        sns.set(context=options.seaborn, style='darkgrid', palette='deep',
                font='sans-serif', font_scale=1, color_codes=False, rc=None)

    if not os.path.exists(options.filepath):
        raise RuntimeError("%s: no such file" % options.filepath)


if __name__ == "__main__":
    sys.exit(main())
