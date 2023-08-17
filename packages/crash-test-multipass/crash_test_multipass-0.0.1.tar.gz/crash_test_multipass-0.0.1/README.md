# Crashtest

<p align="center">
    <img src="./images/crash_test_dummy.png" alt="crash_test_dummy" height="350"/>
</p>

- [Description](#description)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)

## Description

Crashtest is a command-line tool to create a [Multipass](https://multipass.run/) instance and transfer a project to test
to the newly created instance.

## Requirements

- Python 3
- [Multipass](https://multipass.run/)

## Installation

```console
$ pip install crash-test-multipass
```

## Usage

#### Create a new instance and transfer a project

```console
$ crashtest --instance-name INSTANCE_NAME --project PROJECT
```

#### Delete the instance after finishing to test

```console
$ crashtest --instance-name INSTANCE_NAME --project PROJECT --delete
```

## Contributing

If you would like to contribute to this project just create a pull request which I will try to review as soon as
possible.
