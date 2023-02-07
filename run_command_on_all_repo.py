"""Script to run a command on all bids app repositories.

Assumes that you have cloned all the repositories in the same directory.

This can be done with the following command:

    CNTX={orgs};
    NAME={bids-apps};
    PAGE=1
    curl "https://api.github.com/$CNTX/$NAME/repos?page=$PAGE&per_page=100" |
    grep -e 'clone_url*' |
    cut -d \" -f 4 |
    xargs -L1 git clone

Then run this script from within the maintenance-tools repo.
The script will apply the command to all the repos in `START_DIR`.
"""
import os
from pathlib import Path
from subprocess import run

from rich import print

# git shortlog -sne --all
COMMANDS = ["git add -A", "git commit -m 'precommit'", "git push"]

DRY_RUN = False

VERBOSE = True

OUTPUT_FILE = Path(__file__).parent / "output.md"
OUTPUT_FILE = None

START_DIR = Path(__file__).parent.joinpath("output")


class DummyResult:
    def __init__(self, stdout="dummy output", stderr=None):
        self.stdout = stdout
        self.stderr = stderr


def run_cmd(cmd, dry_run=True, verbose=True, split=True):
    if split:
        cmd = cmd.split()

    if verbose:
        print(f"[green]{' '.join(cmd)}[/green]")

    if dry_run:
        return DummyResult()

    result = run(cmd, capture_output=True, text=True)

    if verbose and result.stderr:
        print(f"stderr: {result.stderr}")

    return result


def print_to_output(output_file, text):
    if output_file is not None:
        with open(output_file, "a") as f:
            print(f"{text}", file=f)
        return
    else:
        print(text)


def main():
    if OUTPUT_FILE is not None:
        with open(OUTPUT_FILE, "w") as log:
            print(f"# Output from '{COMMANDS}'\n", file=log)

    print(f"Appying to folders in: {START_DIR}")

    for repo in START_DIR.iterdir():
        if repo.is_file():
            continue

        if repo.name in [
            ".github",
            "maintenance-tools",
            "bids-apps",
            "bids-apps.github.io",
        ]:
            continue

        os.chdir(repo)

        result = run_cmd(
            "git config --get remote.origin.url", verbose=False, dry_run=False
        )
        print(f"\n[blue]{repo.name}[/blue]")
        print(f"[blue]{result.stdout}[/blue]")
        print_to_output(
            output_file=OUTPUT_FILE, text=rf"## \[{repo.name}]({result.stdout[:-1]})"
        )

        for cmd in COMMANDS:
            result = run_cmd(cmd, verbose=VERBOSE, dry_run=DRY_RUN)
            print_to_output(output_file=OUTPUT_FILE, text="\n```")
            print_to_output(output_file=OUTPUT_FILE, text=result.stdout)
            print_to_output(output_file=OUTPUT_FILE, text="```\n")

    os.chdir(START_DIR)


if __name__ == "__main__":
    main()
