# Sample Ticket Walkthroughs

Real examples of how tickets move through the lifecycle in this system.

---

### Example 1: Critical Incident (P1)

**Scenario:** VPN is down, blocking the entire sales team from reaching
internal tools.

```bash
python3 cli.py create --category Incident --priority P1 \
  --title "VPN down for entire sales team" --requester "manager@company.com"
```

- SLA: 4 hours (Critical)
- If not resolved within SLA, `sla-report` flags it as breached
- Real-world equivalent: this would page on-call network engineering immediately

---

### Example 2: Medium Incident that needs escalation (P3 → P2)

**Scenario:** A single printer is offline. Initially low urgency, but after
24 hours with no response from facilities, it's escalated.

```bash
python3 cli.py create --category Incident --priority P3 \
  --title "Printer offline, 3rd floor" --requester "user@company.com"

# 24 hours later, still unresolved:
python3 cli.py escalate --id 2 --reason "No response from facilities in 24h"
```

- Escalating bumps priority from P3 → P2 and recalculates the SLA due time
- This mirrors how real service desks re-prioritize tickets that are aging out

---

### Example 3: Service Request (not an incident)

**Scenario:** A user requests a new monitor. Nothing is broken — this is a
**Service Request**, not an Incident.

```bash
python3 cli.py create --category "Service Request" --priority P4 \
  --title "New monitor request" --requester "user2@company.com"

python3 cli.py resolve --id 3 --notes "Approved and shipped monitor"
```

- Distinguishing Incident vs. Service Request is a core ITIL concept:
  - **Incident** = something is broken / degraded
  - **Service Request** = a standard request for something new
