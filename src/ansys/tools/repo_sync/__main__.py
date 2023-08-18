"""Tool to copy the content of one repo toward an other.
Run with:

repo-sync -o organization -r repository --from-dir ... --to-dir ... --token ... [-b branch_name -m manifest_file -d]

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
@click.option("--branch_checked_out", "-b", type=str, help="Branch to check out.", default="main")
@click.option(
    "--manifest",
    "-m",
    type=click.Path(dir_okay=False, exists=True),
    help="Manifest to mention prohibited extension files.",
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
def synchronize(
    owner, repository, token, from_dir, to_dir, branch_checked_out, manifest, dry_run, skip_ci
):
    """CLI command to execute the repository synchronization."""
    _synchronize(
        owner=owner,
        repository=repository,
        token=token,
        from_dir=from_dir,
        to_dir=to_dir,
        branch_checked_out=branch_checked_out,
        manifest=manifest,
        dry_run=dry_run,
        skip_ci=skip_ci,
    )


if __name__ == "__main__":
    synchronize()
