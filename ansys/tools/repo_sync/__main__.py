"""
Run with:

python -m ansys.tools.repo_sync -f "path_to_package"

"""

import argparse

from .repo_sync import synchronize

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy the content of a repository into an other repository.")
    parser.add_argument("-o", "--organization", help="Name of the organization. Default value is ``pyansys``.")
    parser.add_argument("-r", "--repository", help="Name of the repository.")
    parser.add_argument("-t", "--token", help="Personal access token.")
    parser.add_argument("-f", "--filename", help="Add a specific file.")
    args = parser.parse_args()
    synchronize(args.folder)
