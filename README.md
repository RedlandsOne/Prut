# Prut

> A small, modern programming language built from scratch.

Prut is an experimental programming language designed to be simple to read, easy to learn, and useful for exploring how programming languages work.

It includes its own lexer, parser, abstract syntax tree, interpreter, interactive REPL, and graphical launcher.

---

## Features

Prut currently supports:

- Variables with `set`
- Output with `say`
- Strings
- Numbers
- Booleans
- Arithmetic expressions
- Comparison operators
- `if` / `else` / `end`
- Nested conditional statements
- Interactive REPL
- `.prut` source files
- Graphical Prut Launcher
- Windows executable support
- Automated tests
- GitHub Actions CI

---

## Example

```prut
say "Hello from Prut!"

set name = "Jed"
say name

set number = 10
say number + 5

if number >= 10
    say "Number is 10 or greater."
else
    say "Number is less than 10."
end
````

Output:

```text
Hello from Prut!
Jed
15
Number is 10 or greater.
```

---

# Installation

## Requirements

* Python 3.10 or newer
* Git
* Windows, macOS, or Linux

Python can be downloaded from the official Python website.

## Clone the repository

```bash
git clone https://github.com/RedlandsOne/Prut.git
cd Prut
```

## Install Prut

Install Prut in editable mode:

```bash
python -m pip install -e .
```

For development and testing:

```bash
python -m pip install -e ".[dev]"
```

---

# Running Prut

## Interactive REPL

Start the Prut interactive shell with:

```bash
prut
```

You can also start it with:

```bash
python -m prut
```

The REPL lets you enter Prut programs interactively.

Example:

```text
Prut 0.2.0
Interactive shell
Type 'exit' or 'quit' to leave.

>>> say "Hello!"
Hello!

>>> set number = 10

>>> say number + 5
15
```

To leave the REPL:

```text
>>> exit
```

or:

```text
>>> quit
```

---

# Running Prut Files

Prut programs use the `.prut` file extension.

For example:

```text
hello.prut
```

Run a file with:

```bash
prut hello.prut
```

You can also use:

```bash
python -m prut hello.prut
```

Example:

```prut
say "Hello, world!"

set name = "Jed"
say name

set number = 10
say number + 5
```

---

# Prut Launcher

Prut includes a graphical application called **Prut Launcher**.

It provides a simple environment for writing and running Prut programs without manually using the command line.

Start it with:

```bash
prut-gui
```

The launcher includes:

* Code editor
* Output panel
* New file
* Open file
* Save file
* Clear editor
* Run program
* Keyboard shortcuts
* Prut branding
* Dark developer-focused interface

The launcher can also be packaged as a Windows executable using PyInstaller.

---

# Language

Prut is designed around simple, readable syntax.

## Output

Use `say` to print something:

```prut
say "Hello!"
```

Numbers can also be printed:

```prut
say 42
```

Variables can be printed:

```prut
set name = "Jed"
say name
```

---

# Variables

Variables are created with `set`.

```prut
set name = "Jed"
set age = 14
set score = 85
```

Variables can then be used in expressions:

```prut
set number = 10
say number + 5
```

Output:

```text
15
```

---

# Strings

Strings are written inside double quotes:

```prut
say "Hello, world!"
```

They can be stored in variables:

```prut
set message = "Welcome to Prut!"
say message
```

---

# Numbers

Prut supports integer and floating-point numbers.

```prut
set age = 14
set score = 85
set average = 7.5
```

Arithmetic can be performed directly:

```prut
say 10 + 5
say 10 - 3
say 4 * 5
say 20 / 4
```

Output:

```text
15
7
20
5.0
```

---

# Booleans

Prut supports two boolean values:

```prut
true
false
```

Example:

```prut
set enabled = true
say enabled
```

Booleans can be used in conditions:

```prut
set password_correct = true

if password_correct == true
    say "Access granted."
else
    say "Access denied."
end
```

---

# Operators

## Arithmetic

Prut currently supports:

| Operator | Description    |
| -------- | -------------- |
| `+`      | Addition       |
| `-`      | Subtraction    |
| `*`      | Multiplication |
| `/`      | Division       |

Example:

```prut
say 10 + 5
say 10 - 5
say 10 * 5
say 10 / 5
```

---

## Comparison

Prut supports:

| Operator | Description              |
| -------- | ------------------------ |
| `==`     | Equal to                 |
| `!=`     | Not equal to             |
| `>`      | Greater than             |
| `<`      | Less than                |
| `>=`     | Greater than or equal to |
| `<=`     | Less than or equal to    |

Example:

```prut
set age = 14

if age >= 13
    say "You are 13 or older."
