#!/usr/bin/env python
import os
import argparse
import itertools
import pathlib


USER = os.environ['USER']
# GROUP = 'c-pionlt'
GROUP = 'c-kaonlt' # analysis directory, not the unix group
PWD = pathlib.Path(__file__).parent.resolve()

###########################################################################################
print("Beginning setup of folders and symlinks")
print("-" * 30)

# check hostname
if not 'farm' in os.environ['HOST']:
    print("Host not recognised, please add relevant pathing for hostname to the script and re-run")
    exit(1)

ANALPATH = pathlib.Path(f'/group/{GROUP}')
VOLATILEPATH = pathlib.Path(f"/volatile/hallc/{GROUP}")

###########################################################################################

def main(args):
    
    if args.dry_run:
        print(f"Dry run: create symlink {str(ANALPATH / 'hcana')} -> {str(PWD / 'hcana')}")
    else:
        create_symlink(ANALPATH / 'hcana', PWD / 'hcana', overwrite=args.overwrite)

    ###########################################################################################
    # Next, need to make a load of directories, check they exist, if not, make em!
    CREATEDIRS = ['ROOTfiles', 'OUTPUT', 'REPORT_OUTPUT', 'HISTOGRAMS']
    DIRSTRUCT = {
        'Analysis' : ['HeeP', 'Lumi', f'{args.particle.capitalize()}LT', 'PID', 'Optics', 'General'],
        'Calib' :  ['Hodo', 'DC', 'HGC', 'Aero', 'NGC', 'General', 'Timing'],
        'Scalers' : []
    }

    for d1, (d2, subdirs) in itertools.product(CREATEDIRS, DIRSTRUCT.items()):
        for d3 in subdirs:
            pth = VOLATILEPATH / USER / d1 / d2 / d3
            if args.dry_run:
                print(f'Dry run: create directory {str(pth)}')
            else:
                pth.mkdir(parents=True, exist_ok=True)

    # also create the following directories in VOLATILEPATH / USER
    extra_dirs = ['raw', 'log', 'worksim']
    for d in extra_dirs:
        pth = VOLATILEPATH / USER / d
        if args.dry_run:
            print(f'Dry run: create directory {str(pth)}')
        else:
            pth.mkdir(parents=True, exist_ok=True)

    ###########################################################################################

    # Directories now created, make the sym links
    for d in CREATEDIRS:
        src = VOLATILEPATH / USER / d
        des = PWD / d
        if args.dry_run:
            print(f'Dry run: create symlink {str(src)} -> {str(des)}')
        else:
            create_symlink(src, des, args.overwrite)

    # some extra symlink
    EXTRALINKS = {
        'raw_volatile' : VOLATILEPATH / USER / 'raw',
        'raw' : '/cache/hallc/spring17/raw',
        'raw_PionLT' : '/cache/hallc/c-pionlt/raw',
        'raw_KaonLT' : '/cache/hallc/spring17/raw',
        'cache' : '/cache/hallc/spring17/raw'
    }

    for link_name, src_path in EXTRALINKS.items():
        src, des = pathlib.Path(src_path), PWD / link_name
        if args.dry_run:
            print(f'Dry run: create symlink {str(src)} -> {str(des)}')
        else:
            create_symlink(src, des, args.overwrite)

    ###########################################################################################
    # hcana setup ????
    ###########################################################################################

    print('\nAll DONE.')



################################################################################################################
def overwrite_symlink(src:pathlib.Path, des:pathlib.Path):
    des.unlink()
    des.symlink_to(src)

def is_broken_link(pth:pathlib.Path):
    return pth.is_symlink() and not pth.exists()

def is_real_path(pth:pathlib.Path):
    return pth.exists() and not pth.is_symlink()

def is_valid_link(pth:pathlib.Path):
    return pth.is_symlink() and pth.exists()

def create_symlink(src:pathlib.Path, des:pathlib.Path, overwrite=True):
    """Create a symlink from src to des, overwriting if necessary."""

    if is_real_path(des):
        print(f"Source {str(des)} is not a symlink, cannot create link.")
        return

    # here des must be a symlink (broken or valid) or does not exist at all
    if is_valid_link(des):
        # valid link but linked to something else
        if not des.resolve().samefile(src.resolve()):
            if overwrite:
                print(f"Overwriting existing symlink {str(des)} -> {str(src)}")
                overwrite_symlink(src, des)
        else:
            print(f"Symlink {str(des)} already exists and points to {str(des.resolve())}, skipping.")

    elif is_broken_link(des):
        if overwrite:
            print(f"Symlink {str(des)} is broken, now linking {str(des)} -> {str(src)}")
            overwrite_symlink(src, des)
        else:
            print(f"Symlink {str(des)} is broken, but not overwriting as --overwrite is not set. Please fix manually.")

    else:
        print(f"Creating symlink {des} -> {src}")
        des.symlink_to(src)


###########################################################################################



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up symbolic links for analysis paths.")
    parser.add_argument('--overwrite', action='store_true', help="Overwrite existing symlinks if broken")
    parser.add_argument("--particle", default="kaon", type=str, choices=["kaon", "pion"], help="Specify the particle type for the corresponding folder in `input`; currently only supports `kaon` and `pion`")
    parser.add_argument('--dry-run', action='store_true', help="Show what links would be created without actually creating them")
    args = parser.parse_args()
    main(args)
