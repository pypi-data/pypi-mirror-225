# Minimon

This is just a stub for a future Readme file for minimon, the minimal monitor.

Here are some buzz-phrases:

- Minimal monitoring
- `textual`/`rich` based
- Heavy use of async programming
- `asyncssh` instead of `paramiko`
- Configuration as application
- Functional approaches wherever possible


## Installation

While you can just clone and use minimon, the intended way to use it is to install via
`pip` or run it from inside a virtual environment.

Install it locally using `pip`:

```sh
[<PYTHON> -m] pip[3] install [--user] [--upgrade] minimon
```


## Why

- async
- functional
- testability
- bullet proof


## Todo

This is very early development, no real todo-list here, yet. Some of the bigger tasks include

- [ ] provide a way to use data propagating through functions by different consumers
- [ ] provide broader set of useful data sources and handlers
- [ ] provide monadic (async) function chaining
- [ ] capture and persist metrics
- [ ] visualize metrics
- [ ] provide ways to interact
- [ ] improve logging: to file, log threads, log task context
- [ ] and error handling


## Development & Contribution

### Setup

For active development you need to have `poetry` and `pre-commit` installed

```sh
python3 -m pip install --upgrade --user poetry pre-commit
git clone git@projects.om-office.de:frans/minimon.git
cd minimon
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3
poetry install
```


### Workflow

* Create/test/commit changes and check commits via `pre-commit`
* after work is done locally:
  - adapt version in `pyproject.toml`
  - build and check a package
```sh
poetry build && \
twine check dist/* &&
python3 -m pip uninstall -y minimon && \
python3 -m pip install --user dist/minimon-$(grep -E "^version.?=" pyproject.toml | cut -d '"' -f 2)-py3-none-any.whl
```
  - check installed package
  - go through review process
  - publish the new package `poetry publish --build`
  - commit new version && push


## License

For all code contained in this repository the rules of GPLv3 apply unless
otherwise noted. That means that you can do what you want with the source
code as long as you make the files with their original copyright notice
and all modifications available.

See [GNU / GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) for details.

This project is not free for machine learning. If you're using any content
of this repository to train any sort of machine learned model (e.g. LLMs),
you agree to make the whole model trained with this repository and all data
needed to train (i.e. reproduce) the model publicly and freely available
(i.e. free of charge and with no obligation to register to any service) and
make sure to inform the author (me, frans.fuerst@protonmail.com) via email
how to get and use that model and any sources needed to train it.
