"""
priority.py

Defines the priority levels and their associated SLA (Service Level
Agreement) resolution windows, mirroring how real ITSM tools like
ServiceNow calculate SLA due dates from a Priority Matrix
(Impact x Urgency).
"""

from datetime import datetime, timedelta

# Priority -> SLA resolution window (in hours)
SLA_HOURS = {
    "P1": 4,    # Critical - e.g. full outage, security incident
    "P2": 8,    # High - e.g. one department blocked
    "P3": 24,   # Medium - e.g. single user, workaround exists
    "P4": 72,   # Low - e.g. cosmetic issue, minor request
}

VALID_PRIORITIES = list(SLA_HOURS.keys())
VALID_CATEGORIES = ["Incident", "Service Request"]
VALID_STATUSES = ["Open", "In Progress", "Escalated", "Resolved", "Closed"]


def calculate_sla_due(priority: str, created_at: datetime) -> datetime:
    """Return the SLA due datetime for a given priority and creation time."""
    if priority not in SLA_HOURS:
        raise ValueError(f"Invalid priority '{priority}'. Must be one of {VALID_PRIORITIES}")
    return created_at + timedelta(hours=SLA_HOURS[priority])


def is_breached(sla_due_at: datetime, status: str, now: datetime = None) -> bool:
    """A ticket is breached if it's still open/in-progress past its SLA due time."""
    now = now or datetime.now()
    if status in ("Resolved", "Closed"):
        return False
    return now > sla_due_at


def next_priority_up(priority: str) -> str:
    """Used when escalating a ticket - bumps priority one level higher."""
    order = ["P4", "P3", "P2", "P1"]
    idx = order.index(priority)
    return order[min(idx + 1, len(order) - 1)]
