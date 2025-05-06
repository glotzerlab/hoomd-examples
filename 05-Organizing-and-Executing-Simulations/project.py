import argparse

import signac
from compress import compress
from equilibrate import equilibrate
from randomize import randomize

if __name__ == "__main__":
    # Parse the command line arguments: python action.py --action <ACTION> [DIRECTORIES]
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", required=True)
    parser.add_argument("directories", nargs="+")
    args = parser.parse_args()

    # Open the signac jobs
    project = signac.get_project()
    jobs = [project.open_job(id=directory) for directory in args.directories]

    # Call the action
    if args.action == "compress":
        compress(*jobs)
    elif args.action == "equilibrate":
        equilibrate(*jobs)
    elif args.action == "randomize":
        randomize(*jobs)
