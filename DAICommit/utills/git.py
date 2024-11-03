import subprocess
from pathlib import Path
from git import Repo, exc

from rich.console import Console

from .cli import outro

def get_open_commit_ignore() -> set:
    ignore_set = set()
    ignore_file_path = Path('.aicommitignore')

    if ignore_file_path.is_file():
        with ignore_file_path.open() as f:
            for line in f:
                ignore_set.add(line.strip())

    return ignore_set

def get_staged_files() -> list:
    git_dir = subprocess.run(['git', 'rev-parse', '--show-toplevel'], capture_output=True, text=True, check=True)
    git_dir = git_dir.stdout.strip()

    files_result = subprocess.run(['git', 'diff', '--name-only', '--cached', '--relative', git_dir], capture_output=True, text=True, check=True)
    files_list = files_result.stdout.strip().split('\n') if files_result.stdout else []

    ignore_set = get_open_commit_ignore()
    allowed_files = [file for file in files_list if file not in ignore_set]

    return sorted(allowed_files)


def get_changed_files() -> list:
    modified_result = subprocess.run(['git', 'ls-files', '--modified'], capture_output=True, text=True, check=True)
    others_result = subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], capture_output=True,
                                   text=True, check=True)

    files = modified_result.stdout.strip().split('\n') + others_result.stdout.strip().split('\n')
    return sorted(file for file in files if file)

console = Console()
def git_add(files: list):
    with console.status("Adding files to commit", spinner='point'):
        subprocess.run(['git', 'add', *files])

def get_diff(files: list[str]) -> str:
    lock_files = [
        file for file in files if (
            '.lock' in file or
            '-lock.' in file or
            file.endswith(('.svg', '.png', '.jpg', '.jpeg', '.webp', '.gif'))
        )
    ]

    if lock_files:
        outro("Some files are excluded by default from 'git diff'. No commit messages are generated for these files:" + '\n'.join(lock_files), 'yellow')

    files_without_locks = [file for file in files if not ('.lock' in file or '-lock.' in file)]

    try:
        repo = Repo()
        staged_diff = repo.git.diff('--staged', '--', *files_without_locks)
    except exc.GitCommandError as e:
        outro(f"Error running git diff: {e}", 'red')
        exit(1)

    return staged_diff

def assert_git_repo():
    try:
        subprocess.run(['git', 'rev-parse'], check=True)
    except subprocess.CalledProcessError as error:
        raise Exception(str(error))
