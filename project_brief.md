# My agent: ShiftHandoverAgent (L1.5 IT Operations Handover Assistant)
One-liner: A conversational agent that helps L1.5 IT support engineers maintain 24/7 operations continuity between shifts by aggregating incidents, SLAs, runbooks, and pending actions into prioritized handover summaries and visual dashboards.

Tool coverage:
- Memory: Remembers prior shift context, operator notes, recurring incident patterns, and unresolved handoff tasks across sessions using Vertex AI Memory Bank.
- Tools:
  - `get_incidents(status, severity)`: Fetches active, resolved, or recurring P1-P4 incidents with SLA countdowns.
  - `get_runbook(topic)`: Retrieves step-by-step SOPs and runbook procedures for incident mitigation.
  - `get_pending_actions()`: Returns pending L1.5/L2/L3 handoff tasks and open approvals.
  - `calculate_sla_risk()`: Evaluates MTTR and calculates percentage risk of SLA breach.
  - `create_handover_report(summary, critical_items, pending_tasks)`: Logs and saves the final shift handover report.
- Catalog/UI: Renders incident priority tables, approaching SLA warnings, and pending action checklists as rich A2UI cards.
- Image gen: Generates visual shift summary dashboards (e.g., system status topology and SLA heatmaps).
- Sandbox: Computes incident MTTR statistics and SLA breach probabilities.

Recommended for every project: memory, storage, tools, image generation, A2UI
Agent-specific / stretch: Python code execution for SLA risk math, Vertex AI Memory Bank for cross-shift history.
