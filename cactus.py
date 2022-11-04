import json
import matplotlib.pyplot as plt
from matplotlib import __version__ as mpl_version
import math
import numpy as np
from typing import List

from load_data import Program
from plot import Plot


class Cactus(Plot, object):
    """
    Cactus plot class.
    """

    def __init__(self, options):
        """
        Cactus constructor.
        """

        super(Cactus, self).__init__(options)

        with open(self.def_path, "r") as fp:
            self.linestyles = json.load(fp)["cactus_linestyle"]

    def create(self, data: List[Program]):
        """
        Does the plotting.
        """

        # Make x and y line plot from the data
        coords = []
        for prog in data:
            coords.append(np.arange(1, len(prog) + 1))  # xs (separate for each line)
            coords.append(np.array(sorted(prog.get_values())))
        lines = plt.plot(*coords, zorder=3)

        # setting line styles
        if not self.byname:  # by default, assign fist line to best tool
            lmap = lambda i: i
        else:  # assign line styles by tool name
            tnames = [(prog.get_alias(), i) for i, prog in enumerate(data)]
            tnames.sort(key=lambda pair: pair[0])
            tmap = {tn[1]: i for i, tn in enumerate(tnames)}
            lmap = lambda i: tmap[i]

        # Set the line-styles
        for i, l in enumerate(lines):
            plt.setp(l, **self.linestyles[lmap(i) % len(self.linestyles)])

        # Turning the grid on
        if not self.no_grid:
            plt.grid(True, color=self.grid_color, ls=self.grid_style, lw=self.grid_width, zorder=1)

        #  Compute the x-axis limit
        if self.x_max:
            x_max = self.x_max
        else:
            # Make sure that the last values are not crammed in the corner
            x_max = math.ceil(max([len(prog) for prog in data]) / float(100)) * 100

        # Set the axis limits
        plt.xlim(self.x_min, x_max)
        plt.ylim(self.y_min, self.y_max if self.y_max else self.timeout)

        # axes labels
        if self.x_label:
            plt.xlabel(self.x_label)
        else:
            plt.xlabel("instances")

        if self.y_label:
            plt.ylabel(self.y_label)
        else:
            plt.ylabel("CPU time (s)")

        # choosing logarithmic scales if needed
        ax = plt.gca()
        if self.x_log:
            ax.set_xscale("log")
        if self.y_log:
            ax.set_yscale("log")

        if float(mpl_version[:3]) < 1.5:
            ax.set_xticklabels(ax.get_xticks(), self.f_props)
            ax.set_yticklabels(ax.get_yticks(), self.f_props)

        strFormatter = plt.FormatStrFormatter("%d")
        logFormatter = plt.LogFormatterMathtext(base=10)
        ax.xaxis.set_major_formatter(strFormatter if not self.x_log else logFormatter)
        ax.yaxis.set_major_formatter(strFormatter if not self.y_log else logFormatter)

        # Making the legend
        if self.lgd_loc != "off":
            lgtext = [prog.get_alias() for prog in data]
            lg = ax.legend(
                lines,
                lgtext,
                ncol=self.lgd_ncol,
                loc=self.lgd_loc,
                fancybox=self.lgd_fancy,
                shadow=self.lgd_shadow if self.lgd_alpha == 1.0 else False,
            )
            fr = lg.get_frame()
            fr.set_lw(1)
            fr.set_alpha(self.lgd_alpha)
            fr.set_edgecolor("black")

        # Setting frame thickness
        for axis in ["top", "bottom", "left", "right"]:
            ax.spines[axis].set_linewidth(1)

        plt.savefig(self.save_to, bbox_inches="tight", transparent=self.transparent)
        print("Saved to:", self.save_to)
