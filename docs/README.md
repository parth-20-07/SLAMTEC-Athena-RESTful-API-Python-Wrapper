# Welcome to MkDocs

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Requirements

To Use this Library, You will require:

- `poetry` for dependency management. Suggested Install type is system-wide. Complete Setup Guide [here](https://python-poetry.org/)
- `docker` for Remote Connection Setup. Setup Guide [here](https://docs.docker.com/engine/install/)

## Commands

- `make init` => Create a new virtual environment.
- `make setup` => Install all python dependencies from `pyproject.toml`.
- `source .venv/bin/activate && mkdocs serve` => Generate Documentation Website that can be accesses on `http://127.0.0.1:8000/`
- `make run` => Run the Test File for Project.
- `make format` => Run `black` for formatting and `ruff` for linter checking.
- `make fix` => Run Ruff Linter Fixes.
- `make clean` => Remove Virtual Environment and Cache Files.
- `make docker_run` => Spin the Docker Container for Remote Connection.
- `make docker_clean` => Stop Docker Container, Remove the Container and Image.

## Project layout

```tree
[ 238]  ./
├── [ 250]  docs/
│   ├── [  13]  API_Docs.md
│   ├── [1.1K]  README.md
│   ├── [  65]  RoboComms_Docs.md
│   ├── [892K]  Slamware Restful API Development Manual V1.1-2.pdf
│   ├── [ 196]  Utils_Docs.md
│   └── [2.2K]  VPN Setup Docker Guide.md
├── [ 108]  robotComms/
│   ├── [ 262]  api_classes/
│   │   ├── [ 252]  __init__.py
│   │   ├── [   0]  application.py
│   │   ├── [ 20K]  artifact.py
│   │   ├── [   0]  delivery.py
│   │   ├── [   0]  firmware.py
│   │   ├── [9.7K]  motion.py
│   │   ├── [   0]  multi-floor.py
│   │   ├── [2.2K]  platform.py
│   │   ├── [   0]  sensors.py
│   │   ├── [2.2K]  slam.py
│   │   ├── [1.8K]  statistics.py
│   │   └── [ 21K]  system.py
│   ├── [ 116]  utils/
│   │   ├── [ 302]  __init__.py
│   │   ├── [8.5K]  connection.py
│   │   ├── [3.1K]  logger.py
│   │   ├── [7.5K]  rest_adapter.py
│   │   └── [5.2K]  results.py
│   ├── [ 117]  __init__.py
│   ├── [   0]  __version__.py
│   └── [8.1K]  robotComms.py
├── [1.2K]  LICENSE
├── [1.1K]  Makefile
├── [ 361]  README.md
├── [  63]  ip.json
├── [1.6K]  main.py
├── [1.2K]  mkdocs.yml
├── [ 83K]  poetry.lock
├── [  46]  poetry.toml
└── [1.5K]  pyproject.toml
```

## Essential Links

### API

- Slamware RESTful API: [https://docs.slamtec.com/](https://docs.slamtec.com/)

### SDK

- ROS SDK: [https://wiki.slamtec.com/pages/viewpage.action?pageId=36208700](https://wiki.slamtec.com/pages/viewpage.action?pageId=36208700)
- C++ SDK: [https://developer.slamtec.com/docs/slamware/cpp-sdk-en/4.6.2_rtm/](https://developer.slamtec.com/docs/slamware/cpp-sdk-en/4.6.2_rtm/)

## Documentation Guide

Documentation is developed using [`mkdocs`](https://www.mkdocs.org/) and the docstring inclusion is done using [`mkdocstring`](https://mkdocstrings.github.io/)
