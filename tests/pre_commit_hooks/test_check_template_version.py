"""Unit tests for check_template_version pre-commit hook"""

import pytest
from packaging.version import InvalidVersion, Version

from pre_commit_hooks import FriendlyException, check_template_version


def test_copier_file_exist():
    test_file = "./tests/pre_commit_hooks/.testing-copier-answers.yml"
    assert check_template_version._does_file_exist(test_file)


def test_copier_file_does_not_exist():
    test_file = "./tests/pre_commit_hooks/.bogus_file_name.yml"
    assert not check_template_version._does_file_exist(test_file)


def test_get_template_version():
    version_string = "v1.3.0"
    copier_config = {"_commit": version_string}
    test_version = Version(version_string)
    template_version = check_template_version._get_template_version(copier_config)
    assert test_version == template_version


def test_get_template_version_no_commit():
    version_string = "v1.3.0"
    copier_config = {"_nothing": version_string}
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._get_template_version(copier_config)
        assert "Cannot parse version string" in str(exc.value)


def test_get_template_version_invalid_version():
    version_string = "bogus_version_id"
    copier_config = {"_commit": version_string}
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._get_template_version(copier_config)
        assert "Cannot parse version string" in str(exc.value)


def test_get_template_url():
    template_url = "https://github.com/example/repo"
    copier_config = {"_src_path": template_url}
    extracted_url = check_template_version._get_template_path(copier_config)
    assert extracted_url == template_url


def test_get_template_url_no_src():
    template_url = "https://github.com/example/repo"
    copier_config = {"_nothing": template_url}
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._get_template_path(copier_config)
        assert "Cannot return _src_path" in str(exc.value)


def test_get_template_url_with_str_replace():
    template_url = "gh://example/repo"
    expected_url = "https://github.com/example/repo"
    copier_config = {"_src_path": template_url}
    extracted_url = check_template_version._get_template_path(copier_config)
    assert extracted_url == expected_url


def test_parse_git_blog():
    test_blob = "cc9babf3057ec04cdffc7d8b2edce212d589a255\trefs/tags/v1.3.1\nb2a26468a6ad00573b4c61948b6959a08a25938e\trefs/tags/v1.3.0\n341bf28af7e3b167e53a7643bc42ceb5db341ab5\trefs/tags/v1.2.1\nbd1a5522f324b77984873f517364c8ce59d2e44b\trefs/tags/v1.1.0\n5c4250154fd5ceddb8c75b25f8eb690c0914dc28\trefs/tags/v1.0.0\nebb241dacaefab8d57d424dabb463cbce9f4df88\trefs/tags/v0.0.6\n3968ff997296c1b5c1b5965579173cb91ae2afcf\trefs/tags/v0.0.5\n1f2e6e938ceeb4f5c0407a798edf8598b50123a7\trefs/tags/v0.0.4\n859bbfbfa354aafba9d0bc83c8d060211bade1a7\trefs/tags/v0.0.3\nb47caea55a20285fecf3a2f17e3eed3e5db0274a\trefs/tags/v0.0.2\n51b8601c413fab872d31d8f9cc78c8510c2e2e54\trefs/tags/v0.0.1\nfb6197d45acc6cc547b474ab6b878297b4641ff5\trefs/tags/1.2.0"
    expected_version = Version("v1.3.1")
    output_version = check_template_version._parse_git_blob(test_blob)
    assert expected_version == output_version


def test_parse_git_blob_none_blob():
    test_blob = None
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._parse_git_blob(test_blob)
        assert "Parsing the results of git ls-remote failed" in str(exc.value)


def test_parse_git_blob_empty_blob():
    test_blob = ""
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._parse_git_blob(test_blob)
        assert "Parsing the results of git ls-remote failed" in str(exc.value)


def test_parse_git_blog_no_tag():
    test_blob = "cc9babf3057ec04cdffc7d8b2edce212d589a255\trefs/tags"
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._parse_git_blob(test_blob)
        assert "Parsing the results of git ls-remote failed" in str(exc.value)


def test_get_latest_remote_version(mocker):
    test_blob = "cc9babf3057ec04cdffc7d8b2edce212d589a255\trefs/tags/v1.3.1\nb2a26468a6ad00573b4c61948b6959a08a25938e\trefs/tags/v1.3.0\n341bf28af7e3b167e53a7643bc42ceb5db341ab5\trefs/tags/v1.2.1\nbd1a5522f324b77984873f517364c8ce59d2e44b\trefs/tags/v1.1.0\n5c4250154fd5ceddb8c75b25f8eb690c0914dc28\trefs/tags/v1.0.0\nebb241dacaefab8d57d424dabb463cbce9f4df88\trefs/tags/v0.0.6\n3968ff997296c1b5c1b5965579173cb91ae2afcf\trefs/tags/v0.0.5\n1f2e6e938ceeb4f5c0407a798edf8598b50123a7\trefs/tags/v0.0.4\n859bbfbfa354aafba9d0bc83c8d060211bade1a7\trefs/tags/v0.0.3\nb47caea55a20285fecf3a2f17e3eed3e5db0274a\trefs/tags/v0.0.2\n51b8601c413fab872d31d8f9cc78c8510c2e2e54\trefs/tags/v0.0.1\nfb6197d45acc6cc547b474ab6b878297b4641ff5\trefs/tags/1.2.0"
    template_url = "https://github.com/example/repo"
    mocker.patch("pre_commit_hooks.check_template_version._retrieve_git_remote_tags", return_value=test_blob)
    expected_version = Version("v1.3.1")
    output_version = check_template_version._get_latest_remote_version(template_url)
    assert expected_version == output_version


def test_get_latest_remote_version_with_parse_failure(mocker):
    template_url = "https://github.com/example/repo"
    mocker.patch(
        "pre_commit_hooks.check_template_version._retrieve_git_remote_tags", side_effect=FriendlyException()
    )
    with pytest.raises(FriendlyException) as exc:
        _ = check_template_version._get_latest_remote_version(template_url)
        assert "Failed to get latest version" in str(exc.value)


def test_compare_versions():
    version_string = "v1.3.1"
    local_version = Version(version_string)
    remote_version = Version(version_string)
    assert 0 == check_template_version._compare_versions(local_version, remote_version)


def test_compare_versions_out_of_date(capfd):
    local_version = Version("v1.2.0")
    remote_version = Version("v1.3.1")
    check_template_version._compare_versions(local_version, remote_version)
    out, _ = capfd.readouterr()
    assert "A new version" in str(out)


def test_compare_versions_local_ahead():
    local_version = Version("v1.4.0")
    remote_version = Version("v1.3.0")
    assert 0 == check_template_version._compare_versions(local_version, remote_version)


def test_compare_versions_wrong_type():
    version_string = "v1.3.1"
    remote_version = Version(version_string)
    with pytest.raises(FriendlyException) as exc:
        check_template_version._compare_versions(version_string, remote_version)
        assert "Failed to compare" in str(exc.value)
