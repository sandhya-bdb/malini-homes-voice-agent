"""Lead storage for Malini Voice.

Every booking inquiry or escalation is saved so the host team actually sees it:
- Always appended to a local CSV (data/leads.csv) as a backup.
- Also appended to a Google Sheet when GOOGLE_SHEET_ID and
  GOOGLE_SERVICE_ACCOUNT_FILE are set in .env.

A Sheet failure never breaks the call: the guest still gets their reference
number and the lead is still in the CSV.
"""

import csv
import secrets
import threading
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from config import settings

IST = ZoneInfo("Asia/Kolkata")

LEAD_COLUMNS = [
    "ticket_id",
    "created_at_ist",
    "type",
    "guest_name",
    "phone",
    "property",
    "check_in",
    "check_out",
    "guests",
    "notes",
    "status",
]

_lock = threading.Lock()
_sheet = None


def new_ticket_id() -> str:
    """Short reference number the guest can read out over the phone."""
    return f"MALINI-{secrets.randbelow(100000):05d}"


def _get_sheet():
    """Open the first worksheet of the configured Google Sheet (cached)."""
    global _sheet
    if _sheet is not None:
        return _sheet
    if not (settings.google_sheet_id and settings.google_service_account_file):
        return None

    import gspread  # imported lazily so the agent runs without it

    client = gspread.service_account(filename=settings.google_service_account_file)
    ws = client.open_by_key(settings.google_sheet_id).sheet1
    if not ws.row_values(1):
        ws.append_row(LEAD_COLUMNS)
    _sheet = ws
    return _sheet


def _append_csv(row: list[str]) -> None:
    path = Path(settings.leads_csv_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(LEAD_COLUMNS)
        writer.writerow(row)


def save_lead(lead_type: str, **fields: str) -> str:
    """Save a lead and return its ticket id."""
    ticket_id = new_ticket_id()
    record = {
        "ticket_id": ticket_id,
        "created_at_ist": datetime.now(IST).strftime("%Y-%m-%d %H:%M"),
        "type": lead_type,
        "status": "NEW",
        **fields,
    }
    row = [str(record.get(col, "")) for col in LEAD_COLUMNS]

    with _lock:
        _append_csv(row)
        try:
            sheet = _get_sheet()
            if sheet is not None:
                sheet.append_row(row, value_input_option="USER_ENTERED")
        except Exception as exc:  # never let storage errors reach the guest
            print(f"[LEADS] Google Sheet write failed, saved to CSV only: {exc}", flush=True)

    print(f"[LEAD] {lead_type} {ticket_id} {fields}", flush=True)
    return ticket_id
