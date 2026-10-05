# Changelog

All notable changes to Prut are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Planned

- `repeat` loops
- Functions
- User input
- Additional data types
- Logical operators
- Improved error messages
- Standard library features
- Syntax highlighting
- Editor tooling
- Language Server Protocol support

---

## [0.2.0] - 2026-10-05

### Added

#### Language

- Variable assignment using `set`
- Output using `say`
- String literals
- Integer and floating-point numbers
- Boolean values using `true` and `false`
- Arithmetic expressions
- Comparison expressions
- `if` statements
- `else` branches
- Explicit `end` statements
- Nested conditional statements
- Variable references
- Parenthesised expressions

#### Operators

Added arithmetic operators:

- `+`
- `-`
- `*`
- `/`

Added comparison operators:

- `==`
- `!=`
- `>`
- `<`
- `>=`
- `<=`

#### Runtime

- Variable storage and lookup
- Boolean evaluation
- Arithmetic evaluation
- Comparison evaluation
- Truthy/falsy condition handling
- Undefined-variable errors
- Division-by-zero errors
- Runtime error reporting

#### Developer Experience

- Interactive Prut REPL
- Coloured REPL banner
- `.prut` source-file execution
- `python -m prut` support
- Prut Launcher graphical interface
- Windows executable packaging with PyInstaller
- Automated pytest test suite
- GitHub Actions CI

### Improved

- Parser now handles operator precedence
- Parser supports nested blocks
- Syntax errors include line and column information
- CLI provides clearer usage information
- Windows terminal output supports ANSI colours

---

## [0.1.0]

### Added

- Initial Prut project
- Basic lexer
- Basic parser
- Abstract Syntax Tree
- Interpreter
- `say` statement
- String literals
- Number literals
- Basic command-line execution

---

[Unreleased]: https://github.com/RedlandsOne/Prut/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/RedlandsOne/Prut/releases/tag/v0.2.0
[0.1.0]: https://github.com/RedlandsOne/Prut/releases/tag/v0.1.0
