# Minimon

This is just a stub for a future Readme file

Here are some buzz-phrases:

- Minimal monitoring
- textual/rich
- async programming
- asyncssh instead of paramiko
- Configuration as application


## Installation

While you can just clone and use minimon, the intended way to use it is via
`pip` or inside a virtual environment.

Install it locally using `pip`:

```sh
[<PYTHON> -m] pip[3] install [--user] [--upgrade] minimon
```


## Todo

TBD


## Development & Contribution

### Setup

For active development you need to have `poetry` and `pre-commit` installed

```sh
python3 -m pip install --upgrade --user poetry pre-commit
git clone git@projects.om-office.de:frans/minimon.io.git
cd minimon.io
pre-commit install
# if you need a specific version of Python inside your dev environment
poetry env use ~/.pyenv/versions/3.10.4/bin/python3
poetry install
```

### Workflow

* Create/commit changes and check commits via `pre-commit`
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
