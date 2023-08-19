"""Ensure version bump."""
import pkg_resources
import os
import subprocess


def _any_py_files_changed(file_names):
    return any(file_name.endswith(".py") for file_name in file_names)


def _version_changed(pyproject_diff):
    return "+version = " in pyproject_diff


def find_remote():
    """Find the primary remote for a git repository."""
    remotes = subprocess.check_output(
        ["git", "remote"], universal_newlines=True
    ).splitlines()
    if len(remotes) == 1:
        return remotes[0]
    elif "origin" in remotes:
        return "origin"
    raise KeyError("Cannot determine remote")


def find_default_branch():
    """Find the default branch for a git repository."""
    remote = find_remote()
    remote_info = subprocess.check_output(
        ["git", "remote", "show", remote], universal_newlines=True
    ).splitlines()
    return [x for x in remote_info if "HEAD branch" in x][0].split(":")[1].strip()


def check_default_branch(default_branch):
    """Get changed files and pyproject.toml diff for a branch."""
    changed_files = subprocess.check_output(
        ["git", "diff", default_branch, "--name-only"], universal_newlines=True
    ).splitlines()
    pyproject_diff = subprocess.check_output(
        ["git", "diff", default_branch, "pyproject.toml"], universal_newlines=True
    )
    return changed_files, pyproject_diff


def check_version():
    """Verify the version is changed if any code files are changed."""
    default_branch = find_default_branch()
    # if the check is running in github actions, we need to use the remote ref
    if os.getenv("GITHUB_ACTIONS") == "true":
        default_branch = f"origin/{default_branch}"
    changed_files, pyproject_diff = check_default_branch(default_branch)
    check_file_changes = _any_py_files_changed
    for entry in pkg_resources.iter_entry_points("file_checkers"):
        if entry.name == "version_trigger":
            check_file_changes = entry.load()
            break

    if check_file_changes(changed_files) and not _version_changed(pyproject_diff):
        print("Code files changed with no corresponding version bump!")
        exit(1)
