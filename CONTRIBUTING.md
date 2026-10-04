# Contributing to Prut

Thanks for your interest in contributing to Prut!

Prut is an open-source programming language built from scratch. Contributions, ideas, bug reports, documentation improvements, and experiments are welcome.

## Before You Start

For major changes, open an issue first so the proposed change can be discussed before development begins.

Small fixes and documentation changes can generally be submitted directly as a pull request.

## Development Setup

Clone the repository:

```bash
git clone https://github.com/RedlandsOne/prut.git
cd prut
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Activate it on Linux or macOS:

```bash
source .venv/bin/activate
```

Install Prut with its development dependencies:

```bash
pip install -e ".[dev]"
```

## Running Prut

Run the interactive shell:

```bash
prut
```

Run a Prut program:

```bash
prut examples/hello.prut
```

You can also run it directly through Python:

```bash
python -m prut examples/hello.prut
```

## Running Tests

Run the test suite with:

```bash
pytest
```

All tests should pass before submitting a pull request.

## Project Structure

```text
src/prut/
├── __init__.py
├── __main__.py
├── interpreter.py
├── lexer.py
├── main.py
├── parser.py
└── repl.py
```

### Lexer

`lexer.py` converts Prut source code into tokens.

### Parser

`parser.py` converts tokens into an Abstract Syntax Tree (AST).

### Interpreter

`interpreter.py` executes the AST.

### REPL

`repl.py` provides the interactive Prut shell.

## Coding Guidelines

When contributing code:

* Keep code readable and straightforward.
* Use descriptive names.
* Add tests for new functionality.
* Keep changes focused.
* Update documentation when behaviour changes.
* Avoid unnecessary dependencies.
* Follow existing project conventions.

## Adding Language Features

New language features should generally include:

1. Lexer changes, if new tokens are required.
2. Parser changes, if new syntax is introduced.
3. Interpreter changes, if new behaviour is required.
4. Tests covering the new feature.
5. Documentation or examples where appropriate.

## Pull Requests

Pull requests should:

* Explain what was changed.
* Explain why the change was made.
* Include tests where appropriate.
* Pass the automated GitHub Actions checks.
* Avoid unrelated changes.

## Bug Reports

When reporting a bug, include:

* What you expected to happen.
* What actually happened.
* The Prut code that caused the problem.
* The version of Prut you were using.
* Any relevant error messages.

## Code of Conduct

Please be respectful and constructive when participating in the Prut project.

Harassment, discrimination, personal attacks, and deliberately disruptive behaviour are not welcome.

## License

By contributing to Prut, you agree that your contributions will be released under the project's MIT License.
