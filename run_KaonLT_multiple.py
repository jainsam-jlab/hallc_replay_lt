#!/usr/bin/env python
import os
import argparse
import subprocess
import pathlib
import itertools
import time


from e1209011.database.runinfo import RunInfo

###############################################################################################################################################

# Q2=["5p5", "4p4", "3p0", "3p0", "2p1"]
# W=["3p02", "2p74", "3p14", "2p32", "2p95"]
# ORIENTATIONS = ["left", "right", "center"]
# EPSILONS = ["low", "high"]

# Q2 = ["3p0", "2p1"]
# W = ["3p14", "2p95"]
Q2 = ["4p4"]
W = ["2p74"]
ORIENTATIONS = ["left", "right", "center"]
EPSILONS = ["low", "high"]

###############################################################################################################################################

SYSTEMS = [
    (q2_str, w_str, ori, eps_str)
    for (q2_str, w_str), ori, eps_str in itertools.product(
        zip(Q2, W), ORIENTATIONS, EPSILONS
    )
    if not (ori == "right" and eps_str == "low")
]
###############################################################################################################################################
MAX_RUNTIME_SECONDS = 2 * 60 * 60  # 2 hours in seconds
###############################################################################################################################################


def main(args):

    # this script is not used any more, just keep it for record
    data_config = RunInfo("job_submission_local/RUN_LIST/data.json")
    dummy_config = RunInfo("job_submission_local/RUN_LIST/dummy.json")

    if args.debug:
        print("Debug mode is enabled. No jobs will be submitted.")
        return

    start_time = time.time()

    required_cache_file = []

    for q2_str, w_str, ori, eps_str in SYSTEMS:

        data_runs = data_config.get_run_list(q2_str, w_str, ori, eps_str)
        dummy_runs = dummy_config.get_run_list(q2_str, w_str, ori, eps_str)
        print(f"Processing Q2: {q2_str}, W: {w_str}, Orientation: {ori}, Epsilon: {eps_str}")
        print(f"Data runs: {data_runs}")
        print(f"Dummy runs: {dummy_runs}")
        required_cache_file = required_cache_file + data_runs + dummy_runs

        continue

        target = ["LH2"] * len(data_runs) + ["dummy"] * len(dummy_runs)
        for run, tgt in zip(data_runs + dummy_runs, target):
            cmd = list(map(str, [
                    "python3",
                    pathlib.Path(__file__).parent / "run_KaonLT.py",
                    f"--run-number",
                    run, 
                    f"--run-type",
                    "Prod",
                    f"--target",
                    tgt,
            ]))
            subprocess.run(
                cmd,
                check=True,
                text=True,
            )

            time_elapsed = time.time() - start_time

            if time_elapsed > MAX_RUNTIME_SECONDS:
                print(f"Reached maximum runtime of {MAX_RUNTIME_SECONDS} seconds. Stopping running further processes locally.")
                return

    required_cache_file = [f"/mss/hallc/spring17/raw/coin_all_{run:05d}.dat" for run in set(required_cache_file)]
    required_cache_file = [f for f in sorted(required_cache_file) if pathlib.Path(f).exists()]
    print(len(required_cache_file), "cache files are required for all runs.")
    chain = " ".join(required_cache_file)
    print(f"Required cache files for all runs: {chain}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    main(args)