end
```

---

# Conditions

Conditions use `if`.

Every `if` block ends with `end`.

```prut
if score >= 50
    say "Pass!"
end
```

---

# Else

Use `else` to provide an alternative:

```prut
if score >= 50
    say "Pass!"
else
    say "Try again."
end
```

---

# Nested Conditions

Conditions can be placed inside other conditions.

```prut
set score = 85

if score >= 50
    if score >= 90
        say "Excellent!"
    else
        say "Pass!"
    end
else
    say "Try again."
end
```

---

# Complete Example

```prut
say "Welcome to Prut!"

set name = "Jed"
set age = 14
set score = 85

say name
say age
say score

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

Output:

```text
Welcome to Prut!
Jed
14
85
Pass!
```

---

# Project Structure

```text
prut/
│
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
│       ├── launcher.py
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
├── prut_app.py
└── pyproject.toml
```

---

# How Prut Works

Prut is built as a small language pipeline.

```text
Prut Source Code
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

## Lexer

The lexer reads Prut source code and converts it into tokens.

For example:

```prut
set age = 14
```

becomes a sequence containing tokens such as:

```text
KEYWORD      set
IDENTIFIER   age
EQUALS       =
NUMBER       14
```

---

## Parser

The parser takes the tokens produced by the lexer and builds an **Abstract Syntax Tree (AST)**.

The AST represents the structure of the Prut program.

For example:

```prut
say 10 + 5
```

is represented as an expression containing:

```text
10
+
5
```

---

## Interpreter

The interpreter walks through the AST and executes the program.

It manages variables, evaluates expressions, performs calculations, and executes conditional branches.

---

# Development

Clone the repository:

```bash
git clone https://github.com/RedlandsOne/Prut.git
cd Prut
```

Install development dependencies:

```bash
python -m pip install -e ".[dev]"
```

Run the tests:

```bash
pytest
```

You can also run:

```bash
python -m pytest
```

---

# Testing

Prut uses **pytest** for automated testing.

The test suite covers areas including:

* Lexer tokens
* Statements
* Variables
* Arithmetic
* Boolean values
* Comparisons
* Conditions
* `else` branches
* Nested conditions
* Division by zero
* Undefined variables

Tests are also automatically run through GitHub Actions when changes are pushed or pull requests are opened.

---

# Building the Windows Executable

Prut Launcher can be packaged into a Windows executable with PyInstaller.

From the repository directory:

```powershell
python -m PyInstaller --onefile --windowed --name Prut --icon "prutlog.ico" --add-data "prutlog.ico;." --paths src prut_app.py
```

The executable will be created in:

```text
dist/Prut.exe
```

Build directories and PyInstaller files are excluded from Git using `.gitignore`.

---

# Error Handling

Prut provides syntax and runtime error messages.

For example, using an undefined variable:

```prut
say missing
```

produces a runtime error similar to:

```text
Prut runtime error: Undefined variable: missing
```

Division by zero is also detected:

```prut
say 10 / 0
```

which produces:

```text
Prut runtime error: Division by zero
```

---

# Version

Current version:

**0.2.0**

Prut follows a simple semantic-style versioning approach:

```text
MAJOR.MINOR.PATCH
```

---

# Roadmap

Prut is still under active development.

Planned or potential future features include:

* `repeat` loops
* Functions
* User input
* More data types
* Better error messages
* More operators
* Logical operators
* Standard library functionality
* File operations
* Improved REPL features
* Syntax highlighting
* Editor integration
* Language Server Protocol support
* Better developer tooling
* Package/module support

The language will continue to grow alongside the project.

---

# Contributing

Contributions, ideas, bug reports, and experiments are welcome.

Before making changes:

1. Fork or clone the repository.
2. Create a branch for your changes.
3. Make your changes.
4. Run the test suite.
5. Commit your changes.
6. Open a pull request.

Please read `CONTRIBUTING.md` for the project's contribution guidelines.

---

# License

Prut is released under the **MIT License**.

See [`LICENSE`](LICENSE) for the full license text.

---

# Redlands One

Prut is developed as part of **Redlands One**.

Redlands One is an independent technology organisation focused on building software, experimenting with new ideas, and learning through hands-on development.

Other projects include:

* **Prut** — programming language
* **Moldova OS** — experimental operating system

GitHub:

[https://github.com/RedlandsOne](https://github.com/RedlandsOne)

---

# Status

**Prut 0.2.0 — In active development.**

Prut is intentionally small and experimental. The project is being built from scratch to explore programming-language design, compilers and interpreters, software architecture, developer tooling, and practical programming.

> Build it. Break it. Understand it. Improve it.
