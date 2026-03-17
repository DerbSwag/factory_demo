# 🏭 Factory Attendance Dashboard (Demo)

A production-style attendance dashboard that simulates employee time tracking in a manufacturing environment.
Designed for portfolio demonstration, system design showcase, and interview presentation.

---

## 🚀 Overview

This project demonstrates how an attendance system processes employee punch records and generates actionable insights.

Key capabilities:

* Attendance tracking (Present / Absent / Overtime)
* Department-based filtering
* Search by employee name or ID
* Excel export for reporting
* Demo mode with realistic mock data (no database required)

---

## 🧠 Key Features

### 📊 Attendance Dashboard

* Displays employee attendance status:

  * ✅ Present
  * ❌ Absent
  * 🔴 Overtime
* KPI summary for quick insights

---

### 🔍 Filtering & Search

* Filter employees by department
* Search by name or employee ID
* Real-time update of table and KPIs

---

### 📥 Export to Excel

* Export current dataset (filtered or full)
* Useful for HR reporting and audit

### 📅 Date Selection
- Select a specific date for attendance view  
- Designed to support daily reporting workflows  

### 📥 Smart Export Naming
- Export file name automatically generated based on:
  - Selected date  
  - Selected department  
- Example: Attendance_2026-03-17_WH.xlsx

### 🎨 UI Enhancements
- Improved layout and spacing  
- Clear KPI summary display  
- Responsive filtering controls  

### ⚡ Demo Mode

* Runs without database connection
* Uses mock data designed to simulate real-world scenarios
* Safe for public GitHub and presentations
- Uses generated mock data (Faker)
- No database required
- Designed for safe demonstration and testing
---

## 🏭 Business Logic Simulation

This system uses simplified and general attendance rules.

### 🕘 Working Hours

* Standard working hours: **08:00 – 17:00**

---

### 🔴 Overtime (OT)

Overtime is calculated based on the **last recorded punch time**.

```
OT = Last Punch Time - 17:00
```

**Example:**

```id="f5qk9p"
08:00, 12:00, 13:00, 18:30
→ OT = 1.5 hours
```

---

### ❌ Absent

* No punch records → marked as Absent

---

### ⚠️ Irregular Data

* Incomplete or inconsistent punch records may be flagged
* Examples:

  * Only one punch
  * Duplicate timestamps
  * Missing expected entries

---

### 📊 Status Logic

| Condition            | Status       |
| -------------------- | ------------ |
| No records           | ❌ Absent     |
| Valid records, no OT | ✅ Present    |
| Last punch > 17:00   | 🔴 Overtime  |
| Incomplete pattern   | ⚠️ Irregular |

---

## 🧪 Demo Data Design

Mock data simulates a real organization structure:

### Departments

* Warehouse (WH)
* Production (PD, PE)
* Quality (QA, QC)
* Engineering (EN, RD)
* Office (IT, HR, AC, Sales)
* Safety (SAF)
* Purchasing (PUR)

### Scenarios Covered

* Normal working day
* Overtime work
* Absence
* Irregular punch behavior

---

## 🖥️ Tech Stack

* Python 3
* Tkinter (GUI)
* Pandas (Data processing)
* Faker (Mock data generation)

---

## 📂 Project Structure

```id="o1m6gx"
factory_demo/
│
├── factory_demo.py      # Main application (Demo mode)
├── requirements.txt
├── README.md
```

---

## ⚙️ Installation

```bash
pip install pandas faker
```

---

## ▶️ Run

```bash
python factory_demo.py
```

---

## 📸 Screenshots

(Add your UI screenshots here)

---

## 🔐 Security

* No real employee data
* No database credentials
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

---

## 👨‍💻 Author

**Natthawat Raengkom**
IT Support / System Administration / Aspiring Full Stack Developer

GitHub: https://github.com/DerbSwag

---

## ⭐ Notes

This project focuses on practical system design and business logic simulation,
bridging the gap between simple scripts and real-world enterprise applications.
