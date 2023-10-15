import os

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

import glob

import corner
import h5py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from thesis_utils.gw import get_cbc_parameter_labels
from thesis_utils.plotting import set_plotting, save_figure

from utils import EVENTS, load_pe_summary_posterior_samples

sns.set_palette("colorblind")
set_plotting()

plt.rcParams["axes.grid"] = False


def make_chirp_mass_plot():
    samples = load_pe_summary_posterior_samples(
        "/home/michael.williams/git_repos/nessai-gwtc-1/comparison/gwtc-1/comparison/",
        EVENTS,
    )

    analyses = ["GWTC-1", "nessai-Pv2"]
    parameter = "chirp_mass"
    figure_name = "gwtc1_pv2_chirp_mass_comparison"

    df_data = {parameter: [], "analysis": [], "event": []}
    for event in EVENTS:
        for analysis in analyses:
            try:
                data = samples[event][analysis][parameter].tolist()
                df_data[parameter] += data
                df_data["analysis"] += len(data) * [analysis]
                df_data["event"] += len(data) * [event]
            except KeyError:
                print(f"Skipping: {event}")
                pass

    df = pd.DataFrame.from_dict(df_data)

    parameter = "chirp_mass"

    all_events = set(EVENTS)
    low_mass_events = {"GW151226", "GW170608"}
    high_mass_events = all_events - low_mass_events

    high_mass_idx = df["event"].isin(high_mass_events)
    low_mass_idx = df["event"].isin(low_mass_events)

    df_high_mass = df.copy()
    df_high_mass[parameter].loc[low_mass_idx] = np.nan
    df_low_mass = df.copy()
    df_low_mass[parameter].loc[high_mass_idx] = np.nan

    fig, axs = plt.subplots(
        2,
        1,
        sharex=True,
        gridspec_kw={
            "height_ratios": [1.5, 1],
            "hspace": 0.05,
        },
    )

    g1 = sns.violinplot(
        data=df_high_mass,
        x="event",
        y=parameter,
        hue="analysis",
        split=True,
        ax=axs[0],
        legend=False,
        inner=None,
    )

    g2 = sns.violinplot(
        data=df_low_mass,
        x="event",
        y=parameter,
        hue="analysis",
        split=True,
        ax=axs[1],
        legend=False,
        inner=None,
    )

    axs[0].set_ylabel(get_cbc_parameter_labels("chirp_mass", units=True))
    axs[1].set_ylabel(get_cbc_parameter_labels("chirp_mass", units=True))

    # axs[0].tick_params(axis='x', rotation=45, ha="right")
    axs[1].set_xticklabels(EVENTS, rotation=45, ha="right", rotation_mode="anchor")
    # axs[1].tick_params(axis='x', rotation=45)
    # axs[0].xaxis.set_ticks_position('both')
    axs[0].tick_params(axis="x", which="minor", bottom=False, top=False)
    axs[0].tick_params(axis="x", which="major", bottom=False, top=True)
    # axs[0].tick_params(labelbottom=False, labeltop=True)
    axs[1].tick_params(axis="x", which="minor", bottom=False, top=False)
    axs[1].tick_params(axis="x", which="major", bottom=True, top=False)

    axs[0].set(xlabel=None, ylabel=None)
    axs[1].set(xlabel=None, ylabel=None)

    handles, labels = axs[0].get_legend_handles_labels()
    axs[0].get_legend().remove()
    axs[1].get_legend().remove()
    axs[1].legend(
        handles=handles,
        labels=["GWTC-1", r"\texttt{nessai} - \texttt{IMRPhenomPv2}"],
        loc="lower right",
    )

    axs[0].spines["bottom"].set_visible(False)
    axs[1].spines["top"].set_visible(False)

    fig.text(
        0.04,
        0.5,
        get_cbc_parameter_labels(parameter, units=True),
        va="center",
        rotation="vertical",
    )

    d = 0.015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    # kwargs = dict(transform=axs[0].transAxes, color='k', clip_on=False)
    # axs[0].plot((1-d, 1+d), (-d, +d), **kwargs)
    # axs[0].plot((1-d, 1+d), (1-d, 1+d), **kwargs)

    # kwargs.update(transform=axs[1].transAxes)  # switch to the bottom axes
    # axs[1].plot((-d, +d), (1-d, 1+d), **kwargs)
    # axs[1].plot((-d, +d), (-d, +d), **kwargs)
    axs[1].set_ylim(8.2, 10.2)

    d = 0.5  # proportion of vertical to horizontal extent of the slanted line
    kwargs = dict(
        marker=[(-1, -d), (1, d)],
        markersize=10,
        linestyle="none",
        color="k",
        mec="k",
        mew=1,
        clip_on=False,
    )
    axs[0].plot([0, 1], [0, 0], transform=axs[0].transAxes, **kwargs)
    axs[1].plot([0, 1], [1, 1], transform=axs[1].transAxes, **kwargs)

    # plt.tight_layout()
    plt.show()
    # fig.savefig("figures/nessai_gwtc1_chirp_mass.png")
    save_figure(fig, figure_name, "figures/gwtc1")


if __name__ == "__main__":
    make_chirp_mass_plot()
