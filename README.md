# Prut

> A small, modern programming language built from scratch.

Prut is an experimental programming language designed to be simple to learn, easy to understand, and fun to build with.

## Example

```prut
say "Hello, world!"

set name = "Jed"
say name

set number = 10
say number + 5
```

Output:

```text
Hello, world!
Jed
15
```

## Interactive Mode

Prut includes an interactive REPL.

Start it with:

```bash
prut
```

Then write Prut code directly:

```text
Prut 0.1.0
Interactive shell
Type 'exit' or 'quit' to leave.

>>> say "Hello"
Hello
>>> set number = 10
>>> say number + 5
15
>>> exit
```

## Running a Program

Prut programs use the `.prut` file extension.

For example:

```bash
prut examples/hello.prut
```

You can also run a program through Python:

```bash
python -m prut examples/hello.prut
```

## Current Features

Prut 0.1 currently supports:

* Strings
* Numbers
* Variables
* `say` statements
* `set` statements
* Addition
* Subtraction
* Multiplication
* Division
* Parentheses
* Operator precedence
* Interactive REPL
* Syntax errors
* Runtime errors
* Automated tests

## Goals

Prut is being built with a few simple goals:

* Easy-to-read syntax
* Beginner-friendly programming
* Lightweight execution
* Clear and useful error messages
* A simple standard library
* Easy extensibility
* Built from scratch

## Roadmap

### Prut 0.1

* [x] Basic project structure
* [x] Lexer
* [x] Parser
* [x] Interpreter
* [x] Variables
* [x] Strings
* [x] Numbers
* [x] Basic arithmetic
* [x] REPL
* [x] Automated tests
* [x] GitHub Actions

### Prut 0.2

* [ ] Booleans
* [ ] Comparisons
* [ ] `if`
* [ ] `else`
* [ ] Better error messages

### Prut 0.3

* [ ] `while`
* [ ] `repeat`
* [ ] `for`
* [ ] Lists

### Prut 0.4

* [ ] Functions
* [ ] Function arguments
* [ ] Return values

### Prut 0.5

* [ ] Modules
* [ ] Imports
* [ ] Standard library

### Prut 1.0

* [ ] Stable language specification
* [ ] Package manager
* [ ] Comprehensive documentation
* [ ] Standard library
* [ ] Production-ready tooling

## How Prut Works

Prut currently uses an interpreter architecture:

```text
Prut source code
       │
       ▼
     Lexer
       │
       ▼
     Tokens
       │
       ▼
     Parser
       │
       ▼
      AST
       │
       ▼
   Interpreter
       │
       ▼
     Output
```

### Lexer

The lexer converts Prut source code into tokens.

### Parser

The parser converts those tokens into an Abstract Syntax Tree (AST).

### Interpreter

The interpreter evaluates the AST and executes the program.

## Repository Structure

```text
prut/
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── examples/
│   └── hello.prut
│
├── src/
│   └── prut/
│       ├── __init__.py
│       ├── __main__.py
│       ├── interpreter.py
│       ├── lexer.py
│       ├── main.py
│       ├── parser.py
│       └── repl.py
│
├── tests/
│   └── test_basic.py
│
├── .gitignore
├── CHANGELOG.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── README.md
└── pyproject.toml
```

## Development

Prut is currently developed in Python.

### Requirements

* Python 3.10 or newer
* Git

### Clone the repository

```bash
git clone https://github.com/RedlandsOne/prut.git
cd prut
```

### Create a virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Linux or macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Prut

Install Prut with its development dependencies:

```bash
pip install -e ".[dev]"
```

### Run Prut

Start the REPL:

```bash
prut
```

Run an example:

```bash
prut examples/hello.prut
```

### Run Tests

```bash
pytest
```

GitHub Actions also automatically runs the test suite when changes are pushed or a pull request is opened.

## Contributing

Contributions, ideas, bug reports, documentation improvements, and language experiments are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and contribution guidelines.

Please also read the [Code of Conduct](CODE_OF_CONDUCT.md).

## Project Status

Prut is **experimental and under active development**.

The language syntax and implementation may change significantly before version 1.0.

## License

Prut is open source software licensed under the MIT License.

See [LICENSE](LICENSE) for the full license text.
