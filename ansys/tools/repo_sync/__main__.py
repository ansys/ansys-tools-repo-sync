"""
Run with:

python -m ansys.tools.repo_sync -f "path_to_package"

"""

import argparse

from .repo_sync import synchronize_repositories

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Copy the content of a repository into an other repository.')
    parser.add_argument('-o', '--organization',
                        help='Name of the organization.')
    parser.add_argument('-r', '--repository',
                        help='Name of the repository.')
    parser.add_argument('-t', '--token',
                        help='Personal access token.')
    args = parser.parse_args()
    synchronize_repositories(args.folder)
