<p align="center">
    <img alt="Latitude55" src="https://res.cloudinary.com/latitude55/image/upload/v1634117961/logo-light.svg" width="210" />
</p>
<h1 align="center">
Latitude55 Cli
</h1>

CLI tool for managing general development tasks.

## Getting Started

Requirements:

- [Poetry](https://python-poetry.org/)

### Development

```bash
poetry shell
poetry install
pre-commit install
poetry run latitude55 --help
```

### Build

```bash
poetry shell
poetry build
```

### Generate requirements.txt

```bash
poetry shell
poetry export -f requirements.txt --output requirements.txt
```

### Creating a release

```bash
poetry shell
poetry version <patch, minor, major>
git commit -m "Release v<Version>"
// After Merge
git tag -a v<Version> -m "release v<Version>"
```
