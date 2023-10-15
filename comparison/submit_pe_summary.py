#!/usr/bin/env python
"""
Submit a PE summary job via condor
"""
import argparse
import os
import subprocess

from pycondor import Job, Dagman

EXTRA_LINES = [
    "accounting_group=ligo.dev.o4.cbc.pe.bilby",
]


def parse_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submit-dir", type=str, required=True)
    parser.add_argument("--job-label", type=str, required=True)
    parser.add_argument("--dryrun", action="store_true")
    parser.add_argument("--memory", type=str, default="4GB")
    return parser.parse_known_args()


def get_dag(name: str, submit_dir: str, pesummary_args: str, memory: str) -> Dagman:
    """Get the dag"""

    submit = os.path.join(submit_dir, name, "")
    os.makedirs(submit, exist_ok=True)

    dag = Dagman("dag_" + name, submit=submit)

    summarypages_exe = (
        subprocess.run(["which", "summarypages"], stdout=subprocess.PIPE)
        .stdout.decode("utf-8")
        .strip()
    )

    extra_lines = EXTRA_LINES + [
        f"log={submit}/summarypage.log",
        f"output={submit}/summarypage.out",
        f"error={submit}/summarypage.err",
    ]

    job = Job(
        name="summarypage",
        executable=summarypages_exe,
        queue=1,
        getenv=True,
        submit=submit,
        request_memory=memory,
        request_disk="4GB",
        request_cpus=4,
        extra_lines=extra_lines,
    )
    job.add_arg(pesummary_args + " --multi_process 4")
    dag.add_job(job)
    return dag


def main():
    args, unknown = parse_args()
    pesummary_args = " ".join(unknown)
    print(pesummary_args)
    dag = get_dag(args.job_label, args.submit_dir, pesummary_args, args.memory)
    if not args.dryrun:
        dag.build_submit()


if __name__ == "__main__":
    main()
