import tkinter as tk
from tkinter import ttk
import pandas as pd
import random
from faker import Faker
from datetime import datetime
import time

# ==============================
# CONFIG
# ==============================
USE_DEMO_MODE = True

fake = Faker()

DEPTS = ['WH','PD','QA','IT','HR','EN','PE','PK','CC','LM']

# ==============================
# MOCK DATA
# ==============================
def generate_mock_data(n=100):
    data = []

    for i in range(n):
        emp_id = str(1000 + i)
        name = fake.name()
        dept = random.choice(DEPTS)

        status_type = random.choice(['normal', 'absent', 'ot', 'weird'])

        if status_type == 'absent':
            punches = []

        elif status_type == 'normal':
            punches = ["08:00:00","12:00:00","13:00:00","17:00:00"]

        elif status_type == 'ot':
            punches = ["08:00:00","12:00:00","13:00:00","17:00:00","18:00:00","21:00:00"]

        else:
            punches = ["08:05:00","08:07:00","12:00:00"]  # ผิดปกติ

        punch_str = ",".join(punches)

        punch_count = len(punches)
        ot_time = 3 if punch_count >= 6 else 0

        if punch_count == 0:
            status = "❌ ขาด"
        elif ot_time >= 3:
            status = "🔴 OT"
        else:
            status = "✅ มา"

        data.append({
            "EMP_DEPT": dept,
            "EMP_ID": emp_id,
            "EMP_NAME": name,
            "STATUS": status,
            "PUNCH_COUNT": punch_count,
            "ALL": punch_str,
            "OT_TIME": ot_time
        })

    return pd.DataFrame(data)


# ==============================
# APP
# ==============================
class DemoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Factory Demo (SaaS Style)")
        self.root.geometry("1200x700")

        self.df = pd.DataFrame()

        self.build_ui()
        self.load_data()

    def build_ui(self):

        # Header
        header = tk.Frame(self.root)
        header.pack(fill="x", padx=10, pady=10)

        tk.Label(header, text="🏭 Factory Dashboard",
                 font=("Segoe UI", 18, "bold")).pack(side="left")

        self.mode_label = tk.Label(header,
            text="⚡ DEMO MODE",
            fg="orange",
            font=("Segoe UI", 10, "bold"))
        self.mode_label.pack(side="left", padx=10)

        tk.Button(header, text="🔄 Refresh",
                  command=self.load_data).pack(side="right")

        # KPI
        self.kpi_label = tk.Label(self.root, text="", font=("Segoe UI", 11))
        self.kpi_label.pack(pady=5)

        # Table
        cols = ("DEPT","ID","NAME","STATUS","PUNCH","OT")

        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.pack(fill="both", expand=True)

    def load_data(self):

        # fake loading
        self.kpi_label.config(text="Loading...")
        self.root.update()
        time.sleep(0.8)

        if USE_DEMO_MODE:
            self.df = generate_mock_data(120)

        self.render()

    def render(self):

        self.tree.delete(*self.tree.get_children())

        total = len(self.df)
        present = len(self.df[self.df['STATUS'] == "✅ มา"])
        absent = len(self.df[self.df['STATUS'] == "❌ ขาด"])
        ot = len(self.df[self.df['STATUS'] == "🔴 OT"])

        self.kpi_label.config(
            text=f"👥 {total} | ✅ {present} | ❌ {absent} | 🔴 {ot}"
        )

        for _, r in self.df.iterrows():
            self.tree.insert("", "end", values=(
                r['EMP_DEPT'],
                r['EMP_ID'],
                r['EMP_NAME'],
                r['STATUS'],
                r['PUNCH_COUNT'],
                f"{r['OT_TIME']} hr" if r['OT_TIME'] else "-"
            ))


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()