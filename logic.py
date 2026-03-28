"""Business logic สำหรับระบบ Attendance: คำนวณ OT และกำหนด status พนักงาน"""

import pandas as pd
from datetime import datetime, time, timedelta
import random
from faker import Faker

# ==============================
# CONFIG
# ==============================
WORK_START: time = time(8, 0)           # เวลาเริ่มงาน 08:00
WORK_END: time = time(17, 0)            # เวลาเลิกงาน 17:00
MOCK_DATE_RANGE_DAYS: int = 7           # จำนวนวันย้อนหลังสำหรับ mock data
MOCK_EMPLOYEE_COUNT: int = 40           # จำนวนพนักงาน mock

fake = Faker()

DEPTS: list[str] = [
    'WH', 'PD', 'PE', 'QA', 'QC',
    'EN', 'RD',
    'IT', 'HR', 'AC', 'CS',
    'PUR', 'SAF'
]


def calculate_ot(all_str: str) -> float:
    """คำนวณชั่วโมง OT จาก punch string

    Args:
        all_str: string ของเวลา punch คั่นด้วย comma เช่น "08:00:00,12:00:00,13:00:00,18:30:00"

    Returns:
        จำนวนชั่วโมง OT (ทศนิยม 1 ตำแหน่ง) หรือ 0 ถ้าไม่มี OT
    """
    if not all_str:
        return 0

    times = [datetime.strptime(t, "%H:%M:%S") for t in all_str.split(",") if t]

    if not times:
        return 0

    last_time = times[-1].time()

    if last_time > WORK_END:
        delta = datetime.combine(datetime.today(), last_time) - \
                datetime.combine(datetime.today(), WORK_END)
        return round(delta.total_seconds() / 3600, 1)

    return 0


def process_row(row: pd.Series) -> pd.Series:
    """กำหนดสถานะการเข้างานของพนักงานแต่ละคน

    Args:
        row: แถวข้อมูลพนักงานที่มี column 'ALL' เป็น punch string

    Returns:
        pd.Series ของ [punch_count, ot_time, status]
    """
    punches = row['ALL'].split(',') if row['ALL'] else []
    count = len(punches)
    ot = calculate_ot(row['ALL'])

    if count == 0:
        status = "❌ Absent"
    elif count < 2:
        status = "⚠️ Irregular"
    elif ot > 0:
        status = "🔴 OT"
    else:
        status = "✅ Present"

    return pd.Series([count, ot, status])


def generate_mock_data(n: int = MOCK_EMPLOYEE_COUNT) -> pd.DataFrame:
    """สร้างข้อมูลพนักงานและบันทึกการเข้างานแบบ mock สำหรับ demo

    Args:
        n: จำนวนพนักงานที่ต้องการสร้าง

    Returns:
        DataFrame มี columns: EMP_DEPT, EMP_ID, EMP_NAME, DATE, ALL, PUNCH_COUNT, OT_TIME, STATUS
    """
    data = []
    today = datetime.today().date()

    for i in range(n):
        emp_id = str(1000 + i)
        name = fake.name()
        dept = random.choice(DEPTS)
        date = today - timedelta(days=random.randint(0, MOCK_DATE_RANGE_DAYS - 1))

        pattern = random.choice(['normal', 'ot', 'absent', 'irregular'])

        if pattern == 'absent':
            punches = []
        elif pattern == 'normal':
            punches = ["08:00:00", "12:00:00", "13:00:00", "17:00:00"]
        elif pattern == 'ot':
            punches = ["08:00:00", "12:00:00", "13:00:00", "18:30:00"]
        else:
            punches = ["08:05:00"]  # irregular

        data.append({
            "EMP_DEPT": dept,
            "EMP_ID": emp_id,
            "EMP_NAME": name,
            "DATE": date,
            "ALL": ",".join(punches)
        })

    df = pd.DataFrame(data)
    df[['PUNCH_COUNT', 'OT_TIME', 'STATUS']] = df.apply(process_row, axis=1)

    return df
