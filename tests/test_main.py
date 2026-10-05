from pathlib import Path

from prut.main import run_file, run_source


def test_run_source(capsys):
    run_source(
        """
        say "Hello from Prut!"
        """
    )

    captured = capsys.readouterr()

    assert captured.out == "Hello from Prut!\n"


def test_run_source_with_variables(capsys):
    run_source(
        """
        set name = "Jed"
        say name
        """
    )

    captured = capsys.readouterr()

    assert captured.out == "Jed\n"


def test_run_source_with_condition(capsys):
    run_source(
        """
        set score = 85

        if score >= 50
            say "Pass!"
        else
            say "Fail!"
        end
        """
    )

    captured = capsys.readouterr()

    assert captured.out == "Pass!\n"


def test_run_file(tmp_path, capsys):
    program = tmp_path / "hello.prut"

    program.write_text(
        'say "Hello from a file!"\n',
        encoding="utf-8",
    )

    run_file(str(program))

    captured = capsys.readouterr()

    assert captured.out == "Hello from a file!\n"
