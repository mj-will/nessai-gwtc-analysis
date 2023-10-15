#!/usr/bin/env bash
events=(
    "GW150914"
    "GW151012"
    "GW151226"
    "GW170104"
    "GW170608"
    "GW170729"
    "GW170809"
    "GW170814"
    "GW170818"
    "GW170823"
)
for event in "${events[@]}"; do
    sed -i "s/Pv2/XPHM/g" ${event}.ini 
    sed -i "s/minimum=0.125/minimum=0.05/g" ${event}.ini
    sed -i "s/phase-marginalization=True/phase-marginalization=False/g" ${event}.ini
done