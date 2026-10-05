import pytest

from prut.repl import repl


def test_repl_exit(monkeypatch, capsys):
    inputs = iter(["exit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl()

    captured = capsys.readouterr()

    assert "Prut 0.2.0" in captured.out
    assert "Interactive shell" in captured.out


def test_repl_quit(monkeypatch, capsys):
    inputs = iter(["quit"])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl()

    captured = capsys.readouterr()

    assert "Prut 0.2.0" in captured.out


def test_repl_runs_program(monkeypatch, capsys):
    inputs = iter([
        'say "Hello from REPL!"',
        "exit",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(SystemExit):
        repl()

    captured = capsys.readouterr()

    assert "Hello from REPL!" in captured.out
