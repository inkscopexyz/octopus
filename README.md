# Octopus for Ink Smart Contracts in the Polkadot Ecosystem

## Introduction

This repository is a fork of the original [FuzzingLabs/octopus](https://github.com/FuzzingLabs/octopus) project, customized and enhanced to seamlessly integrate with ink! smart contracts for the Polkadot ecosystem. Our modifications focus on optimizing the functionality for Polkadot's blockchain environment, ensuring compatibility with newer versions of Python, and introducing a security enhancement by implementing a backdoor-checking mechanism in the CLI.

## Changes Made

1. **Ink Smart Contracts Compatibility:** The core modification involves adapting the original project to support ink! smart contracts within the Polkadot ecosystem.

2. **Wasm Library Upgrade:** We replaced the original wasm library with wasm-tob to ensure compatibility with the latest versions of Python.

3. **CLI Backdoor Check:** We've introduced a backdoor-checking feature in the Command Line Interface (CLI). This enhancement enables users to scan for potential backdoors, contributing to a more secure deployment of smart contracts.

## Getting Started

- ⚠️ Requirements:
  - [python3](https://www.python.org/)
  - [poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)

To use this modified version of Octopus for Ink smart contracts in the Polkadot ecosystem, follow these steps:

1. Clone the repository and enter the directory:

```bash
https://github.com/inkscopexyz/octopus.git && cd octopus
```

2. Install the dependencies:

```bash
poetry install
```

3. Run the example backdoor check:

```bash
poetry run inkscope --file ./tests/flipper.wasm --check_backdoor
```

> ℹ️ Note: You can execute the backdoor check on any ink! smart contract by replacing the `flipper.wasm` file with the contract of your choice.

> ℹ️ Note: You can also run other commands from the original Octopus project, check them using the `--help` flag.

```bash
poetry run inkscope --help
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details