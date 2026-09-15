# IT Help Desk & Ticket Management Lab

A command-line ticket management system built to practice core IT Service
Management (ITSM) concepts: ticket intake, prioritization, SLA tracking,
and escalation — the same workflow used in tools like ServiceNow and Jira
Service Management.

## Why this project

Entry-level IT Support / Help Desk roles are built around one core skill:
turning a vague user complaint into a properly classified, prioritized,
and tracked ticket, then resolving it within SLA. This lab simulates that
workflow end-to-end using Python + SQLite so the logic (not just the UI)
is visible and testable.

## Features

- **Create tickets** with category (Incident / Service Request), priority
  (P1–P4), and short description
- **Auto-calculated SLA due time** based on priority
  - P1 (Critical): 4 hours
  - P2 (High): 8 hours
  - P3 (Medium): 24 hours
  - P4 (Low): 72 hours
- **List / filter tickets** by status, priority, or SLA breach
- **Escalate** a ticket (bumps priority, logs escalation reason and timestamp)
- **Resolve** a ticket (logs resolution notes and time-to-resolve)
- **SLA breach report** — flags any open ticket past its due time

## ITSM concepts practiced

| Concept | Where it shows up |
|---|---|
| Incident vs. Service Request | `category` field on ticket creation |
| Priority matrix (Impact x Urgency) | `priority.py` |
| SLA | `sla_due_at` calculation + breach report |
| Escalation | `escalate_ticket()` in `tickets.py` |
| Ticket lifecycle (New → In Progress → Resolved → Closed) | `status` field |

## Project structure

```
it-helpdesk-ticket-lab/
├── scripts/
│   ├── tickets.py          # Core ticket CRUD + SLA logic
│   ├── priority.py         # Priority/SLA rules
│   └── cli.py              # Command-line interface
├── data/
│   └── helpdesk.db         # SQLite DB (created on first run)
├── docs/
│   └── sample_tickets.md   # Example ticket walkthroughs
└── README.md
```

## Setup

```bash
git clone https://github.com/NandanR75/it-helpdesk-ticket-lab.git
cd it-helpdesk-ticket-lab
python3 scripts/cli.py init          # creates the database
```

## Usage

```bash
# Create a ticket
python3 scripts/cli.py create --category Incident --priority P2 \
  --title "Outlook not syncing" --requester "jane.doe@company.com"

# List all open tickets
python3 scripts/cli.py list --status open

# Check for SLA breaches
python3 scripts/cli.py sla-report

# Escalate a ticket
python3 scripts/cli.py escalate --id 3 --reason "No response from user in 24h"

# Resolve a ticket
python3 scripts/cli.py resolve --id 3 --notes "Reset Outlook profile, confirmed sync working"
```

## Example output

```
$ python3 scripts/cli.py sla-report

SLA BREACH REPORT — generated 2026-09-15 10:30
-----------------------------------------------
[ID 4] P1 - "VPN down for entire sales team"
        SLA due: 2026-09-15 08:00 | BREACHED by 2h 30m

[ID 7] P3 - "Printer offline, 3rd floor"
        SLA due: 2026-09-15 14:00 | OK (3h 30m remaining)
```

## What I'd add next

- Web UI (Flask) instead of CLI
- Email notifications on SLA breach
- Basic reporting dashboard (tickets by category/priority over time)
