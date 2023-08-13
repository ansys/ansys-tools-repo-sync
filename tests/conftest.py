import os

from github import Github

THIS_PATH = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIRECTORY = os.path.join(THIS_PATH, "assets")
TOKEN = os.environ["TOKEN"]


def cleanup_remote_repo(owner, repository, pull_request_url):
    """Auxiliary function to clean-up remote repository after test execution."""
    # Authenticate with GitHub
    g = Github(TOKEN)

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
    g = Github(TOKEN)

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
