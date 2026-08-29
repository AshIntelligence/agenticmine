# Ash OS · Personal Control Plane

A public-safe prototype for a persistent personal assistant that sits above inbox, calendar, money, travel, career and other life systems.

The control loop is:

**signals → context → policy → action → approval → audit**

Every item routes to one of four states:

- **HANDLE** — high-confidence, low-sensitivity, reversible work inside the autonomy boundary
- **DRAFT** — prepare the work, but do not commit it yet
- **ASK ASH** — sensitive, financially meaningful, hard-to-reverse or otherwise high-consequence action
- **WATCH** — keep state alive without interrupting the user

The core product choice is that model confidence does **not** equal execution authority. Policy remains outside the model and can require approval even when confidence is high.

## Public demo

The Streamlit page uses only synthetic scenarios. It does not connect to real email, calendar, financial accounts, credentials or travel accounts.

## Production extension

A production implementation would add secure connectors, event triggers, durable state, user-specific policies, tool execution, credential isolation, notification controls, outcome learning and auditable approvals.

**Live page:** https://ash-intelligence-lab.streamlit.app/Ash_OS
