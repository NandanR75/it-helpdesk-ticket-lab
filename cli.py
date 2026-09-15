"""
cli.py

Command-line interface for the IT Help Desk & Ticket Management Lab.

Usage:
    python3 cli.py init
    python3 cli.py create --category Incident --priority P2 --title "..." --requester "..."
    python3 cli.py list [--status open|Open|Escalated|Resolved]
    python3 cli.py escalate --id 3 --reason "..."
    python3 cli.py resolve --id 3 --notes "..."
    python3 cli.py sla-report
"""

import argparse
import sys

import tickets
from priority import VALID_PRIORITIES, VALID_CATEGORIES


def main():
    parser = argparse.ArgumentParser(description="IT Help Desk & Ticket Management Lab")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init", help="Initialize the database")

    p_create = sub.add_parser("create", help="Create a new ticket")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--category", required=True, choices=VALID_CATEGORIES)
    p_create.add_argument("--priority", required=True, choices=VALID_PRIORITIES)
    p_create.add_argument("--requester", required=True)

    p_list = sub.add_parser("list", help="List tickets")
    p_list.add_argument("--status", default=None)

    p_esc = sub.add_parser("escalate", help="Escalate a ticket")
    p_esc.add_argument("--id", required=True, type=int)
    p_esc.add_argument("--reason", required=True)

    p_res = sub.add_parser("resolve", help="Resolve a ticket")
    p_res.add_argument("--id", required=True, type=int)
    p_res.add_argument("--notes", required=True)

    sub.add_parser("sla-report", help="Show SLA breach report")

    args = parser.parse_args()

    if args.command == "init":
        tickets.init_db()
    elif args.command == "create":
        tickets.create_ticket(args.title, args.category, args.priority, args.requester)
    elif args.command == "list":
        tickets.list_tickets(args.status)
    elif args.command == "escalate":
        tickets.escalate_ticket(args.id, args.reason)
    elif args.command == "resolve":
        tickets.resolve_ticket(args.id, args.notes)
    elif args.command == "sla-report":
        tickets.sla_report()


if __name__ == "__main__":
    sys.exit(main())
