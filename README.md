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

## Goals

Prut is being built with a few simple goals:

* Easy-to-read syntax
* Beginner-friendly programming
* Fast and lightweight execution
* A simple standard library
* Clear and useful error messages
* Easy to extend
* Built completely from scratch

## Project Status

Prut is currently in **early development**.

### Roadmap

* [ ] Prut v0.1 — Basic syntax
* [ ] Variables
* [ ] Strings
* [ ] Numbers
* [ ] Basic arithmetic
* [ ] `if` / `else`
* [ ] Loops
* [ ] Functions
* [ ] Lists
* [ ] Modules
* [ ] Standard library
* [ ] Package manager
* [ ] Prut v1.0

## Repository Structure

```text
prut/
├── README.md
├── LICENSE
├── .gitignore
├── src/
│   └── prut/
│       ├── __init__.py
│       ├── lexer.py
│       ├── parser.py
│       ├── interpreter.py
│       └── main.py
├── examples/
│   └── hello.prut
└── tests/
    └── test_basic.py
```

## Building Prut

Prut is currently being developed in Python.

More information about building and running Prut will be added as development progresses.

## Contributing

Prut is an experimental project, and contributions, ideas, bug reports, and suggestions are welcome.

## License

Prut is open source. See the `LICENSE` file for details.
