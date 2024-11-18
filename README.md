# FFDecks

## SETUP

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements_linter.txt
pre-commit install
cp git-hook-commit-msg .git/hooks/commit-msg
```
## RUN APPLICATION

```bash
python3 main.py
```