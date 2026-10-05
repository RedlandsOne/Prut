import sys

import pytest

from prut.main import main


def test_main_without_arguments(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["prut"])

    with pytest.raises(SystemExit) as error:
        main()

    assert error.value.code == 0


def test_main_with_too_many_arguments(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["prut", "one.prut", "two.prut"],
    )

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert "Usage:" in captured.out


def test_main_with_missing_file(monkeypatch, capsys):
    monkeypatch.setattr(
        sys,
        "argv",
        ["prut", "missing.prut"],
    )

    with pytest.raises(SystemExit) as error:
        main()

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert "File not found" in captured.out
