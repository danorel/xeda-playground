# xeda

### Prerequisite

- Python: 3.8.15
- Jupyter Notebook: 6.4.12

### Environment

1. Install python virtual environment:

```shell
pyenv virtualenv 3.8.15 xeda_3.8.15
```

2. Activate python virtual env

```shell
pyenv activate xeda_3.8.15
```

3. Install python dependencies from requirements.txt:

```shell
pip install -r requirements.txt
```

4. Setup `pre-commit` to make hook with `.git`:

```shell
pre-commit install
pre-commit run --all-files
```

### Vim/NeoVim users:

5. Install pynvim to enable coc:

```shell
python -m pip install --upgrade pynvim
```
