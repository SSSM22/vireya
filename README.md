# Vireya

Vireya is a lightweight MVP scaffold for a restaurant management domain, covering billing, kitchen workflow, inventory, governance, reporting, and a simple runtime layer.

## Quick start

From the repository root:

```powershell
.\.venv\Scripts\python.exe run_demo.py --demo
```

## API server

```powershell
.\.venv\Scripts\python.exe -m vireya.api
```

Then visit:

- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/demo

## Tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
```
