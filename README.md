# PPL Assignment

## Project Status

Current implementation scores:

- **Code Generation:** 91/100
- **Static Checker:** 100/100
- **AST Generation:** 97/100
- **Grammar:** 100/100

## Operating Commands

### Update Java Version in Docker

The project requires **OpenJDK 23**. Run the following commands inside the Docker container:

```bash
apt update
apt install -y software-properties-common
add-apt-repository ppa:openjdk-r/ppa -y
apt update
apt install -y openjdk-23-jdk
```

### Build and Run Grammar, AST, and Static Checker

```bash
./build.sh && python3 -m pytest -vv --timeout=3 tests/*
```

### Build and Run Code Generation Tests

```bash
python3 -m pytest -vv --timeout=3 tests/test_codegen.py
```

## Project Structure

```text
src/
├── astgen/
│   └── ast_generation.py
│
├── codegen/
│   ├── codegen.py
│   ├── emitter.py
│   ├── error.py
│   ├── frame.py
│   ├── io.py
│   ├── jasmin_code.py
│   └── utils.py
│
├── grammar/
│   ├── .antlr/
│   │   ├── TyC.interp
│   │   ├── TyC.tokens
│   │   ├── TyCLexer.interp
│   │   ├── TyCLexer.py
│   │   ├── TyCLexer.tokens
│   │   └── TyCParser.py
│   ├── TyC.g4
│   └── lexererr.py
│
├── semantics/
│   ├── static_checker.py
│   └── static_error.py
│
└── utils/
    ├── error_listener.py
    ├── nodes.py
    └── visitor.py
```
The tree folder show all the files that must be worked on, not everything.
## Components

- **`astgen`** — Contains the AST generation implementation.
- **`codegen`** — Contains the code generation implementation and supporting utilities.
- **`grammar`** — Contains the ANTLR grammar, generated lexer/parser files, and lexer error handling.
- **`semantics`** — Contains the static checker and static error definitions.
- **`utils`** — Contains shared AST nodes, visitors, and error listeners.
