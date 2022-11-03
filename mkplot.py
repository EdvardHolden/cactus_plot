#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# mkplot.py
#
#  Created on: Jan 31, 2014
#      Author: Alexey S. Ignatiev
#      E-mail: aignatiev@ciencias.ulisboa.pt
#

#
# ==============================================================================
from __future__ import print_function
import matplotlib

matplotlib.use("pdf")  # for not loading GUI modules

from cactus import Cactus
from load import load_data
from scatter import Scatter


#
# ==============================================================================

import argparse


def get_parser():

    parser = argparse.ArgumentParser()

    parser.add_argument("data", nargs="+", help="Path to the json data files")

    parser.add_argument(
        "--def_path",
        default="defaults.json",
        help="Config file for loading the other paramters. Slightly strange...",
    )

    parser.add_argument(
        "-a",
        "--alpha",
        type=float,
        default=0.3,
        help='Alpha value (only for scatter plots)") Available values: [0 .. 1]',
    )
    parser.add_argument(
        "-b",
        "--backend",
        type=str,
        default="png",
        choices=["pdf", "pgf", "png", "ps", "svg"],
        help=" Backend to use (file output format?)",
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Do not create a plot but instead show the tools sorted in the terminal",
    )
    parser.add_argument(
        "-f",
        "--font",
        choices=["cmr", "helvetica", "palantino", "times"],
        default="times",
        help="Font to use",
    )
    parser.add_argument("--font-sz", type=int, default=12, help="Font size to use")
    parser.add_argument("--grid_color", default="black", help="The colour of the grid")
    parser.add_argument("--grid_style", default=":", help="The grid style")
    parser.add_argument("--grid_width", default="1", help="The grid width")
    parser.add_argument("--no-grid", action="store_true", help="Do not show the grid")
    parser.add_argument(
        "-j",
        "--join-key",
        nargs="*",
        default=None,
        help="Comma-separated list of keys to join all benchmarks per each tool",
    )
    parser.add_argument("-k", "--key", type=str, default="rtime", help=" Key to measure")
    parser.add_argument("-l", "--usetex", action="store_true", help="Use latex")

    parser.add_argument(
        "--lgd_alpha", type=float, default=1.0, help="Legend transparency level [0.0, ... ,0.1]"
    )
    parser.add_argument(
        "--legend",
        nargs="+",
        default="proram",
        help="Comma-separated list of keys to use in the legend of a plot) Format: program,prog_args",
    )
    parser.add_argument("lgd_fancy", action="store_true", help="Make the legend fancy??`")
    parser.add_argument("lgd_shadow", action="store_true", help="Make the legend shadowy??")
    parser.add_argument(
        "--lgd_loc",
        type=str,
        default="upper left",
        help="Legend location. Available values: upper/center/lower left/right, center, best, off",
    )
    parser.add_argument("--lgd_ncol", type=int, default=1, help="Number of columns in the legend")

    parser.add_argument(
        "-n", "--by_name", action="store_true", help="Assign line style to tools by their name"
    )
    parser.add_argument("--only", nargs="*", default=None, help="Comma-separated list of names")
    parser.add_argument(
        "-p",
        "--plot-type",
        type=str,
        choices=["cactus", "scatter"],
        default="cactus",
        help="Plot type to produce",
    )
    parser.add_argument(
        "-r", "--replace", type=str, default=None, help="List of name replacements"
    )  # Format: {"name1": "$nice_name1$", "name2": "$nice_name2$"}
    parser.add_argument("--reverse", action="store_true", help="Use reversed sorting")
    parser.add_argument("--save-to", type=str, default="plot", help="Where result figure should be saved")
    parser.add_argument(
        "--shape",
        type=str,
        default="standard",
        choices=["long", "squared", "standard"],
        help="Shape of the plot",
    )
    parser.add_argument("-t", "--timeout", type=int, default=305, help="Timeout value")
    parser.add_argument("--t_label", type=str, help="Timeout label (for scatter plots only)")
    parser.add_argument(
        "--tol_loc",
        type=str,
        default="after",
        choices=["before", "after"],
        help="Where to put the timeout label",
    )
    parser.add_argument("--transparent", action="store_true", help="Save the file in the transparent mode")
    parser.add_argument(
        "--vbs", type=str, default=None, help="List of VBSes"
    )  # Format: {"vbs1": ["tool1", "tool2"], "vbs2": "all"}
    parser.add_argument("--xkcd", action="store_true", help="Use xkcd-style sketch plotting")

    parser.add_argument("--x_label", type=str, help="X label")
    parser.add_argument("--x_log", action="store_true", help="Use logarithmic scale for X axis")
    parser.add_argument("--x_max", type=int, default=None, help="X axis ends at this value")
    parser.add_argument("--x_min", type=int, default=0, help="X axis starts from this value")
    parser.add_argument("--y_label", type=str, help="Y label")
    parser.add_argument("--y_log", action="store_true", help="Use logarithmic scale for Y axis")
    parser.add_argument("--y_max", type=int, default=None, help="Y axis ends at this value")
    parser.add_argument("--y_min", type=int, default=0, help="Y axis starts from this value")

    return parser


#
# ==============================================================================
def main():

    parser = get_parser()
    args = parser.parse_args()
    args = vars(args)  # Use dict style

    # Load the data
    data = load_data(args["data"], args)

    # Check if computing stats or plotting
    if args["dry_run"]:
        for d in data:
            d1 = list(map(lambda x: min(x, args["timeout"]), d[1]))

            print("{0}:".format(d[0]))
            print("    # solved: {0}".format(d[2]))
            print("    min. val: {0:.1f}".format(float(min(d1))))
            print("    max. val: {0:.1f}".format(float(max(d1))))
            print("    avg. val: {0:.1f}".format(float(sum(d1)) / len(d1)))
    else:
        # Initialise plotting style
        if args["plot_type"] == "cactus":
            plotter = Cactus(args)
        else:
            plotter = Scatter(args)

        # Create the plot
        plotter.create(data)


if __name__ == "__main__":
    main()
