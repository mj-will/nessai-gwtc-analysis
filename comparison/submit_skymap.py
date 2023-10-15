#!/usr/bin/env python
"""
Submit a ligo.skymap job via condor
"""
import argparse
import os

from pycondor import Job, Dagman

EXTRA_LINES = [
    "accounting_group=ligo.dev.o4.cbc.pe.bilby",
]


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=str, required=True)
    parser.add_argument("--job-label", type=str, required=True)
    parser.add_argument("--submit-dir", type=str, required=True)
    parser.add_argument("--dryrun", action="store_true")
    parser.add_argument("--memory", type=str, default="4GB")
    return parser.parse_known_args()


def get_dag(name: str, submit_dir: str, memory: str, event: str) -> Dagman:
    """Get the dag"""

    submit = os.path.join(submit_dir, name, "")
    os.makedirs(submit, exist_ok=True)

    dag = Dagman("dag_" + name, submit=submit)
    exe = "produce_skymap.sh"

    extra_lines = EXTRA_LINES + [
        f"log={submit}/skymap.log",
        f"output={submit}/skymap.out",
        f"error={submit}/skymap.err",
    ]

    job = Job(
        name="summarypage",
        executable=exe,
        queue=1,
        getenv=True,
        submit=submit,
        request_memory=memory,
        request_disk="4GB",
        request_cpus=4,
        extra_lines=extra_lines,
    )
    job.add_arg(event)
    dag.add_job(job)
    return dag


def main():
    args, unknown = parse_args()
    dag = get_dag(args.job_label, args.submit_dir, args.memory, args.event)
    if not args.dryrun:
        dag.build_submit()


if __name__ == "__main__":
    main()
