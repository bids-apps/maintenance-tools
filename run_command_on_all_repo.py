r"""Script to run a command on all bids app repositories.

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

import yaml
from rich import print

# git shortlog -sne --all
COMMANDS = [
    "git add -A",
    "git commit -m 'set-dependabot-semiannually'",
    "git add -A",
    "git commit -m 'set-dependabot-semiannually'",
    "git push",
]

DRY_RUN = False

VERBOSE = True

OUTPUT_FILE = Path(__file__).parent / "output.md"
# OUTPUT_FILE = None

START_DIR = Path(__file__).parent.joinpath("output")


class DummyResult:
    def __init__(self, stdout="dummy output", stderr=None):
        self.stdout = stdout
        self.stderr = stderr


def run_cmd(cmd, dry_run=True, verbose=True, split=True):
    """Run a given command."""
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
    """Print to file or stdout."""
    if output_file is not None:
        with open(output_file, "a") as f:
            print(f"{text}", file=f)
        return
    else:
        print(text)


def main():
    """Run main function."""
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

        commands_to_run = []
        if do_on_repo(repo):
            print(f"\n[blue]{repo.name}[/blue]")

            result = run_cmd("git config --get remote.origin.url", verbose=False, dry_run=False)
            print_to_output(
                output_file=OUTPUT_FILE, text=rf"## \[{repo.name}]({result.stdout[:-1]})"
            )
            print(f"[blue]{result.stdout}[/blue]")

            commands_to_run = COMMANDS
            pre_commit_config = START_DIR / repo.name / ".pre-commit-config.yaml"
            if pre_commit_config.exists():
                commands_to_run = ["pre-commit install", "pre-commit run -a", *COMMANDS]

            for cmd in commands_to_run:
                result = run_cmd(cmd, verbose=VERBOSE, dry_run=DRY_RUN)
                print_to_output(output_file=OUTPUT_FILE, text="\n```")
                print_to_output(output_file=OUTPUT_FILE, text=result.stdout)
                print_to_output(output_file=OUTPUT_FILE, text="```\n")

    os.chdir(START_DIR)


def do_on_repo(repo) -> bool:
    """Do something on that repo."""
    gh_folder = START_DIR / repo.name / ".github"
    if gh_folder.exists():
        update_dependabot(gh_folder)
        return True

    return False


def update_dependabot(gh_folder: Path) -> None:
    """Update pre-commit config."""
    dependabot_cfg = gh_folder / "dependabot.yml"
    if dependabot_cfg.exists():
        with dependabot_cfg.open() as f:
            config = yaml.safe_load(f)
            print(config)

        for i, x in enumerate(config["updates"]):
            x["schedule"]["interval"] = "semiannually"
            config["updates"][i] = x

        with dependabot_cfg.open("w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    else:
        config = {
            "version": 2,
            "updates": [
                {
                    "package-ecosystem": "github-actions",
                    "directory": "/",
                    "schedule": {"interval": "semiannually"},
                }
            ],
        }
        with dependabot_cfg.open("w") as f:
            yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print_to_output(output_file=OUTPUT_FILE, text="dependabot modified")


if __name__ == "__main__":
    main()
