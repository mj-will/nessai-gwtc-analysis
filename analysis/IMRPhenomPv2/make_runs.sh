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
    sed -i "s/IMRPhenomXP/IMRPhenomPv2/g" ${event}.ini 
done