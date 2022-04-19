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
        os.chdir(temp_dir)

        # Clone the repo.
        process = subprocess.Popen(
            ["git", "clone", f"https://{token}@github.com/{organization}/{repository}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        os.chdir(repository)

        # Set credential
        process = subprocess.Popen(
            ["git", "config", "user.name", f"{user_name}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        process = subprocess.Popen(
            ["git", "config", "user.email", f"{user_email}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        # Create a new branch.
        try:
            process = subprocess.Popen(
                ["git", "checkout", "-b", branch_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()
        except:
            process = subprocess.Popen(
                ["git", "checkout", branch_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()

        # Read manifest
        if manifest:
            with open(manifest, "r") as f:
                prohibited_extensions = f.read().splitlines()

                # Add protos.
                shutil.copytree(
                    os.path.join(origin_directory, protos_path),
                    os.path.join(os.getcwd(), protos_path),
                    ignore=shutil.ignore_patterns(*prohibited_extensions),
                )

        else:
            # Add protos.
            shutil.copytree(
                os.path.join(origin_directory, protos_path),
                os.path.join(os.getcwd(), protos_path),
            )

        # unsafe, should add specific file or directory
        process = subprocess.Popen(
            ["git", "add", "--a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

        if protos_path:
            message = f"""Add folder content from {protos_path}."""
        else:
            message = f"Copy all files located into the {repository} repository from branch {branch_name}."

        if dry_run:
            process = subprocess.Popen(
                ["git", "commit", "-am", message, "--dry-run"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()
            print("Dry-run synchronization output:")
            print(stdout)
        else:
            process = subprocess.Popen(
                ["git", "commit", "-am", message],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()

            process = subprocess.Popen(
                ["git", "push", "-u", "origin", branch_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            stdout, stderr = process.communicate()

            # Create pull request.
            gh = github.Github(token)
            repo = gh.get_repo(f"{organization}/{repository}")
            pr = repo.create_pull(title=message, body=message, head=branch_name, base="main")

        # Delete the git repository that was created.
        parent_folder = os.path.dirname(os.getcwd())
        os.chdir(parent_folder)
        shutil.rmtree(os.path.join(parent_folder, repository), onerror=_on_rm_error)
        os.chdir(os.path.dirname(os.getcwd()))

    if not dry_run:
        print("Synchronization Succeeded...")


def _on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


if __name__ == "__main__":
    synchronize()
