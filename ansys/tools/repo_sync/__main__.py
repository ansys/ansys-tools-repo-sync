"""
Run with:

python -m ansys.tools.repo_sync -o "Organization" -r "repository"

"""
import argparse

from .repo_sync import synchronize

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Copy the content of a repository into an other repository.")
    parser.add_argument("-o", "--organization", help="Name of the organization. Default value is ``pyansys``.")
    parser.add_argument("-r", "--repository", help="Name of the repository.")
    parser.add_argument("-t", "--token", help="Personal access token.")
    parser.add_argument("-p", "--protos", help="Path to the folder containing the *.protos file to copy")
    parser.add_argument("-m", "--manifest", help="Manifest to mention prohibited extension files.")
    parser.add_argument("-d", "--dry-run", help="Simulate the behavior of the synchronization without performing it.")

    args = parser.parse_args()
    synchronize(
        manifest=args.manifest,
        repository=args.repository,
        organization=args.organization,
        protos_path=args.protos,
        dry_run=args.dry_run,
    )
