# git-prune

![build](https://img.shields.io/circleci/build/github/rsoper/git-prune/master?token=6eec49c405bc17c010e3bb14218aacef23ccee8a)
![git-prune-ver](https://img.shields.io/pypi/v/git-prune)
![pythonver](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![license](https://img.shields.io/github/license/mashape/apistatus.svg)


Clean up your local git branches to match the remote with one command. This tool checks your remote location for current branches, compares this list against the local git branches, and gives you the option to remove all orphaned local branches.

### Installation

`pip3 install git-prune`

### Usage

`git-prune` -- Prunes local branches in the current working directory.

`git-prune -d /Path/to/repository` -- Prunes local branches in the provided directory.
