import logging
import re
import subprocess
from dataclasses import dataclass
from functools import cache as _cache
from typing import Optional

import git

from .util import SerializableDataClass

_logger = logging.getLogger("braintrust.gitutil")


@dataclass
class RepoStatus(SerializableDataClass):
    """Information about the current HEAD of the repo."""

    commit: Optional[str]
    branch: Optional[str]
    tag: Optional[str]
    dirty: bool
    author_name: Optional[str]
    author_email: Optional[str]
    commit_message: Optional[str]
    commit_time: Optional[str]


@_cache
def _current_repo():
    try:
        return git.Repo(search_parent_directories=True)
    except git.exc.InvalidGitRepositoryError:
        return None


@_cache
def _get_base_branch(remote=None):
    # NOTE: This should potentially be configuration that we derive from the project,
    # instead of spending a second or two computing it each time we run an experiment.
    repo = _current_repo()
    kwargs = {} if remote is None else {"name": remote}

    try:
        remote = repo.remote(**kwargs).name
        s = subprocess.check_output(["git", "remote", "show", "origin"]).decode()
        match = re.search(r"\s*HEAD branch:\s*(.*)$", s, re.MULTILINE)
        if match is None:
            raise RuntimeError("Could not find HEAD branch in remote " + remote)
        branch = match.group(1)
    except Exception as e:
        _logger.warning(f"Could not find base branch for remote {remote}", e)
        branch = "main"
    return (remote, branch)


def _get_base_branch_ancestor(remote=None):
    remote_name, base_branch = _get_base_branch(remote)

    head = "HEAD" if _current_repo().is_dirty() else "HEAD^"
    try:
        return subprocess.check_output(["git", "merge-base", head, f"{remote_name}/{base_branch}"]).decode().strip()
    except subprocess.CalledProcessError as e:
        _logger.warning(f"Could not find a common ancestor with {remote_name}/{base_branch}", e)
        return None


def get_past_n_ancestors(n=10, remote=None):
    repo = _current_repo()
    if repo is None:
        return

    ancestor = repo.commit(_get_base_branch_ancestor())
    for _ in range(n):
        yield ancestor.hexsha
        if ancestor.parents:
            ancestor = ancestor.parents[0]
        else:
            break


def attempt(op):
    try:
        return op()
    except TypeError:
        return None
    except git.GitCommandError:
        return None


def get_repo_status():
    repo = _current_repo()
    if repo is None:
        return None

    commit = None
    commit_message = None
    commit_time = None
    author_name = None
    author_email = None
    tag = None
    branch = None

    dirty = repo.is_dirty()

    if not dirty:
        commit = attempt(lambda: repo.head.commit.hexsha).strip()
        commit_message = attempt(lambda: repo.head.commit.message).strip()
        commit_time = attempt(lambda: repo.head.commit.committed_datetime.isoformat())
        author_name = attempt(lambda: repo.head.commit.author.name).strip()
        author_email = attempt(lambda: repo.head.commit.author.email).strip()
        tag = attempt(lambda: repo.git.describe("--tags", "--exact-match", "--always"))

    branch = attempt(lambda: repo.active_branch.name)

    return RepoStatus(
        commit=commit,
        branch=branch,
        tag=tag,
        dirty=dirty,
        author_name=author_name,
        author_email=author_email,
        commit_message=commit_message,
        commit_time=commit_time,
    )
