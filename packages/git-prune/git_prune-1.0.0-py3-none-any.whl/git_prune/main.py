import re
import shlex
import subprocess
import sys
from pathlib import Path

import click


class GitPrune:
    def __init__(self, **kwargs):
        self.working_directory = kwargs["dir_"] if ("dir_" in kwargs) else Path.cwd()
        self.is_git = (
            True
            if (Path(self.working_directory) / ".git").exists()
            else sys.exit("Directory does not contain .git directory.")
        )
        self.git = (
            f"/usr/bin/git --git-dir={self.working_directory}/.git/ --work-tree={self.working_directory}"
            if self.working_directory != Path.cwd()
            else "git"
        )

        self.shell_cmd(f"{self.git} fetch -p")

    @property
    def remote_branches(self) -> list[str]:
        """All of the remote branches

        Returns:
            list[str]: List of all the remote branches
        """
        remote_branches = self.shell_cmd(f"{self.git} for-each-ref")
        remote_branches = re.findall(r"refs/remotes/[a-zA-Z]*/(.*)", remote_branches)
        for line in remote_branches:
            if "HEAD" in line:
                remote_branches.remove(line)
            else:
                pass
        return remote_branches

    @property
    def local_branches(self) -> list[str]:
        """All of the local branches

        Returns:
            list[str]: List of all the local branches
        """
        local_branches = self.shell_cmd(f"{self.git} for-each-ref")
        local_branches = re.findall(r"refs/heads/(.*)", local_branches)
        return local_branches

    @property
    def not_remote(self) -> list[str]:
        """Branches that only exist on the local machine

        Returns:
            list[str]: List of the local only branches
        """
        return list(set(self.local_branches) - set(self.remote_branches))

    @property
    def current_branch(self) -> str:
        """Get the current branch

        Returns:
            str: Short branch name
        """
        return self.shell_cmd("git symbolic-ref --short HEAD")

    def shell_cmd(self, cmd: str) -> str:
        """Execute a shell command

        Args:
            cmd (str): Shell command with arguments to execute

        Returns:
            str: Shell command output
        """
        try:
            cmd = shlex.split(cmd)
            results = subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, shell=False
            )
            results = results.strip()
            return results.decode("UTF-8")
        except subprocess.CalledProcessError as exc:
            error_text = exc.output.strip()
            return error_text.decode("UTF-8")

    def change_to_branch(self):
        """Change to branch not marked for deletion"""
        try:
            if "master" in self.local_branches:
                target_branch = "master"
            if "main" in self.local_branches:
                target_branch = "main"
            if (
                "main" not in self.local_branches
                and "master" not in self.local_branches
            ):
                eligible_branches = self.remote_branches
                target_branch = eligible_branches[0]
        except IndexError as exc:
            print(exc)
            print(f"Current branch: {self.current_branch}")
            print(f"Not remote: {self.not_remote}")
            print(f"Local: {self.local_branches}")
            print(f"Remote: {self.remote_branches}")

        self.shell_cmd(f"git checkout {target_branch}")

    def delete_branches(self):
        """Delete the branches not on remote"""
        if not self.not_remote:
            return
        if self.current_branch in self.not_remote:
            self.change_to_branch()
        for branch in self.not_remote:
            self.shell_cmd(f'{self.git} branch -D "{branch}"')

    def prune_local_branches(self):
        """Confirm which branches will be removed. Remove them."""
        if self.not_remote:
            user_prompt = input(
                f"Branch(es) {self.not_remote} do not exist in the origin repository. Would you like to delete them? y/N: "
            )
            if user_prompt.lower() == "y":
                self.delete_branches()
            else:
                print(f"Branch(es) {self.not_remote} will not be deleted.")
        else:
            print("Local git branches match remote. No pruning needed.")
            sys.exit(0)


@click.command()
@click.option(
    "-d",
    "--directory",
    "dir_",
    default="pwd",
    help="Specify your target directory. Default is current working directory.",
)
def cli(dir_):
    if dir_ == "pwd":
        dir_ = Path.cwd()
    git_prune = GitPrune(dir_=dir_)
    git_prune.prune_local_branches()


if __name__ == "__main__":
    cli("pwd")
