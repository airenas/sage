# sage

![Python](https://github.com/airenas/sage/workflows/Python/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/airenas/sage/badge.svg?branch=main)](https://coveralls.io/github/airenas/sage?branch=main) ![CodeQL](https://github.com/airenas/sage/workflows/CodeQL/badge.svg)

Demonstration for voice to voice bot

## Requirements

Python >= 3.10

## Installation

1. Create and activate new environment
2. Install dependencies:

```sh
pip install -r requirements.txt
```

## Testing

1. Install test dependencies:

```sh
pip install -r requirements_test.txt
```

2. Run test

```sh
make test
```

## Running

1. Start the bot:

```sh
make run
```

It will try to open and listen to a local port 8007.

2. Open GUI https://sinteze-test.intelektika.lt/sage/, it will try to connect to `http://localhost:8007`.
3. If connected do play.

---

## License

Copyright © 2022, [Airenas Vaičiūnas](https://github.com/airenas).

Released under the [The 3-Clause BSD License](LICENSE).

---
