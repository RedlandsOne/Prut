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
