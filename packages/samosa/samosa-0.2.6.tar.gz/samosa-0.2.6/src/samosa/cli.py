#!/usr/bin/env python3
# Copyright 2022 David Seaward and contributors
# SPDX-License-Identifier: AGPL-3.0-or-later
import os

import click

from samosa import git_task


def get_raw_root_or_exit():
    root = git_task.get_root_from_path(os.getcwd())
    if not root:
        exit("No repository found.")

    return root


def get_valid_root_or_exit():
    root = get_raw_root_or_exit()
    if not git_task.fix_and_validate_root(root, quiet_if_valid=True):
        exit(1)

    return root


@click.group()
def samosa():
    """
    Enforce a triangular Git workflow. If this is not possible, explain why.
    """


@samosa.command()
def init():
    """
    Initialise an empty local repository.
    """

    working_path = os.getcwd()
    root = git_task.get_root_from_path(working_path)
    if root is not None:
        exit(f"There is already a repository at {root}")

    if git_task.initialise_repository(working_path, quiet_if_valid=False):
        exit(0)
    else:
        exit(1)


@samosa.command()
@click.argument("remote")
@click.argument("url")
def add(remote, url):
    """
    Add remote to repository.
    """

    root = get_valid_root_or_exit()
    git_task.add_remote(root, remote, url)


@samosa.command()
@click.argument("branch")
def checkout(branch):
    """
    Check out a new or existing branch.
    """

    root = get_valid_root_or_exit()
    git_task.checkout_branch(root, branch)


@samosa.command()
def fix():
    """
    Prepare repository. Provide manual instructions if necessary.
    """

    root = get_raw_root_or_exit()
    if git_task.fix_and_validate_root(root, quiet_if_valid=False):
        exit(0)
    else:
        exit(1)
