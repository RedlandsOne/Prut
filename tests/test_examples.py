from pathlib import Path

from prut.main import run_file


def test_hello_example(capsys):
    example = Path(__file__).parent.parent / "examples" / "hello.prut"

    run_file(str(example))

    captured = capsys.readouterr()

    assert captured.out == (
        "Hello, world!\n"
        "Jed\n"
        "15\n"
        "20\n"
        "5.0\n"
        "You are 13 or older.\n"
        "Access granted.\n"
        "Pass!\n"
    )
