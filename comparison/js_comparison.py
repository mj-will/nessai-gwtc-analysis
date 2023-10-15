#!/usr/bin/env python
# coding: utf-8

import click
import pandas as pd
import csv
import itertools
import os
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.lines import Line2D
import importlib

from thesis_utils.plotting import set_plotting, get_default_figsize, save_figure
from thesis_utils.gw import get_cbc_parameter_labels

import utils

importlib.reload(utils)
from utils import (
    EVENTS,
    get_min_n_samples,
    load_js_data,
    get_js_per_event,
    get_js_per_parameter,
)
from utils import ANALYSIS_LABELS as analysis_labels

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

set_plotting()


@click.command()
@click.option("--catalogue")
def make_js_plot(catalogue):
    if catalogue == "GWTC-1":
        analyses = ["GWTC-1", "nessai-Pv2", "nessai-XP"]
        focus = ["GWTC-1", "nessai-Pv2"]
        filename = "js_comparison_gwtc1"
    elif catalogue == "GWTC-2.1":
        analyses = ["GWTC-2", "nessai-XPHM", "nessai-XP"]
        focus = ["GWTC-2", "nessai-XPHM"]
        filename = "js_comparison_gwtc2p1"

    else:
        raise ValueError(catalogue)

    n_samples = get_min_n_samples(
        "/home/michael.williams/git_repos/nessai-gwtc-1/comparison/gwtc-1/comparison/",
        EVENTS,
        analyses,
    )

    # In[7]:

    data = load_js_data(
        "js_data",
        "JS_test_total_XPHM.csv",
        EVENTS,
    )

    # In[8]:

    parameters_to_plot = [
        "chirp_mass",
        "mass_ratio",
        # "mass_1",
        # "mass_2",
        # "a_1",
        # "a_2",
        # "tilt_1",
        # "tilt_2",
        "chi_eff",
        "chi_p",
        "ra",
        "dec",
        "theta_jn",
        "luminosity_distance",
    ]

    # In[9]:

    js_per_event = get_js_per_event(
        data,
        focus,
        parameters=parameters_to_plot,
    )
    js_per_parameter = get_js_per_parameter(
        data,
        focus,
        parameters=parameters_to_plot,
    )

    factor = np.log2(np.e)

    mean_js_per_event = {e: np.nanmean(js) for e, js in js_per_event.items()}
    min_event = min(mean_js_per_event, key=mean_js_per_event.get)
    max_event = max(mean_js_per_event, key=mean_js_per_event.get)
    print(f"Event with lowest median JSD: {min_event}")
    print(f"Event with highest median JSD: {max_event}")

    mean_js_per_param = {p: np.nanmean(js) for p, js in js_per_parameter.items()}
    min_param = min(mean_js_per_param, key=mean_js_per_param.get)
    max_param = max(mean_js_per_param, key=mean_js_per_param.get)
    print(f"Parameter with lowest mean JSD: {min_param}")
    print(f"JSD={min(mean_js_per_param.values()) * factor}")
    print(f"Parameter with highest mean JSD: {max_param}")
    print(f"JSD={max(mean_js_per_param.values()) * factor}")

    # In[13]:

    print(f"Mean overall JSD (bits): {np.mean(list(js_per_event.values())) * factor}")

    # In[ ]:

    parameters_to_plot, np.array(js_per_event["GW170814"]) * factor, mean_js_per_event[
        "GW170814"
    ] * factor

    # In[ ]:

    mean_js_per_param["chi_p"] * factor

    # In[ ]:

    comb = list(itertools.combinations(analyses, 2))
    print(comb)
    colours = sns.color_palette("colorblind", n_colors=len(comb))
    markers = ["^", ".", "x", "*", "^", "x"]

    xticklabels = get_cbc_parameter_labels(parameters_to_plot, units=False)

    legend_elements = []
    for pair, colour, marker in zip(comb, colours, markers):
        label = f"{analysis_labels.get(pair[0])} vs {analysis_labels.get(pair[1])}"
        legend_elements.append(
            Line2D([0], [0], color=colour, marker=marker, label=label, ls="None")
        )

    # In[11]:

    mean_n_samples = np.mean(list(n_samples.values()))
    mean_threshold = np.mean(10 / np.array(list(n_samples.values())))

    print(f"Mean n samples: {mean_n_samples}")
    print(f"Mean threshold: {mean_threshold}")

    n_events = len(EVENTS)
    figsize = get_default_figsize()
    figsize[1] *= 2
    fig, axs = plt.subplots(n_events // 2, 2, sharey=True, figsize=figsize)
    axs = axs.ravel()
    jsd = dict()
    xticks = np.arange(len(parameters_to_plot))
    count = 0
    for (event, event_data), ax in zip(data.items(), axs):
        jsd[event] = {}
        ax.set_xticks(xticks)
        ax.set_xticklabels(xticklabels)
        ax.set_yscale("log")
        # ax.legend(handles=legend_elements)
        if (count % 2) == 0:
            ax.set_ylabel(r"$D_{JS}\;[\textrm{bits}]$")
        ax.set_title(
            f"{event}: mean "
            + r"$D_{JS}="
            + f"{factor * mean_js_per_event[event]:.3f}"
            + r"$",
            x=-0.0,
            loc="left",
        )
        ax.tick_params(axis="x", which="minor", bottom=False, top=False)
        ax.tick_params(axis="y", which="minor", left=True, right=True)

        count += 1
        if event_data is None:
            continue

        threshold = 10 / n_samples[event]
        ax.axhline(threshold, color="grey", zorder=-1)
        offsets = np.linspace(-0.2, 0.2, 6, endpoint=True)
        offsets = np.zeros(6)
        for i, key in enumerate(parameters_to_plot):
            js = event_data.get(key, None)
            if js is None:
                print(f"Missing {key} for {event}")
                continue
            for (
                j,
                (a, b),
            ) in enumerate(comb):
                value = np.log2(np.e) * float(js[a][b])
                ax.scatter(i + offsets[j], value, marker=markers[j], color=colours[j])

    ax.set_yticks([1e-4, 1e-3, 1e-2, 1e-1])

    fig.legend(
        handles=legend_elements, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.05)
    )
    plt.tight_layout()
    plt.show()
    save_figure(fig, filename, "figures/js_comparison/")


if __name__ == "__main__":
    make_js_plot()
