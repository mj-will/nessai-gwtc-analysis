#!/usr/bin/env bash
events=(
    "GW150914_095045"
    "GW151012_095443"
    "GW151226_033853"
    "GW170104_101158"
    "GW170608_020116"
    "GW170729_185629"
    "GW170809_082821"
    "GW170814_103043"
    "GW170818_022509"
    "GW170823_131358"
)

for event in "${events[@]}"; do
    url="https://git.ligo.org/asimov/data/-/raw/main/events/gwtc-2-1/${event}.yaml"
    wget $url
    filename=$(basename "$url")
    event_short=${event%%_*}
    summaryextract --outdir ./ --samples $filename --label C01:IMRPhenomXPHM --filename ${event_short}_GWTC_2p1_IMRPhenomXPHM.dat --file_format dat
done