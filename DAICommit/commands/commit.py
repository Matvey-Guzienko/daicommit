import subprocess
from typing import Optional

from colorama import Fore
from git import Repo
from pick import pick
from rich.console import Console
from rich.prompt import Confirm

from ..utills import (
    assert_git_repo,
    get_changed_files,
    get_diff,
    get_staged_files,
    git_add,
    menu,
    outro,
    try_tm,
)
from ..utills.generateCommitMessageFromGitDiff import generate_commit_message_by_diff

console = Console()


def commit(
    is_stage_all_flag: bool = False,
    full_git_moji_spec: bool = False,
    skip_commit_confirmation: bool = False,
):
    outro("DAICommit", "blue")
    print()

    if is_stage_all_flag:
        changedFiles = get_changed_files()

        if changedFiles:
            git_add(files=changedFiles)
        else:
            outro(
                "No changes detected, write some code and run `aicommit` again", "red"
            )
            exit(0)

    stagedFiles, errorStagedFiles = try_tm(get_staged_files)
    changedFiles, errorChangedFiles = try_tm(get_changed_files)

    if errorStagedFiles or errorChangedFiles:
        outro(f"✖ {errorStagedFiles or errorChangedFiles}", "red")
        exit(0)

    if not changedFiles and not stagedFiles:
        outro("No changes detected", "red")
        exit(0)

    with console.status("Counting staged files", spinner="point") as status:
        if not stagedFiles:
            outro("No files are staged", "red")
            status.stop()

            if changedFiles:
                selected = pick(
                    changedFiles,
                    "Select the files you want to add to the commit (Press Space to select, Enter to finish):",
                    multiselect=True,
                )
                if selected:
                    git_add([file[0] for file in selected])
                    console.clear()
                    return commit(False, full_git_moji_spec, skip_commit_confirmation)

            if not Confirm.ask(
                "Do you want to stage all files and generate commit message?",
                default="n",
            ):
                exit(0)
            else:
                console.clear()
                return commit(True, full_git_moji_spec, skip_commit_confirmation)

    outro(
        f"{len(stagedFiles)} staged files:\n"
        + "\n".join(f"  {file}" for file in stagedFiles),
        "green",
    )

    _, generateCommitError = try_tm(
        func=generate_commit_message_from_git_diff,
        diff=get_diff(files=stagedFiles),
        full_git_moji_spec=full_git_moji_spec,
        skip_commit_confirmation=skip_commit_confirmation,
    )


def generate_commit_message_from_git_diff(
    diff: str,
    full_git_moji_spec: Optional[bool],
    skip_commit_confirmation: Optional[bool],
):
    assert_git_repo()

    with console.status("Generating the commit message", spinner="point"):
        commit_message = generate_commit_message_by_diff(diff, True)
    outro("📝 Commit message generated", "green")

    outro(
        f"Generated commit message:\n"
        f"{Fore.LIGHTCYAN_EX}——————————————————{Fore.RESET}\n"
        f"{commit_message}\n"
        f"{Fore.LIGHTCYAN_EX}——————————————————{Fore.RESET}",
        "green",
    )
    if not skip_commit_confirmation and not Confirm.ask(
        "Confirm the commit message?", default="y"
    ):
        if Confirm.ask("Do you want to regenerate the message?", default="y"):
            return generate_commit_message_from_git_diff(
                diff, full_git_moji_spec, skip_commit_confirmation
            )
    else:
        with console.status("Committing the changes", spinner="point"):
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        if commit_result.returncode != 0:
            outro(commit_result.stderr, "red")
            exit(0)
        else:
            print(commit_result.stdout)
            outro("Successfully committed", "green")

        repo = Repo()

        branches = [branch.name for branch in repo.branches]

        if len(branches) == 1:
            if not Confirm.ask(
                f"Do you want to run `git push origin {branches[0]}`?", default="y"
            ):
                exit(0)
            else:
                branch = branches[0]
        else:
            branch = menu("Choose a branch to push to", options=branches)

        with console.status(f"Running `git push origin {branch}`", spinner="point"):
            push_result = subprocess.run(
                ["git", "push", "origin", branch],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )

        if push_result.returncode != 0:
            outro(commit_result.stderr, "red")
            exit(0)

        outro(f"Successfully pushed all commits to `{branch}` branch", "green")
    outro("Bye Bye 🧙‍", "blue")
