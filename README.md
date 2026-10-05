# Prut

> A small, modern programming language built from scratch.

Prut is an experimental programming language designed to be simple, readable, and easy to understand while exploring how programming languages work internally.

## Features

Prut currently supports:

* Variables
* Strings
* Numbers
* Booleans
* Arithmetic
* Comparisons
* `if` / `else` / `end` conditionals
* Nested conditionals
* Interactive REPL
* Graphical launcher
* Running `.prut` source files

## Example

```prut
say "Hello, world!"

set name = "Jed"
say name

set number = 10
say number + 5

if number >= 10
    say "Number is 10 or greater."
else
    say "Number is less than 10."
end
```

Output:

```text
Hello, world!
Jed
15
Number is 10 or greater.
```

## Installation

Clone the repository:

```bash
git clone https://github.com/RedlandsOne/Prut.git
cd Prut
```

Install Prut in editable mode:

```bash
python -m pip install -e .
```

Prut requires **Python 3.10 or newer**.

## Running Prut

### Interactive REPL

```bash
prut
```

You can also run:

```bash
python -m prut
```

### Run a program

```bash
prut examples/hello.prut
```

### Graphical launcher

```bash
prut-gui
```

The graphical launcher provides a built-in editor and output panel for writing and running Prut programs without using the terminal.

## Project Structure

```text
prut/
├── .github/
│   └── workflows/
│       └── tests.yml
├── examples/
│   └── hello.prut
├── src/
│   └── prut/
│       ├── __init__.py
│       ├── __main__.py
│       ├── interpreter.py
│       ├── launcher.py
│       ├── lexer.py
│       ├── main.py
│       ├── parser.py
│       └── repl.py
├── tests/
│   └── test_basic.py
├── prut_app.py
├── prutlog.ico
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Development

Install the development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Prut also uses GitHub Actions to automatically run the tests when changes are pushed or pull requests are opened.

## Version

**Current version: 0.2.0**

## Project Status

Prut is an experimental project under active development.

The goal is to continue expanding the language while keeping its syntax simple and understandable.

Future versions may introduce additional language features, improved tooling, and a more complete development environment.

## License

Prut is released under the **MIT License**.

## Redlands One

Prut is developed by **Redlands One**, an independent technology organization focused on software, programming languages, operating systems, networking, and experimental technology projects.

**GitHub:** https://github.com/RedlandsOne
