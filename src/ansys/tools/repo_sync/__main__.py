"""Tool to copy the content of one repo toward an other.

Run with:

.. code::

    repo-sync \
      --token <token> \
      --owner <organization-name> \
      --repository <repository-name> \
      --from-dir <path-to-dir-containing-files-to-sync> \
      --to-dir <target-dir-for-sync> \
      --include-manifest <path-to-manifest>

"""
import click

from .repo_sync import synchronize as _synchronize


@click.command(short_help="Copy the content of a repository into an other repository.")
@click.option("--owner", "-o", type=str, help="Name of the owner or organization.", required=True)
@click.option("--repository", "-r", type=str, help="Name of the repository.", required=True)
@click.option("--token", "-t", type=str, help="Personal access token.", required=True)
@click.option(
    "--from-dir",
    type=click.Path(file_okay=False, exists=True),
    help="Path to the folder containing the files to copy.",
    required=True,
)
@click.option(
    "--to-dir",
    type=click.Path(file_okay=False),
    help="Path of the folder that will contain the files (w.r.t. the root of the repository).",
    required=True,
)
@click.option(
    "--include-manifest",
    "-m",
    type=click.Path(dir_okay=False, exists=True),
    help="Manifest to mention accepted extension files.",
    required=True,
)
@click.option("--branch_checked_out", "-b", type=str, help="Branch to check out.", default="main")
@click.option(
    "--clean-to-dir",
    is_flag=True,
    default=False,
    help="Clean the folder defined in --to-dir before synchronizing.",
)
@click.option(
    "--dry-run",
    "-d",
    is_flag=True,
    default=False,
    help="Simulate the behavior of the synchronization without performing it.",
)
@click.option(
    "--skip-ci",
    is_flag=True,
    default=False,
    help="Adds a ``[skip ci]`` prefix to the commit message or not.",
)
@click.option(
    "--random-branch-name",
    is_flag=True,
    default=False,
    help="Generates a random branch name instead of the typical ``sync/file-sync``. Used for testing purposes mainly.",
)
def synchronize(
    owner,
    repository,
    token,
    from_dir,
    to_dir,
    include_manifest,
    branch_checked_out,
    clean_to_dir,
    dry_run,
    skip_ci,
    random_branch_name,
):
    """CLI command to execute the repository synchronization."""
    _synchronize(
        owner=owner,
        repository=repository,
        token=token,
        from_dir=from_dir,
        to_dir=to_dir,
        clean_to_dir=clean_to_dir,
        include_manifest=include_manifest,
        branch_checked_out=branch_checked_out,
        dry_run=dry_run,
        skip_ci=skip_ci,
        random_branch_name=random_branch_name,
    )


if __name__ == "__main__":
    synchronize()
