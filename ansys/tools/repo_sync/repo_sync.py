import os
import shutil
import stat
import subprocess
import tempfile

import github


def synchronize(
    manifest: str = None,
    token: str = None,
    repository: str = "synchronization-demo-public",
    organization: str = "pyansys",
    protos_path: str = r"ansys\api\test\v0",
    dry_run: bool = True,
):
    """Synchronize the content of two different repositories.
    - clone the content of the reference repository
    - create a new branch
    - add/ remove some folders/files.
    - push the modification into the destination repository
    - create a pull request to merge the modification into the main branch of the destination repository

    """
    # use secret
    if not token:
        token = os.environ.get("TOKEN")

    user_name = os.environ.get("BOT_NAME")
    user_email = os.environ.get("BOT_EMAIL")

    branch_name = "sync/sync_branch"
    origin_directory = os.path.join(os.getcwd())

    # Create a temporary folder
    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone the repo.
        subprocess.check_call(["git", "clone", f"https://{token}@github.com/{organization}/{repository}"], cwd=temp_dir)

        repo_path = os.path.join(temp_dir, repository)

        # Set remote url
        subprocess.check_call(
            ["git", "remote", "set-url", "origin", f"https://{token}@github.com/{organization}/{repository}"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Set credential
        subprocess.check_call(
            ["git", "config", "--local", "user.name", f"{user_name}"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        subprocess.check_call(
            ["git", "config", "--local", "user.password", f"{token}"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        subprocess.check_call(
            ["git", "config", "--local", "user.email", f"{user_email}"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Create a new branch.
        try:
            subprocess.check_call(
                ["git", "checkout", "-b", branch_name],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        except:
            subprocess.check_call(
                ["git", "checkout", branch_name],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

        # Read manifest
        if manifest:
            with open(manifest, "r") as f:
                prohibited_extensions = f.read().splitlines()

                # Add protos.
                shutil.copytree(
                    os.path.join(origin_directory, protos_path),
                    os.path.join(temp_dir, protos_path),
                    ignore=shutil.ignore_patterns(*prohibited_extensions),
                )

        else:
            # Add protos.
            shutil.copytree(
                os.path.join(origin_directory, protos_path),
                os.path.join(temp_dir, protos_path),
            )

        # unsafe, should add specific file or directory
        subprocess.check_call(
            ["git", "add", "--a"],
            cwd=os.path.join(temp_dir, repository),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if protos_path:
            message = f"""Add folder content from {protos_path}."""
        else:
            message = f"Copy all files located into the {repository} repository from branch {branch_name}."

        if dry_run:
            subprocess.check_call(
                ["git", "commit", "-am", message, "--dry-run"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            print("Dry-run synchronization output:")
            print(output)
        else:
            subprocess.check_call(
                ["git", "commit", "-am", message],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            subprocess.check_call(
                ["git", "push", "-u", "origin", branch_name, "-v"],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            # Create pull request.
            gh = github.Github(token)
            repo = gh.get_repo(f"{organization}/{repository}")
            pr = repo.create_pull(title=message, body=message, head=branch_name, base="main")

    if not dry_run:
        print("Synchronization Succeeded...")


def _on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


if __name__ == "__main__":
    synchronize()
