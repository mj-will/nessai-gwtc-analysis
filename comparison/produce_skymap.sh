#!/usr/bin/env bash
EVENT=$1
ANALYSES=(
    GWTC-2
    nessai-XPHM
)

for ANALYSIS in "${ANALYSES[@]}"; do
    PATHNAME=./skymaps/${EVENT}/${ANALYSIS}/
    echo ${PATHNAME}
    FILENAME=${PATHNAME}/skymap.fits 
    if [[ ! -e "$FILENAME" ]]; then
    ligo-skymap-from-samples \
        --samples gwtc-1/comparison/${EVENT}/samples/posterior_samples.h5 \
        --outdir ${PATHNAME} \
        --path ${ANALYSIS}/posterior_samples \
        --maxpts 5000 \
        --jobs 4
    fi
done