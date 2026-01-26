from pre_commit_hooks import pre_executed_nb_never_execute


def test_nb_never_metadata(caplog, capsys, tmp_path):
    notebook_path = tmp_path / "empty_metadata.ipynb"
    with notebook_path.open("w") as fh:
        fh.write(
            """{
"metadata": {
  "nbsphinx": {
   "execute": "never"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
"""
        )
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 0

    captured = caplog.text
    assert captured == ""

    captured = capsys.readouterr().out
    assert captured == ""


def test_nb_empty_metadata(caplog, tmp_path):
    notebook_path = tmp_path / "empty_metadata.ipynb"
    with notebook_path.open("w") as fh:
        fh.write(
            """{
"metadata": {
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
"""
        )
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 1

    captured = caplog.text
    assert "Modified notebook to set" in captured
    assert "empty_metadata.ipynb" in captured


def test_nb_no_metadata(caplog, tmp_path):
    notebook_path = tmp_path / "no_metadata.ipynb"
    with notebook_path.open("w") as fh:
        fh.write(
            """{
 "nbformat": 4,
 "nbformat_minor": 5
}
"""
        )
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 1

    captured = caplog.text
    assert "Modified notebook to set" in captured
    assert "no_metadata.ipynb" in captured


def test_nb_always_executes(caplog, tmp_path):
    notebook_path = tmp_path / "always_execute.ipynb"
    with notebook_path.open("w") as fh:
        fh.write(
            """{
"metadata": {
  "nbsphinx": {
   "execute": "always"
  }
 }
}
"""
        )
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 1

    captured = caplog.text
    assert "always_execute.ipynb" in captured
    assert "expected 'never'" in captured


def test_nb_metadata_wrong_type(caplog, tmp_path):
    notebook_path = tmp_path / "wrong_metadata.ipynb"
    with notebook_path.open("w") as fh:
        fh.write(
            """{
"metadata": {
  "nbsphinx": "never"
 }
}
"""
        )
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 1

    captured = caplog.text
    assert "wrong_metadata.ipynb" in captured
    assert "expected a mapping" in captured


def test_nb_not_a_nb(caplog, tmp_path):
    notebook_path = tmp_path / "not_a_nb.ipynb"
    with notebook_path.open("w") as fh:
        fh.write(
            """# README
Hey man, this is just a readme.
"""
        )
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 1

    captured = caplog.text
    assert "ERROR" in captured


def test_nb_no_argument(caplog):
    result = pre_executed_nb_never_execute.main()
    assert result == 0

    captured = caplog.text
    assert "No notebooks found at path" in captured


def test_nb_no_notebooks(caplog, tmp_path):
    result = pre_executed_nb_never_execute.main(tmp_path)
    assert result == 0

    captured = caplog.text
    assert "No notebooks found at path" in captured


def test_nb_dir_does_not_exist(caplog, tmp_path):
    result = pre_executed_nb_never_execute.main(tmp_path / "not_there")
    assert result == 0

    captured = caplog.text
    assert "No notebooks found at path" in captured
