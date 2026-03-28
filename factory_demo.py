import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkcalendar import DateEntry

import pandas as pd
from logic import (
    generate_mock_data,
    MOCK_EMPLOYEE_COUNT,
)

# ==============================
# CONFIG
# ==============================
USE_DEMO_MODE = True


# ==============================
# APP
# ==============================
class DemoApp:

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Factory Attendance Dashboard")
        self.root.geometry("1200x720")

        self.df = pd.DataFrame()
        self.filtered_df = pd.DataFrame()

        self.build_ui()
        self.load_data()

    def build_ui(self) -> None:
        """สร้าง UI ทั้งหมด: header, filter, KPI, table"""

        # ===== HEADER =====
        header = tk.Frame(self.root)
        header.pack(fill="x", padx=15, pady=15)

        tk.Label(header, text="🏭 Factory Dashboard",
                 font=("Segoe UI", 18, "bold")).pack(side="left")

        mode = "DEMO MODE" if USE_DEMO_MODE else "LIVE MODE"
        tk.Label(header, text=f"⚡ {mode}",
                 fg="orange",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=10)

        tk.Button(header, text="📥 Export",
                  command=self.export_excel).pack(side="right", padx=5)

        tk.Button(header, text="🔄 Refresh",
                  command=self.load_data).pack(side="right", padx=5)

        # ===== FILTER =====
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(filter_frame, text="Dept:").pack(side="left")

        self.dept_var = tk.StringVar()
        self.dept_combo = ttk.Combobox(filter_frame,
                                       textvariable=self.dept_var,
                                       state="readonly",
                                       width=10)
        self.dept_combo.pack(side="left", padx=5)
        self.dept_combo.bind("<<ComboboxSelected>>",
                             lambda e: self.apply_filter())

        tk.Label(filter_frame, text="Search:").pack(side="left", padx=10)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side="left")
        search_entry.bind("<KeyRelease>",
                          lambda e: self.apply_filter())

        tk.Label(filter_frame, text="Date:").pack(side="left", padx=10)

        self.date_picker = DateEntry(filter_frame, width=12)
        self.date_picker.pack(side="left")
        self.date_picker.bind("<<DateEntrySelected>>",
                              lambda e: self.apply_filter())

        # ===== KPI =====
        self.kpi_label = tk.Label(self.root, font=("Segoe UI", 11))
        self.kpi_label.pack(pady=8)

        # ===== TABLE =====
        cols = ("DEPT", "ID", "NAME", "STATUS", "PUNCH", "OT")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.column("DEPT", width=80)
        self.tree.column("ID", width=80)
        self.tree.column("NAME", width=200)
        self.tree.column("STATUS", width=120)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data(self) -> None:
        """โหลด/รีเฟรชข้อมูลพนักงานและอัปเดต dropdown แผนก"""
        if USE_DEMO_MODE:
            self.df = generate_mock_data(MOCK_EMPLOYEE_COUNT)

        dept_list = ["ALL"] + sorted(self.df['EMP_DEPT'].unique())
        self.dept_combo['values'] = dept_list
        self.dept_combo.set("ALL")

        self.filtered_df = self.df.copy()
        self.apply_filter()

    def apply_filter(self) -> None:
        """กรองข้อมูลตาม dept, keyword และ date ที่เลือก"""
        df = self.df.copy()

        dept = self.dept_var.get()
        if dept and dept != "ALL":
            df = df[df['EMP_DEPT'] == dept]

        keyword = self.search_var.get().lower()
        if keyword:
            df = df[
                df['EMP_NAME'].str.lower().str.contains(keyword) |
                df['EMP_ID'].str.contains(keyword)
            ]

        selected_date = self.date_picker.get_date()
        df = df[df['DATE'] == selected_date]

        self.filtered_df = df
        self.render()

    def render(self) -> None:
        """อัปเดตตารางและ KPI จาก filtered_df ปัจจุบัน"""
        self.tree.delete(*self.tree.get_children())

        df = self.filtered_df
        total = len(df)
        present = len(df[df['STATUS'] == "✅ Present"])
        absent = len(df[df['STATUS'] == "❌ Absent"])
        ot = len(df[df['STATUS'] == "🔴 OT"])

        self.kpi_label.config(
            text=f"👥 Total: {total}   |   ✅ {present}   |   ❌ {absent}   |   🔴 {ot}"
        )

        for _, r in df.iterrows():
            self.tree.insert("", "end", values=(
                r['EMP_DEPT'],
                r['EMP_ID'],
                r['EMP_NAME'],
                r['STATUS'],
                r['PUNCH_COUNT'],
                f"{r['OT_TIME']} hr" if r['OT_TIME'] else "-"
            ))

    def export_excel(self) -> None:
        """Export ข้อมูลที่กรองแล้วเป็นไฟล์ Excel พร้อม error handling"""
        if self.filtered_df.empty:
            messagebox.showwarning("Warning", "No data to export")
            return

        selected_date = self.date_picker.get_date().strftime("%Y-%m-%d")
        dept = self.dept_var.get() or "ALL"
        filename = f"Attendance_{selected_date}_{dept}.xlsx"

        path = filedialog.asksaveasfilename(
            initialfile=filename,
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not path:
            return

        try:
            self.filtered_df.to_excel(path, index=False)
            messagebox.showinfo("Success", f"Saved: {filename}")
        except PermissionError:
            messagebox.showerror(
                "Export Failed",
                f"ไม่สามารถบันทึกได้ กรุณาปิดไฟล์ '{filename}' ก่อนแล้วลองใหม่"
            )
        except Exception as e:
            messagebox.showerror("Export Failed", f"เกิดข้อผิดพลาด: {e}")


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    root = tk.Tk()
    app = DemoApp(root)
    root.mainloop()
