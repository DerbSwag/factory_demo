import pytest
import pandas as pd
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from logic import calculate_ot, process_row, WORK_END


# ==============================
# calculate_ot
# ==============================
class TestCalculateOt:

    def test_no_punches_returns_zero(self):
        assert calculate_ot("") == 0

    def test_normal_shift_no_ot(self):
        """ออกงานตรงเวลา 17:00 ไม่มี OT"""
        assert calculate_ot("08:00:00,12:00:00,13:00:00,17:00:00") == 0

    def test_ot_one_and_half_hours(self):
        """ออกงาน 18:30 → OT = 1.5 ชั่วโมง"""
        assert calculate_ot("08:00:00,12:00:00,13:00:00,18:30:00") == 1.5

    def test_ot_one_hour(self):
        """ออกงาน 18:00 → OT = 1.0 ชั่วโมง"""
        assert calculate_ot("08:00:00,12:00:00,13:00:00,18:00:00") == 1.0

    def test_left_early_no_ot(self):
        """ออกงานก่อน 17:00 ไม่มี OT"""
        assert calculate_ot("08:00:00,12:00:00,13:00:00,16:00:00") == 0

    def test_single_punch_no_ot(self):
        """punch เดียว ไม่ถึง 17:00 ไม่มี OT"""
        assert calculate_ot("08:05:00") == 0

    def test_ot_uses_last_punch_only(self):
        """OT คำนวณจาก punch สุดท้ายเท่านั้น"""
        assert calculate_ot("18:00:00,08:00:00") == 0  # สุดท้ายคือ 08:00


# ==============================
# process_row
# ==============================
class TestProcessRow:

    def _make_row(self, punches: list[str]) -> pd.Series:
        return pd.Series({"ALL": ",".join(punches)})

    def test_absent_when_no_punches(self):
        result = process_row(self._make_row([]))
        assert result[2] == "❌ Absent"
        assert result[0] == 0

    def test_irregular_when_single_punch(self):
        result = process_row(self._make_row(["08:05:00"]))
        assert result[2] == "⚠️ Irregular"
        assert result[0] == 1

    def test_present_when_normal_shift(self):
        result = process_row(self._make_row(["08:00:00", "12:00:00", "13:00:00", "17:00:00"]))
        assert result[2] == "✅ Present"
        assert result[0] == 4
        assert result[1] == 0

    def test_ot_when_last_punch_after_work_end(self):
        result = process_row(self._make_row(["08:00:00", "12:00:00", "13:00:00", "18:30:00"]))
        assert result[2] == "🔴 OT"
        assert result[1] == 1.5

    def test_punch_count_matches_input(self):
        result = process_row(self._make_row(["08:00:00", "12:00:00"]))
        assert result[0] == 2
