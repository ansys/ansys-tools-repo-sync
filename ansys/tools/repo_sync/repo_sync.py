import os
import shutil
import stat
import subprocess

import github

# import git  # To be investigated.


def synchronize(
    token: str = None, repository: str = "synchronization-demo", filename: str = None, organization: str = "pyansys"
):
    """Synchronize the content of two differents repositories.
    - clone the content of the reference repository
    - create a new branch
    - add/ remove some folders/files.
    - push the modification into the destination repository
    - create a pull request to merge the modification into the main branch of the destination repository
    """

    # use secret
    if not token:
        token = os.environ.get("GH_PAT")

    user_name = os.environ.get("git_bot_user")
    organization = "pyansys"
    branch_name = "sync/sync_branch"

    # Clone the repo.
    process = subprocess.Popen(
        ["git", "clone", f"https://{token}@github.com/{organization}/{repository}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate()

    # # Set the username
    # process = subprocess.Popen(
    #     'git config user.name "Max"',
    #     shell=True,
    #     stdout=subprocess.PIPE,
    #     stderr=subprocess.PIPE,
    # )
    # stdout, stderr = process.communicate()

    os.chdir(repository)

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

    # Add a sample file.
    with open("testing.txt", "w") as f:
        f.write("hello world")

    # unsafe, should add specific file or directory
    if not filename:
        process = subprocess.Popen(
            ["git", "add", "--a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
    else:
        process = subprocess.Popen(
            ["git", "add", filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()

    if filename:
        message = f"Add {filename}"
    else:
        message = f"Copy all files located into the {repository} repository from branch {branch_name}."

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
    shutil.rmtree(os.path.join(parent_folder, repository), onerror=on_rm_error)


def on_rm_error(func, path, exc_info):
    # path contains the path of the file that couldn't be removed
    # let's just assume that it's read-only and unlink it.
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)


if __name__ == "__main__":
    synchronize()
