import os
import shutil
import tempfile
from typing import Optional

from git import Repo
from github import Github


def synchronize_v2(
    owner: str,
    repository: str,
    token: str,
    from_dir: str,
    to_dir: str,
    branch_checked_out: str = "main",
    manifest: Optional[str] = None,
    dry_run: bool = False,
):
    """_summary_.

    Parameters
    ----------
    owner : str
        _description_.
    repository : str
        _description_.
    token : str
        _description_.
    from_dir : str
        _description_.
    to_dir : str
        _description_
    branch_checked_out : str, optional
        _description_, by default "main".
    manifest : Optional[str], optional
        _description_, by default ``None``.
    dry_run : bool, optional
        _description_, by default ``False``.

    """
    # New branch name and PR title
    new_branch_name = "sync/file-sync"
    pr_title = "sync: file sync performed by ansys-tools-repo-sync"

    # Authenticate with GitHub
    g = Github(token)

    # Get the repository
    repo = g.get_repo(f"{owner}/{repository}")

    # Create a temporary directory for the clone
    temp_dir = tempfile.mkdtemp(prefix="repo_clone_")

    # Check if manifest was provided
    prohibited_extensions = []
    if manifest:
        with open(manifest, "r") as f:
            prohibited_extensions = f.read().splitlines()

    try:
        # Clone the repository
        repo_path = os.path.join(temp_dir, repository)
        Repo.clone_from(repo.git_url, repo_path)

        # Copy local folder contents to the cloned repository
        destination_path = os.path.join(repo_path, to_dir)
        os.makedirs(destination_path, exist_ok=True)
        shutil.copytree(
            from_dir,
            os.path.join(destination_path),
            ignore=shutil.ignore_patterns(*prohibited_extensions),
        )

        # Commit changes to a new branch
        repo = Repo(repo_path)
        repo.git.checkout(branch_checked_out)
        repo.git.checkout("-b", new_branch_name)
        repo.git.add("--all")
        repo.index.commit("sync: add changes from local folder")

        if not dry_run:
            # Push changes to remote repositorys
            repo.git.push("origin", new_branch_name)

            # Create a pull request
            pull_request = repo.create_pull(
                title=pr_title,
                body="Please review and merge these changes.",
                base=branch_checked_out,
                head=new_branch_name,
            )

            print(f"Pull Request created: {pull_request.html_url}")

    finally:
        # Cleanup: Remove temporary directory
        shutil.rmtree(temp_dir)
