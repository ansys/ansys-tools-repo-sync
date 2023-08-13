import os

from github import Auth, Github

TEST_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.split(TEST_PATH)[0]
ASSETS_DIRECTORY = os.path.join(TEST_PATH, "assets")
TOKEN = os.environ.get("TOKEN")
SKIP_LOCALLY = False if os.environ.get("ON_WORKFLOW") else True


def cleanup_remote_repo(owner, repository, pull_request_url):
    """Auxiliary function to clean-up remote repository after test execution."""
    # Authenticate with GitHub
    g = Github(auth=Auth.Token(TOKEN))

    # Extract owner, repository, and pull request number from the URL
    url_parts = pull_request_url.split("/")
    pull_request_number = int(url_parts[-1])

    # Get the repository
    repo = g.get_repo(f"{owner}/{repository}")

    # Get the Pull Request
    pull_request = repo.get_pull(pull_request_number)

    # Delete the Pull Request
    pull_request.edit(state="closed")

    # Delete the remote branch
    branch_name = pull_request.head.ref
    repo.get_git_ref(f"heads/{branch_name}").delete()


def check_files_in_pr(owner, repository, pull_request_url, list_of_files):
    """Auxiliary function to verify modified files in PR."""
    # Authenticate with GitHub
    g = Github(auth=Auth.Token(TOKEN))

    # Extract owner, repository, and pull request number from the URL
    url_parts = pull_request_url.split("/")
    pull_request_number = int(url_parts[-1])

    # Get the repository
    repo = g.get_repo(f"{owner}/{repository}")

    # Get the Pull Request
    pull_request = repo.get_pull(pull_request_number)

    # Get the list of files changed in the Pull Request
    files_changed = [file.filename for file in pull_request.get_files()]

    # Check that the lists are the same
    return all(item in list_of_files for item in files_changed) and all(
        item in files_changed for item in list_of_files
    )


def get_pr_from_cli(owner, repository):
    """Auxiliary method to get the PR generated when using CLI tool."""
    # Authenticate with GitHub
    g = Github(auth=Auth.Token(TOKEN))

    # Get the repository
    repo = g.get_repo(f"{owner}/{repository}")

    # Pull request already exists
    prs = repo.get_pulls()

    # Find the associated PR (must be open...)
    associated_pull_request = None
    for pr in prs:
        if pr.head.ref == "sync/file-sync":
            associated_pull_request = pr
            break

    if not associated_pull_request:
        raise RuntimeError("Something went wrong in CLI execution...")
    else:
        return associated_pull_request.html_url
