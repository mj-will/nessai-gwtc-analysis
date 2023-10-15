"""Utilties for producing plots"""

import csv
import os
from typing import List

import h5py
import numpy as np
import pandas as pd
import tqdm

EVENTS = [
    "GW150914",
    "GW151012",
    "GW151226",
    "GW170104",
    "GW170608",
    "GW170729",
    "GW170809",
    "GW170814",
    "GW170818",
    "GW170823",
]

ANALYSIS_LABELS = {
    "GWTC-1": "GWTC-1",
    "GWTC-2": "GWTC-2.1",
    "nessai-Pv2": r"\texttt{nessai} - \texttt{Pv2}",
    "nessai-XP": r"\texttt{nessai} - \texttt{XP}",
    "nessai-XPHM": r"\texttt{nessai} - \texttt{XPHM}",
}


def load_pe_summary_posterior_samples(path: str, events: List[str]) -> dict:
    """Load the posterior samples produced by PE summary."""
    samples = {}
    for event in tqdm.tqdm(events):
        samples_path = os.path.join(path, event, "samples", "posterior_samples.h5")
        if not os.path.exists(samples_path):
            print(f"Skipping {event}")
            continue
        with h5py.File(samples_path, "r") as f:
            samples[event] = {}
            for key in f.keys():
                s = f[key].get("posterior_samples", None)
                if s is not None:
                    samples[event][key] = s[()]
    return samples


def get_min_n_samples(path: str, events: List[str], analyses: List[str]) -> dict:
    """Load the posterior samples produced by PE summary."""
    n_samples = {}
    for event in tqdm.tqdm(events):
        samples_path = os.path.join(path, event, "samples", "posterior_samples.h5")
        if not os.path.exists(samples_path):
            print(f"Skipping {event}")
            continue
        with h5py.File(samples_path, "r") as f:
            n = []
            for key in analyses:
                s = f[key].get("posterior_samples", None)
                if s is not None:
                    n.append(len(s))
            n_samples[event] = min(n)
    return n_samples


def load_js_data(path: str, filename: str, events: List[str]) -> dict:
    """Load JS data from PE summary csv files"""
    data = {}
    names = None
    for event in events:
        data_file = os.path.join(path, event, filename)
        event_data = {}
        if not os.path.isfile(data_file):
            data[event] = None
            continue
        parameter = None
        with open(data_file, "r") as file:
            reader = csv.reader(file)
            for i, row in enumerate(reader):
                if len(row) == 1:
                    if parameter is not None:
                        tmp_data = np.array(tmp_data)
                        event_data[parameter] = pd.DataFrame(
                            tmp_data[1:, 1:], columns=names, index=names
                        )
                    parameter = row[0]
                    event_data[parameter] = {}
                    tmp_data = []
                else:
                    if row[0] == "" and names is None:
                        names = row[1:]
                    tmp_data.append(row)
            if parameter is not None:
                event_data[parameter] = pd.DataFrame(
                    np.array(tmp_data)[1:, 1:], columns=names, index=names
                )

        event_data = {k: v for k, v in event_data.items() if len(v)}
        data[event] = event_data
    return data


def get_js_per_event(data: dict, analyses: List[str], parameters: List[str]) -> dict:
    """Get the JS grouped by event"""
    if len(analyses) != 2:
        raise RuntimeError
    js_per_event = {}
    for event in data:
        js_per_event[event] = []
        for key in parameters:
            if data[event] is None:
                js_per_event[event].append(np.nan)
                continue
            js_per_event[event].append(
                float(data[event][key][analyses[0]][analyses[1]])
            )
    return js_per_event


def get_js_per_parameter(
    data: dict, analyses: List[str], parameters: List[str]
) -> dict:
    """Get the JS grouped by parameter"""
    js_per_event = get_js_per_event(data, analyses, parameters)
    jsds_array = np.array([js for js in js_per_event.values()])
    js_per_parameter = {k: js for k, js in zip(parameters, jsds_array.T)}
    return js_per_parameter
