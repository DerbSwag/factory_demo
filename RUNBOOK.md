# RUNBOOK — factory_demo

> Factory Attendance Dashboard (Portfolio project)
> Updated: 2026-06-15

## Quick Reference

| Item | Value |
|------|-------|
| Language | Python (Tkinter) |
| Features | OT calculation, department filtering, Excel export |
| Tests | 12 unit tests |

---

## Procedures

### 1. Run Application

```bash
python main.py
```

### 2. Run Tests

```bash
python -m pytest tests/
```

### 3. Troubleshooting

| Symptom | Fix |
|---------|-----|
| Tkinter not found | Install: `apt install python3-tk` (Linux) or reinstall Python with tk (Windows) |
| Excel export fails | `pip install openpyxl` |
| Test failures | Check Python version ≥3.8 |

---

## Related Docs

- `README.md` — features and screenshots
