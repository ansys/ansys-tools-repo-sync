import os

from ansys.tools.repo_sync.repo_sync_v2 import synchronize_v2

from tests.conftest import ASSETS_DIRECTORY, TOKEN, check_files_in_pr, cleanup_remote_repo


def test_synchronize(temp_folder):
    """Test syncronization tool (without manifest)."""

    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"

    # Call the function
    result = None
    try: 
        result = synchronize_v2(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result
        
        # Check that the proper modifed files have been added
        list_of_files = ["src/ansys/api/test/v0/hello_world.py", "src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)

def test_synchronize_with_manifest(temp_folder):
    """Test syncronization tool (with manifest)."""
    
    # Define your test data here
    owner = "ansys"
    repository = "ansys-tools-repo-sync"
    from_dir = os.path.join(ASSETS_DIRECTORY, "ansys")
    to_dir = "src/ansys"
    manifest = os.path.join(ASSETS_DIRECTORY, "manifest.txt")

    # Call the function
    result = None
    try: 
        result = synchronize_v2(
            owner=owner,
            repository=repository,
            token=TOKEN,
            from_dir=from_dir,
            to_dir=to_dir,
            manifest=manifest
        )

        # Assertions or validations
        assert f"https://github.com/ansys/ansys-tools-repo-sync/pull/" in result
        
        # Check that the proper modifed files have been added
        list_of_files = ["src/ansys/api/test/v0/test.proto"]
        assert check_files_in_pr(owner, repository, result, list_of_files)

    except Exception as err:
        raise err
    finally:
        if result:
            cleanup_remote_repo(owner, repository, result)