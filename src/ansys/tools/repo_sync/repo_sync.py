import os
import shutil
import tempfile
from typing import Optional

from git import Repo
from github import Auth, Github, GithubException


def synchronize(
    owner: str,
    repository: str,
    token: str,
    from_dir: str,
    to_dir: str,
    branch_checked_out: str = "main",
    manifest: Optional[str] = None,
    dry_run: bool = False,
):
    """Synchronize a folder to a remote repository.

    Parameters
    ----------
    owner : str
        Repository owner (user or organization).
    repository : str
        Repository name.
    token : str
        GitHub access token.
    from_dir : str
        Directory from which files want to be synced.
    to_dir : str
        Directory to which files want to be synced (w.r.t. the root of the repository).
    branch_checked_out : str, optional
        Branch to check out, by default "main".
    manifest : Optional[str], optional
        Path to manifest which mention prohibited extension files, by default ``None``.
    dry_run : bool, optional
        Simulate the behavior of the synchronization without performing it, by default ``False``.

    """
    # New branch name and PR title
    new_branch_name = "sync/file-sync"
    pr_title = "sync: file sync performed by ansys-tools-repo-sync"

    # Authenticate with GitHub
    g = Github(auth=Auth.Token(token))

    # Get the repository
    print(f">>> Accessing repository '{owner}/{repository}'...")
    pygithub_repo = g.get_repo(f"{owner}/{repository}")

    # Create a temporary directory for the clone
    #
    # tempfile.TemporaryDirectory will clean itself up once it has run out
    # of scope. No need to actively remove.

    temp_dir = tempfile.TemporaryDirectory(prefix="repo_clone_", ignore_cleanup_errors=True)

    # Check if manifest was provided
    prohibited_extensions = []
    if manifest:
        print(f">>> Considering manifest file at {manifest} ...")
        with open(manifest, "r") as f:
            prohibited_extensions = f.read().splitlines()

    # Clone the repository
    print(f">>> Cloning repository '{owner}/{repository}'...")
    repo_path = os.path.join(temp_dir.name, repository)
    authenticated_url = f"https://{token}@{pygithub_repo.html_url.split('https://')[-1]}"
    Repo.clone_from(authenticated_url, repo_path)

    # Copy local folder contents to the cloned repository
    destination_path = os.path.join(repo_path, to_dir)
    print(f">>> Moving desired files from {from_dir} to {destination_path} ...")
    os.makedirs(destination_path, exist_ok=True)
    shutil.copytree(
        from_dir,
        os.path.join(destination_path),
        ignore=shutil.ignore_patterns(*prohibited_extensions),
        dirs_exist_ok=True,
    )

    # Commit changes to a new branch
    print(f">>> Checking out new branch '{new_branch_name}' from '{branch_checked_out}'...")
    repo = Repo(repo_path)
    try:
        repo.git.checkout(branch_checked_out)
        repo.git.checkout("-b", new_branch_name)
        print(f">>> Committing changes to branch '{new_branch_name}'...")
        repo.git.add("--all")
        repo.index.commit("sync: add changes from local folder")

        pull_request = None
        if not dry_run:
            # Push changes to remote repositories
            print(f">>> Force-pushing branch '{new_branch_name}' remotely...")
            repo.git.push("--force", "origin", new_branch_name)

            # Create a pull request
            try:
                print(f">>> Creating pull request from '{new_branch_name}'...")
                pull_request = pygithub_repo.create_pull(
                    title=pr_title,
                    body="Please review and merge these changes.",
                    base=branch_checked_out,
                    head=new_branch_name,
                )
            except GithubException as err:
                if err.args[0] == 422 or err.data["message"] == "Validation Failed":
                    print(f">>> Branch and pull request already existed, searching for it...")

                    # Pull request already exists
                    prs = pygithub_repo.get_pulls()

                    # Find the associated PR (must be opened...)

                    associated_pull_request = None
                    for pr in prs:
                        if pr.head.ref == new_branch_name:
                            associated_pull_request = pr
                            break

                    # Return the associated PR
                    if associated_pull_request:
                        pull_request = associated_pull_request
                    else:
                        # Don't know what could have happened...
                        raise err
                else:
                    # Unidentified error.. raise it.
                    raise err

            print(f">>> Pull request created: {pull_request.html_url}")
            return pull_request.html_url
        else:
            print(f">>> Dry run successful.")
            return None
    finally:
        # Close local repo for proper file deletion
        repo.close()
