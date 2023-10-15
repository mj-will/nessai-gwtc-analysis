#!/usr/bin/env python
import argparse
import ast
import glob
import json
from natsort import natsorted
import os
import re
import shutil


BASE_PATH = "/home/daniel.williams/events/O3/event_repos/"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("events", nargs="+", type=str)
    parser.add_argument("--prod", type=str, default=None)
    return parser.parse_args()


def main():
    waveform = "IMRPhenomXPHM"
    sampler_kwargs = r"{'nlive': 1000, 'flow_class': 'gwflowproposal', 'constant_volume_mode': True, 'volume_fraction': 0.98, 'analytic_priors': True, 'flow_config': {'model_config': {'n_blocks': 6, 'n_neurons': 32}}, 'fallback_reparameterisation': 'z-score', 'reparameterisations': {'mass_ratio': 'mass', 'a_1': 'to-cartesian', 'a_2': 'to-cartesian'}}"

    args = parse_args()
    events = args.events

    for event in events:
        if "_" in event:
            short_gid = event.split("_")[0]
        else:
            short_gid = event

        gid = re.findall(r"\d+", re.search(r"((S|GW)\d{6})", short_gid).group())[0]
        name = "GW" + gid

        event_path = os.path.join(BASE_PATH, short_gid)
        print(f"Path: {event_path}")
        C01_path = os.path.join(event_path, "C01_offline", "")

        if args.prod is not None:
            prod_number = args.prod
        else:
            prior_path = os.path.join(C01_path, "*.prior")
            prior_files = natsorted(glob.glob(prior_path))
            if len(prior_files) < 1:
                raise RuntimeError(f"Could not find files for: {short_gid}")
            prior_file = prior_files[-1]
            prod_number = os.path.basename(prior_file).split(".")[0]

        print(f"Copying Prod: {prod_number}")
        ini_file = os.path.join(C01_path, prod_number + ".ini")
        prior_file = os.path.join(C01_path, prod_number + ".prior")

        new_ini_file = f"{name}.ini"
        new_prior_file = f"{name}.prior"

        shutil.copyfile(ini_file, new_ini_file)
        shutil.copyfile(prior_file, new_prior_file)

        label = f"{name}_{waveform}"

        with open(new_ini_file, "r") as file:
            data = file.readlines()

        new_data = []
        outdir = f"outdir_{label}/"

        for line in data:
            line = re.sub("outdir=.*", f"outdir={outdir}", line)
            line = re.sub(
                "webdir=.*",
                f"webdir=/home/michael.williams/public_html/nessai-gwtc/O3/initial/{label}/",
                line,
            )
            line = re.sub("prior-file=.*", f"prior-file={new_prior_file}", line)
            line = re.sub(
                "waveform-approximant=.*", f"waveform-approximant={waveform}", line
            )
            line = re.sub("prod.o3.cbc.pe.lalinference", "dev.o4.cbc.pe.bilby", line)
            line = re.sub("label=.*", f"label={label}", line)
            line = re.sub("sampler=.*", f"sampler=nessai", line)
            line = re.sub("sampler-kwargs=.*", f"sampler-kwargs={sampler_kwargs}", line)
            line = re.sub("n-parallel=.*", "n-parallel=2", line)
            line = re.sub("calibration-model=.*", "calibration-model=None", line)
            line = re.sub("time-marginalization=.*", "time-marginalization=False", line)

            if "detectors" in line:
                dets = ast.literal_eval(line.split("=")[1])

            new_data.append(line)

        new_data.append("reweighting-configuration=calibration_reweight.json\n")
        new_data.append("reweight-nested-samples=False")

        lookup_table = {}
        additional_paths = []
        for det in dets:
            path = outdir + f"data/calibration_{det}.h5"
            lookup_table[det] = path
            additional_paths.append(path)

        new_data.append(f"additional-transfer-paths={','.join(additional_paths)}\n")
        new_data.append(f"calibration-lookup-table={json.dumps(lookup_table)}\n")

        with open(new_ini_file, "w") as file:
            file.writelines(new_data)


if __name__ == "__main__":
    main()
