#!/usr/bin/env python
import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

import glob

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import seaborn as sns
import tqdm

from thesis_utils.plotting import get_default_corner_kwargs, get_default_figsize

import corner
import click

from thesis_utils.gw import get_cbc_parameter_labels
from thesis_utils.plotting import set_plotting, save_figure

from utils import ANALYSIS_LABELS, load_pe_summary_posterior_samples

set_plotting()

plt.rcParams["axes.grid"] = False


@click.command()
@click.option("--event", multiple=True)
@click.option("--analysis", multiple=True)
@click.option(
    "--label",
)
@click.option("--parameter", multiple=True)
def plot_event(event, analysis, label, parameter):
    print("Loading results")
    posterior_samples = load_pe_summary_posterior_samples(
        path="gwtc-1/comparison/",
        events=event,
    )

    for e in tqdm.tqdm(event):
        corner_data = {}
        for rtp in analysis:
            res = posterior_samples[e][rtp]
            array = np.array([res[p] for p in parameter]).T
            corner_data[rtp] = array

        corner_kwargs = get_default_corner_kwargs()
        corner_kwargs["plot_density"] = True
        corner_kwargs["plot_datapoints"] = False
        corner_kwargs["no_fill_contours"] = True
        corner_kwargs["show_titles"] = False
        corner_kwargs.pop("fill_contours")
        corner_kwargs["levels"] = (
            1 - np.exp(-0.5),
            1 - np.exp(-2),
            1 - np.exp(-9 / 2.0),
        )
        corner_kwargs["quantiles"] = []
        corner_kwargs["smooth"] = 0.9
        corner_kwargs["bins"] = 32
        corner_kwargs["labelpad"] = 0.1

        figsize = 2 * get_default_figsize()
        figsize[0] = figsize[1]
        fig = plt.figure(figsize=figsize)

        colours = ["k", "C0", "C1"]
        linestyles = ["--", "-", "-"]
        labels = get_cbc_parameter_labels(parameter, units=True)
        legend_elements = []
        for c, ls, (key, data) in zip(colours, linestyles, corner_data.items()):
            corner_kwargs["color"] = c
            corner_kwargs["hist_kwargs"]["color"] = c
            corner_kwargs["hist_kwargs"]["ls"] = ls
            corner_kwargs["contour_kwargs"] = dict(linestyles=[ls])
            fig = corner.corner(
                data,
                fig=fig,
                labels=labels,
                **corner_kwargs,
            )
            legend_elements.append(
                Line2D([0], [0], color=c, ls=ls, label=ANALYSIS_LABELS.get(key))
            )
        fig.legend(
            handles=legend_elements,
            bbox_to_anchor=(0.8, 0.8),
            loc="center",
            fontsize=16,
        )
        plt.show()
        save_figure(fig, f"{e}_{label}_comparison", f"figures/{e}")


if __name__ == "__main__":
    plot_event()
