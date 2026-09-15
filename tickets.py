"""
tickets.py

Core CRUD and lifecycle logic for help desk tickets, backed by SQLite.
Simulates the ticket table structure you'd find in a real ITSM tool.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from priority import calculate_sla_due, is_breached, next_priority_up, VALID_STATUSES

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "helpdesk.db"


def get_connection():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            priority TEXT NOT NULL,
            requester TEXT,
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TEXT NOT NULL,
            sla_due_at TEXT NOT NULL,
            escalation_reason TEXT,
            resolution_notes TEXT,
            resolved_at TEXT
        )
    """)
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")


def create_ticket(title, category, priority, requester):
    now = datetime.now()
    sla_due = calculate_sla_due(priority, now)
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO tickets (title, category, priority, requester, status, created_at, sla_due_at)
           VALUES (?, ?, ?, ?, 'Open', ?, ?)""",
        (title, category, priority, requester, now.isoformat(), sla_due.isoformat()),
    )
    conn.commit()
    ticket_id = cur.lastrowid
    conn.close()
    print(f"Created ticket #{ticket_id}: [{priority}] {title} (SLA due {sla_due:%Y-%m-%d %H:%M})")
    return ticket_id


def list_tickets(status_filter=None):
    conn = get_connection()
    if status_filter and status_filter.lower() == "open":
        rows = conn.execute(
            "SELECT * FROM tickets WHERE status NOT IN ('Resolved','Closed') ORDER BY priority, created_at"
        ).fetchall()
    elif status_filter:
        rows = conn.execute(
            "SELECT * FROM tickets WHERE status = ? ORDER BY created_at", (status_filter,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM tickets ORDER BY created_at").fetchall()
    conn.close()

    for r in rows:
        breached = is_breached(datetime.fromisoformat(r["sla_due_at"]), r["status"])
        flag = " [SLA BREACHED]" if breached else ""
        print(f"#{r['id']:<3} [{r['priority']}] {r['status']:<12} {r['title']}{flag}")
    return rows


def escalate_ticket(ticket_id, reason):
    conn = get_connection()
    row = conn.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,)).fetchone()
    if not row:
        print(f"Ticket #{ticket_id} not found.")
        return
    new_priority = next_priority_up(row["priority"])
    new_sla = calculate_sla_due(new_priority, datetime.now())
    conn.execute(
        """UPDATE tickets SET priority = ?, status = 'Escalated',
           escalation_reason = ?, sla_due_at = ? WHERE id = ?""",
        (new_priority, reason, new_sla.isoformat(), ticket_id),
    )
    conn.commit()
    conn.close()
    print(f"Ticket #{ticket_id} escalated to {new_priority}. New SLA due {new_sla:%Y-%m-%d %H:%M}")


def resolve_ticket(ticket_id, notes):
    conn = get_connection()
    now = datetime.now()
    conn.execute(
        """UPDATE tickets SET status = 'Resolved', resolution_notes = ?, resolved_at = ?
           WHERE id = ?""",
        (notes, now.isoformat(), ticket_id),
    )
    conn.commit()
    conn.close()
    print(f"Ticket #{ticket_id} resolved.")


def sla_report():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM tickets WHERE status NOT IN ('Resolved','Closed')"
    ).fetchall()
    conn.close()

    now = datetime.now()
    print(f"\nSLA BREACH REPORT — generated {now:%Y-%m-%d %H:%M}")
    print("-" * 47)
    any_breach = False
    for r in rows:
        due = datetime.fromisoformat(r["sla_due_at"])
        if is_breached(due, r["status"], now):
            any_breach = True
            delta = now - due
            print(f'[ID {r["id"]}] {r["priority"]} - "{r["title"]}"')
            print(f"        SLA due: {due:%Y-%m-%d %H:%M} | BREACHED by {delta}")
    if not any_breach:
        print("No SLA breaches. All open tickets within window.")
