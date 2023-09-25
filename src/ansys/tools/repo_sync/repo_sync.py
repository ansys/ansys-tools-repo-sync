from fnmatch import filter
import os
import shutil
import tempfile
from typing import Union

from git import Repo
from github import Auth, Github, GithubException


def include_patterns(*patterns):
    """Include listed patterns in ``copytree()``.

    Factory function that can be used with ``copytree()`` ignore parameter.

    Arguments define a sequence of glob-style patterns
    that are used to specify which files to NOT ignore.

    Creates and returns a function that determines this for each directory
    in the file hierarchy rooted at the source directory when used with
    shutil.copytree().
    """

    def _ignore_patterns(path, names):
        keep = set(name for pattern in patterns for name in filter(names, pattern))
        ignore = set(
            name
            for name in names
            if name not in keep and not os.path.isdir(os.path.join(path, name))
        )
        return ignore

    return _ignore_patterns


def delete_folder_contents(folder_path):
    """Delete the content inside a folder without deleting the folder itself.

    Parameters
    ----------
    folder_path : str
        Path to the folder whose content is requested to be deleted.

    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(
            f"Directory '{folder_path}' does not exist and will not be cleaned - process will continue."
        )
        return

    try:
        # List all files and directories in the folder
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)

            if os.path.isfile(item_path):
                # If it's a file, delete it
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # If it's a directory, use recursive call to delete its contents
                delete_folder_contents(item_path)
                # After the contents are deleted, remove the empty directory
                os.rmdir(item_path)

    except (FileNotFoundError, PermissionError, OSError) as e:  # pragma: no cover
        print(f"An error occurred: {str(e)} - process will continue.")


def synchronize(
    owner: str,
    repository: str,
    token: str,
    from_dir: str,
    to_dir: str,
    include_manifest: str,
    branch_checked_out: str = "main",
    clean_to_dir: bool = False,
    dry_run: bool = False,
    skip_ci: bool = False,
    random_branch_name: bool = False,
) -> Union[str, None]:
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
    include_manifest : str
        Path to manifest which mentions accepted extension files.
    branch_checked_out : str, optional
        Branch to check out, by default "main".
    clean_to_dir : bool, optional
        Delete the content inside the directory where the files will be synced, by default ``False``.
    dry_run : bool, optional
        Simulate the behavior of the synchronization without performing it, by default ``False``.
    skip_ci : bool, optional
        Whether to add a ``[skip ci]`` prefix to the commit message or not. By default ``False``.
    random_branch_name : bool, optional
        For testing purposes - generates a random suffix for the branch name ``sync/file-sync``.

    Returns
    -------
    Union[str, None]
        Pull request URL. In case of dry-run or no files modified, ``None`` is returned.

    """
    # New branch name and PR title
    new_branch_name = "sync/file-sync"
    pr_title = "sync: file sync performed by ansys-tools-repo-sync"

    # If requested, add random suffix
    if random_branch_name:
        from secrets import token_urlsafe

        new_branch_name = f"{new_branch_name}-{token_urlsafe(16)}"

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

    # Retrieve accepted extensions from manifest
    accepted_extensions = []
    print(f">>> Considering manifest file at {include_manifest} ...")
    with open(include_manifest, "r") as f:
        accepted_extensions = f.read().splitlines()

    # Clone the repository
    print(f">>> Cloning repository '{owner}/{repository}'...")
    repo_path = os.path.join(temp_dir.name, repository)
    authenticated_url = f"https://{token}@{pygithub_repo.html_url.split('https://')[-1]}"
    Repo.clone_from(authenticated_url, repo_path)

    # Define the destination path for the files to be synced
    destination_path = os.path.join(repo_path, to_dir)
    os.makedirs(destination_path, exist_ok=True)

    # If requested, clean the destination path
    if clean_to_dir:
        print(f">>> Cleaning content inside '{to_dir}'...")
        delete_folder_contents(destination_path)

    # Copy local folder contents to the cloned repository
    print(f">>> Moving desired files from {from_dir} to {destination_path} ...")
    shutil.copytree(
        from_dir,
        os.path.join(destination_path),
        ignore=include_patterns(*accepted_extensions),
        dirs_exist_ok=True,
    )

    print(f">>> Checking out new branch '{new_branch_name}' from '{branch_checked_out}'...")
    repo = Repo(repo_path)
    try:
        # Commit changes to a new branch
        repo.git.checkout(branch_checked_out)
        repo.git.checkout("-b", new_branch_name)
        print(f">>> Committing changes to branch '{new_branch_name}'...")
        repo.git.add("--all")
        repo.index.commit(f"{'[skip ci] ' if skip_ci else ''}sync: add changes from local folder")

        # Get a list of the files modified
        output = repo.git.diff("--compact-summary", f"{branch_checked_out}", f"{new_branch_name}")

        # If output is empty, avoid creating PR
        if not output:
            print(">>> No files to sync... Ignoring PR request.")
            return None
        else:
            print(">>> Summary of modified files...")
            print(output)

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
