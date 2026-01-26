import pre_commit_hooks


def test_version():
    """Check to see that we can get the package version"""
    assert pre_commit_hooks.__version__ is not None
