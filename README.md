````markdown
# Prut

> A small, modern programming language built from scratch.

Prut is an experimental programming language designed to be simple to learn, easy to understand, and fun to build with.

## Example

```prut
say "Hello, world!"

set name = "Jed"
say name

set age = 14

if age >= 13
    say "You are 13 or older."
else
    say "You are under 13."
end
````

Output:

```text
Hello, world!
Jed
You are 13 or older.
```

## Interactive Mode

Prut includes an interactive REPL.

Start it with:

```bash
prut
```

Then write Prut code directly:

```text
Prut 0.2.0
Interactive shell
Type 'exit' or 'quit' to leave.

>>> say "Hello"
Hello
>>> set number = 10
>>> say number + 5
15
>>> say number >= 10
True
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

Prut 0.2 currently supports:

### Values

* Strings
* Numbers
* Booleans
* Variables

### Statements

* `say`
* `set`
* `if`
* `else`
* `end`

### Arithmetic Operators

* `+` Addition
* `-` Subtraction
* `*` Multiplication
* `/` Division

### Comparison Operators

* `==` Equal
* `!=` Not equal
* `>` Greater than
* `<` Less than
* `>=` Greater than or equal
* `<=` Less than or equal

### Other

* Parentheses
* Operator precedence
* Nested `if` statements
* Interactive REPL
* Syntax errors
* Runtime errors
* Automated tests
* GitHub Actions

## Conditional Statements

Prut uses `if`, `else`, and `end` for conditional logic.

```prut
set age = 14

if age >= 13
    say "Allowed"
else
    say "Not allowed"
end
```

The condition is evaluated first.

If it is true, the code inside the `if` block runs.

If it is false and an `else` block exists, the `else` block runs.

## Boolean Values

Prut supports two boolean values:

```prut
true
false
```

They can be stored in variables:

```prut
set online = true
set connected = false

say online
say connected
```

## Comparisons

Prut supports six comparison operators:

```prut
10 == 10
10 != 5
10 > 5
5 < 10
10 >= 10
5 <= 10
```

Comparisons produce a boolean result.

For example:

```prut
set age = 14

say age >= 13
```

Output:

```text
True
```

## Nested Conditions

Conditions can be placed inside other conditions:

```prut
set score = 85

if score >= 90
    say "Excellent!"
else
    if score >= 50
        say "Pass!"
    else
        say "Try again."
    end
end
```

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

It recognizes:

* Keywords
* Identifiers
* Strings
* Numbers
* Booleans
* Arithmetic operators
* Comparison operators
* Assignment
* Parentheses
* Newlines

### Parser

The parser converts those tokens into an Abstract Syntax Tree (AST).

It currently understands:

* `say`
* `set`
* `if`
* `else`
* `end`
* Arithmetic expressions
* Comparison expressions
* Variables
* Strings
* Numbers
* Booleans

### Interpreter

The interpreter evaluates the AST and executes the program.

It currently handles:

* Variables
* Strings
* Numbers
* Booleans
* Arithmetic
* Comparisons
* Conditional statements
* Runtime errors

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

* [x] Booleans
* [x] Comparisons
* [x] `if`
* [x] `else`
* [x] Nested conditions
* [x] Better conditional error handling

### Prut 0.3

* [ ] `and`
* [ ] `or`
* [ ] `not`
* [ ] `while`
* [ ] `repeat`
* [ ] `break`
* [ ] `continue`

### Prut 0.4

* [ ] Lists
* [ ] List indexing
* [ ] `in`
* [ ] `len()`

### Prut 0.5

* [ ] Functions
* [ ] Function arguments
* [ ] Return values
* [ ] Local variables

### Prut 0.6

* [ ] Modules
* [ ] Imports
* [ ] Standard library

### Prut 1.0

* [ ] Stable language specification
* [ ] Package manager
* [ ] Comprehensive documentation
* [ ] Standard library
* [ ] Production-ready tooling

## Project Status

Prut is **experimental and under active development**.

The language syntax and implementation may change significantly before version 1.0.

## Contributing

Contributions, ideas, bug reports, documentation improvements, and language experiments are welcome.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and contribution guidelines.

Please also read the [Code of Conduct](CODE_OF_CONDUCT.md).

## License

Prut is open source software licensed under the MIT License.

See [LICENSE](LICENSE) for the full license text.

```
```
