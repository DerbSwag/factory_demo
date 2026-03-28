# 🏭 Factory Attendance Dashboard (Demo)

A production-style attendance dashboard that simulates employee time tracking in a manufacturing environment.
Designed for portfolio demonstration, system design showcase, and interview presentation.

---

## 🚀 Overview

This project demonstrates how an attendance system processes employee punch records and generates actionable insights.

Key capabilities:

* Attendance tracking (Present / Absent / Overtime / Irregular)
* Department-based filtering
* Date-based filtering (last 7 days)
* Search by employee name or ID
* Excel export with error handling
* Demo mode with realistic mock data (no database required)

---

## 🧠 Key Features

### 📊 Attendance Dashboard

* Displays employee attendance status:

  * ✅ Present
  * ❌ Absent
  * 🔴 Overtime (OT)
  * ⚠️ Irregular
* Real-time KPI summary: Total / Present / Absent / OT

---

### 🔍 Filtering & Search

* Filter by department
* Filter by date (calendar picker — connected to data)
* Search by employee name or ID
* All filters work together in real-time

---

### 📅 Smart Export

* Export filtered data to Excel (`.xlsx`)
* Filename auto-generated: `Attendance_{date}_{dept}.xlsx`
* Error handling for locked files and write failures

---

### ⚡ Demo Mode

* Runs without database connection
* Generates 40 mock employees with random attendance patterns
* Data spans last 7 days for realistic date filtering
* Safe for public GitHub and presentations

---

## 🏭 Business Logic

### 🕘 Working Hours

Configured as constants in `logic.py`:

```python
WORK_START = time(8, 0)   # 08:00
WORK_END   = time(17, 0)  # 17:00
```

### 🔴 Overtime (OT)

Calculated from the **last recorded punch time**:

```
OT = Last Punch Time - 17:00
```

Example:

```
08:00, 12:00, 13:00, 18:30  →  OT = 1.5 hours
```

### 📊 Status Logic

| Condition            | Status        |
|----------------------|---------------|
| No records           | ❌ Absent     |
| Only 1 punch         | ⚠️ Irregular  |
| Last punch > 17:00   | 🔴 OT         |
| Valid records, no OT | ✅ Present    |

---

## 🧪 Demo Data

Mock data simulates a real organization with 13 departments:

| Group       | Departments         |
|-------------|---------------------|
| Warehouse   | WH                  |
| Production  | PD, PE              |
| Quality     | QA, QC              |
| Engineering | EN, RD              |
| Office      | IT, HR, AC, CS      |
| Purchasing  | PUR                 |
| Safety      | SAF                 |

Punch patterns generated:

* **Normal** — 4 punches, no OT
* **OT** — 4 punches, last punch after 17:00
* **Absent** — no punches
* **Irregular** — single punch only

---

## 🖥️ Tech Stack

| Component      | Technology          |
|----------------|---------------------|
| Language       | Python 3.11+        |
| GUI            | Tkinter + tkcalendar|
| Data           | Pandas >= 2.0       |
| Mock Data      | Faker >= 24.0       |
| Excel Export   | openpyxl >= 3.1     |
| Testing        | pytest >= 8.0       |

---

## 📂 Project Structure

```
factory_demo/
├── factory_demo.py       # GUI application (Tkinter)
├── logic.py              # Business logic: OT calculation, status, mock data
├── requirements.txt      # Dependencies
├── tests/
│   ├── __init__.py
│   └── test_logic.py     # Unit tests (12 tests)
└── README.md
```

---

## ⚙️ Installation

```bash
pip install -r requirements.txt
```

---

## ▶️ Run

```bash
python factory_demo.py
```

---

## 🧪 Run Tests

```bash
pytest tests/ -v
```

Expected output: **12 passed**

---

## 📸 Screenshots

(Add your UI screenshots here)

---

## 🔐 Security

* No real employee data
* No database credentials
* No API keys
* Fully safe for public sharing

---

## 💡 Use Cases

* Developer portfolio project
* IT / Software Engineer interview demo
* HR system prototype
* Desktop application showcase

---

## 🧭 Future Improvements

* Web version (FastAPI / React)
* Role-based access control
* Real database integration
* Advanced analytics (charts, trends)
* Shift-based attendance tracking
* Logging and audit trail

---

## 👨‍💻 Author

**Natthawat Raengkom**
IT Support / System Administration / Aspiring Full Stack Developer

GitHub: https://github.com/DerbSwag
