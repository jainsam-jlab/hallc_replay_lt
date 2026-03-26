#!/usr/bin/env python

import subprocess
import pathlib
import argparse

REPLAYPATH = pathlib.Path(__file__).parent.resolve()
UTILPATH = REPLAYPATH / "UTIL_KAONLT"

assert UTILPATH, f"UTILPATH variable is not set correctly. Expected path: {str(UTILPATH)}"
print(f"\nRunning in {str(REPLAYPATH)}", end="\n\n")

SCRIPTS = {
    "Prod": UTILPATH / "scripts/online_physics/KaonLT/kaon_prod_replay_analysis_sw.sh",
    "Lumi": UTILPATH / "scripts/online_physics/KaonLT/luminosity/replay_lumi.sh",
    "HeePSing": UTILPATH / "scripts/online_physics/KaonLT/heep/sing_heepYield.sh",
    "HeePCoin": UTILPATH / "scripts/online_physics/KaonLT/heep/coin_heepYield.sh",
    "fADC": UTILPATH / "scripts/online_physics/KaonLT/fADC_SIDIS/fADC_Analysis.sh",
    "Optics": UTILPATH / "scripts/online_physics/KaonLT/optics/run_optics.sh"
}

def main(args):
    run_number = args.run_number
    run_type = args.run_type
    target = args.target

    print(f"Starting KaonLT data analysis for run number: {run_number}, run type: {run_type}, target: {target}")

    script_pth = SCRIPTS.get(run_type, None)
    if not script_pth.exists():
        raise FileNotFoundError(f"Script for run type '{run_type}' not found at path: {str(script_pth)}")


    if args.run_type == "Prod":
        script = [
            str(script_pth), 
            str(run_number), 
            str(target)
        ]
    elif run_type == "Lumi":
        script = [
        str(script_pth),
        str(run_number)
        ]    
    
    subprocess.run(
        script,
        cwd=str(REPLAYPATH),
        check=True
    )
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run KaonLT data analysis scripts based on provided run number, run type, and target.")

    parser.add_argument("--run-number", type=int, help="Run number (positive integer)", default=5013)
    parser.add_argument("--run-type", type=str, choices=["Prod", "Lumi", "HeePSing", "HeePCoin", "fADC", "Optics"], help="Run type", default="Prod")
    parser.add_argument("--target", type=str, choices=["LH2", "LD2", "Dummy10cm", "Carbon0p5", "AuFoil", "Optics1", "Optics2", "CarbonHole"], help="Target", default="LH2")

    args = parser.parse_args()
    assert str(args.run_number).isdigit() and len(str(args.run_number)) == 4, "Run number must be a positive integer of length 4."

    main(args)



# elif [[ $RUNTYPE == "Lumi" ]]; then
#     echo "Running luminosity analysis script - ${UTILPATH}/scripts/luminosity/replay_lumi.sh"
#     eval '"${UTILPATH}/scripts/luminosity/replay_lumi.sh" ${RUNNUMBER}'
# elif [[ $RUNTYPE == "HeePSing" ]]; then
#     echo "Running HeeP Singles analysis script - ${UTILPATH}/scripts/heep/sing_heepYield.sh"
#     eval '"${UTILPATH}/scripts/heep/sing_heepYield.sh" hms ${RUNNUMBER}'
#     eval '"${UTILPATH}/scripts/heep/sing_heepYield.sh" shms ${RUNNUMBER}'
# elif [[ $RUNTYPE == "HeePCoin" ]]; then
#     echo "Running HeeP Coin analysis script - ${UTILPATH}/scripts/heep/coin_heepYield.sh"
#     eval '"${UTILPATH}/scripts/heep/coin_heepYield.sh" ${RUNNUMBER}'
# elif [[ $RUNTYPE == "fADC" ]]; then
#     echo "Running fADC Coin analysis script - ${UTILPATH}/scripts/fADC_SIDIS/fADC_Analysis.sh"
#     eval '"${UTILPATH}/scripts/fADC_SIDIS/fADC_Analysis.sh" ${RUNNUMBER}'
# elif [[ $RUNTYPE == "Optics" ]]; then
#     echo "Running optics analysis script - "
#     eval '"${UTILPATH}/scripts/optics/run_optics.sh" ${RUNNUMBER}'
# fi
# if [[ $RUNTYPE != "Optics" ]]; then
#     eval '"${UTILPATH}/scripts/runlist/fill_runList.sh" ${RUNNUMBER} ${RUNTYPE} ${TARGET}'
# else echo "Full replay for HMS and SHMS completed, check output rootfiles for plots"
# fi
