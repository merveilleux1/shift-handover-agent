# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0

"""Comprehensive 30-Day Synthetic IT Operations Data for L1.5 Shift Handover Agent.
Covers date range: 2026-09-05 to 2026-10-05 across microservices, incidents, runbooks, and shift histories.
"""

INCIDENTS = [
    {
        "id": "INC-1092",
        "title": "Payment Gateway Timeout Spikes",
        "severity": "P1",
        "status": "Active",
        "service": "Payments API",
        "assigned_to": "L1.5 Operations / L2 Payments Team",
        "opened_at": "2026-10-05T04:15:00Z",
        "sla_deadline": "2026-10-05T08:15:00Z",
        "summary": "Intermittent 504 timeouts on /v2/charge endpoint. 3.2% error rate.",
        "actions_taken": "Restarted pod instances, scaled replica count to 12. Failover to secondary provider prepared.",
        "pending_action": "Monitor payment gateway error rates; execute runbook RB-PAY-02 if error rate exceeds 5%."
    },
    {
        "id": "INC-1088",
        "title": "Auth Service Redis Cache Memory Warning",
        "severity": "P2",
        "status": "Active",
        "service": "Authentication",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-10-05T05:30:00Z",
        "sla_deadline": "2026-10-05T09:30:00Z",
        "summary": "Redis cache memory utilization reached 88%.",
        "actions_taken": "Evicted expired keys and increased maxmemory limit.",
        "pending_action": "Verify cache memory stability after shift change."
    },
    {
        "id": "INC-1085",
        "title": "Customer Notification Queue Backlog",
        "severity": "P3",
        "status": "Resolved",
        "service": "Notification Worker",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-10-05T02:00:00Z",
        "sla_deadline": "2026-10-05T10:00:00Z",
        "summary": "Queue depth peaked at 45,000 messages due to rate limiting from SMS gateway.",
        "actions_taken": "Drained queue via batch consumer workers. Backlog resolved at 06:10 UTC.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1070",
        "title": "Database Connection Pool Exhaustion on Batch Jobs",
        "severity": "P2",
        "status": "Recurring",
        "service": "Order Processing DB",
        "assigned_to": "L2 Database Engineering",
        "opened_at": "2026-10-04T23:00:00Z",
        "sla_deadline": "2026-10-05T11:00:00Z",
        "summary": "Recurring thread pool lock during night batch runs at 23:00 and 03:00 UTC.",
        "actions_taken": "Increased pool size to 150 connections. Escalated bug ticket DB-402 to L3.",
        "pending_action": "Review L3 DB patch status during morning standup."
    },
    {
        "id": "INC-1065",
        "title": "CDN Edge SSL Certificate Expiration Warning",
        "severity": "P2",
        "status": "Active",
        "service": "CDN & Static Assets",
        "assigned_to": "L1.5 Operations / Security Infra",
        "opened_at": "2026-10-04T18:00:00Z",
        "sla_deadline": "2026-10-05T18:00:00Z",
        "summary": "Wildcard SSL certificate for *.assets.domain.com expires in 48 hours.",
        "actions_taken": "Generated renewal CSR and requested auto-issuance via ACME bot.",
        "pending_action": "Verify TLS handshake validation after automated cert deployment."
    },
    {
        "id": "INC-1062",
        "title": "Search Indexing Ingestion Lag",
        "severity": "P3",
        "status": "Resolved",
        "service": "Search Service",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-10-03T14:20:00Z",
        "sla_deadline": "2026-10-03T22:20:00Z",
        "summary": "Elasticsearch indexing lag increased to 18 minutes for new product catalog updates.",
        "actions_taken": "Triggered cluster rebalance via RB-SRCH-05 and allocated 2 additional worker nodes.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1058",
        "title": "Kafka Partition Rebalance Failure on Payment Stream",
        "severity": "P1",
        "status": "Resolved",
        "service": "Kafka Event Streaming",
        "assigned_to": "L2 Platform Engineering",
        "opened_at": "2026-10-02T09:10:00Z",
        "sla_deadline": "2026-10-02T13:10:00Z",
        "summary": "Consumer group 'pay-reconcile-v1' stuck in continuous rebalance loop.",
        "actions_taken": "Increased max.poll.interval.ms and restarted consumer group pods.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1052",
        "title": "Billing Engine Hourly Settlement Delay",
        "severity": "P2",
        "status": "Active",
        "service": "Billing Engine",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-10-01T21:45:00Z",
        "sla_deadline": "2026-10-02T01:45:00Z",
        "summary": "Hourly merchant settlement job lagging by 2.5 hours due to database lock contention.",
        "actions_taken": "Terminated long-running query lock process. Executed RB-BILL-02.",
        "pending_action": "Confirm settlement reconciliation output matches ledger totals."
    },
    {
        "id": "INC-1048",
        "title": "Inventory Sync Deadlock on ERP Integration",
        "severity": "P3",
        "status": "Resolved",
        "service": "Inventory Sync",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-09-29T11:00:00Z",
        "sla_deadline": "2026-09-29T19:00:00Z",
        "summary": "ERP SOAP endpoint timeout causing inventory update retry loops.",
        "actions_taken": "Fallback to batch CSV ingestion mode.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1040",
        "title": "API Gateway High Latency Spikes during Flash Sale",
        "severity": "P1",
        "status": "Resolved",
        "service": "API Gateway",
        "assigned_to": "L1.5 Operations / SRE",
        "opened_at": "2026-09-25T16:00:00Z",
        "sla_deadline": "2026-09-25T20:00:00Z",
        "summary": "API Gateway latency spiked to 1400ms under 45,000 RPS surge.",
        "actions_taken": "Applied rate limiting rules and enabled Cloud CDN edge caching.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1035",
        "title": "Cart Service Memory Leak on Pod Restart",
        "severity": "P2",
        "status": "Resolved",
        "service": "Cart Service",
        "assigned_to": "L2 Core Backend",
        "opened_at": "2026-09-22T08:30:00Z",
        "sla_deadline": "2026-09-22T16:30:00Z",
        "summary": "Cart service pod memory climbing continuously until OOM kill.",
        "actions_taken": "Deployed hotfix v2.4.1 fixing unclosed HTTP response body leaks.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1025",
        "title": "Recommendation Engine Model Inference Latency Spikes",
        "severity": "P2",
        "status": "Resolved",
        "service": "Recommendation ML API",
        "assigned_to": "L2 ML Ops",
        "opened_at": "2026-09-18T19:15:00Z",
        "sla_deadline": "2026-09-19T03:15:00Z",
        "summary": "p99 latency reached 850ms on recommendation queries.",
        "actions_taken": "Switched model serving instance to GPU-accelerated node pool.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1020",
        "title": "Auth OAuth Token Expiry Validation Bug",
        "severity": "P1",
        "status": "Resolved",
        "service": "Authentication",
        "assigned_to": "L2 Security / L1.5 Ops",
        "opened_at": "2026-09-15T10:00:00Z",
        "sla_deadline": "2026-09-15T14:00:00Z",
        "summary": "Valid JWT tokens rejected prematurely due to NTP time drift across worker nodes.",
        "actions_taken": "Resynced chrony NTP service on cluster nodes; updated clock skew tolerance.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1015",
        "title": "Kubernetes Ingress Controller Pod OOM Kills",
        "severity": "P2",
        "status": "Resolved",
        "service": "Ingress Router",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-09-12T03:45:00Z",
        "sla_deadline": "2026-09-12T11:45:00Z",
        "summary": "NGINX Ingress controller crashed due to memory limit reached.",
        "actions_taken": "Increased memory limits from 2Gi to 4Gi.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1010",
        "title": "Order Processing DB Deadlock during Nightly Cleanup",
        "severity": "P2",
        "status": "Resolved",
        "service": "Order Processing DB",
        "assigned_to": "L2 Database Engineering",
        "opened_at": "2026-09-10T01:30:00Z",
        "sla_deadline": "2026-09-10T09:30:00Z",
        "summary": "Foreign key lock escalation during table partition pruning.",
        "actions_taken": "Rescheduled cleanup job to low-traffic window (04:00 UTC).",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1005",
        "title": "Email Notification Provider API Rate Limit Exceeded",
        "severity": "P3",
        "status": "Resolved",
        "service": "Notification Worker",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-09-08T12:00:00Z",
        "sla_deadline": "2026-09-08T20:00:00Z",
        "summary": "SendGrid API quota throttled 429 Too Many Requests.",
        "actions_taken": "Upgraded SendGrid tier package and enabled transactional priority queue.",
        "pending_action": "None (Resolved)."
    },
    {
        "id": "INC-1001",
        "title": "Payment Gateway Sandbox Environment Outage",
        "severity": "P4",
        "status": "Resolved",
        "service": "Payments API (Sandbox)",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-09-05T08:00:00Z",
        "sla_deadline": "2026-09-06T08:00:00Z",
        "summary": "Dev/Staging sandbox mock payment provider unresponsive.",
        "actions_taken": "Redeployed sandbox stub container.",
        "pending_action": "None (Resolved)."
    }
]

RUNBOOKS = {
    "payment": {
        "id": "RB-PAY-02",
        "title": "Payment Gateway Failover & Circuit Breaker SOP",
        "steps": [
            "1. Verify error rate metric on Grafana dashboard 'Payments Overview'.",
            "2. If error rate > 5% for 5 mins, enable Circuit Breaker: `kubectl exec -it pay-service -- toggle-breaker --enable`.",
            "3. Notify L2 Payments Escalation Lead on PagerDuty.",
            "4. Verify traffic failover to Secondary Processor B."
        ]
    },
    "redis": {
        "id": "RB-AUTH-01",
        "title": "Auth Cache Memory Overflow Mitigation",
        "steps": [
            "1. Check memory status: `redis-cli info memory`.",
            "2. Run key eviction script: `python3 /opt/scripts/evict_expired.py`.",
            "3. If usage remains > 90%, initiate cluster node expansion."
        ]
    },
    "database": {
        "id": "RB-DB-04",
        "title": "Database Connection Pool Exhaustion Recovery",
        "steps": [
            "1. Identify long-running transactions: `SELECT * FROM pg_stat_activity WHERE state = 'active'`.",
            "2. Kill idle-in-transaction sessions exceeding 300 seconds.",
            "3. Alert L2 DB engineering if lock count exceeds threshold."
        ]
    },
    "kafka": {
        "id": "RB-KAFKA-01",
        "title": "Kafka Consumer Group Lag Recovery",
        "steps": [
            "1. Check consumer lag: `kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group pay-reconcile-v1`.",
            "2. Scale consumer deployment replicas: `kubectl scale deployment pay-reconcile-consumer --replicas=8`.",
            "3. Monitor lag reduction until lag < 500 records."
        ]
    },
    "cdn": {
        "id": "RB-CDN-03",
        "title": "CDN Edge Cache Purge & SSL Certificate Renewal",
        "steps": [
            "1. Check SSL validity: `curl -vI https://assets.domain.com`.",
            "2. Execute ACME certificate renewal script.",
            "3. Purge edge cache tags for static asset paths."
        ]
    },
    "billing": {
        "id": "RB-BILL-02",
        "title": "Billing Settlement Reconciliation Recovery",
        "steps": [
            "1. Query locked transactions: `SELECT * FROM settlement_locks WHERE status = 'LOCKED'`.",
            "2. Release stale transaction locks older than 1 hour.",
            "3. Rerun hourly settlement cron job."
        ]
    },
    "search": {
        "id": "RB-SRCH-05",
        "title": "Elasticsearch Index Rebalance & Shard Allocation",
        "steps": [
            "1. Check cluster health: `curl -X GET 'localhost:9200/_cluster/health'`.",
            "2. Unassign unassigned shards: `POST /_cluster/reroute?retry_failed=true`.",
            "3. Monitor cluster green status."
        ]
    }
}

PENDING_ACTIONS = [
    {
        "action_id": "ACT-301",
        "incident_id": "INC-1092",
        "priority": "HIGH",
        "assigned_team": "Incoming Shift (L1.5)",
        "description": "Monitor Payment Gateway error rate every 15 minutes. Execute RB-PAY-02 if error rate > 5%.",
        "due_by": "2026-10-05T08:15:00Z"
    },
    {
        "action_id": "ACT-302",
        "incident_id": "INC-1088",
        "priority": "MEDIUM",
        "assigned_team": "Incoming Shift (L1.5)",
        "description": "Verify Redis memory metric remains below 85% utilization after key eviction.",
        "due_by": "2026-10-05T09:30:00Z"
    },
    {
        "action_id": "ACT-303",
        "incident_id": "INC-1070",
        "priority": "MEDIUM",
        "assigned_team": "L2 DB Team",
        "description": "Confirm L3 DB patch status ticket DB-402 with Database Engineering.",
        "due_by": "2026-10-05T12:00:00Z"
    },
    {
        "action_id": "ACT-304",
        "incident_id": "INC-1065",
        "priority": "HIGH",
        "assigned_team": "Security Infra / L1.5",
        "description": "Verify automated deployment of renewed TLS wildcard cert for *.assets.domain.com.",
        "due_by": "2026-10-05T18:00:00Z"
    },
    {
        "action_id": "ACT-305",
        "incident_id": "INC-1052",
        "priority": "MEDIUM",
        "assigned_team": "Incoming Shift (L1.5)",
        "description": "Confirm merchant settlement output totals match general ledger balances for Oct 1st.",
        "due_by": "2026-10-05T14:00:00Z"
    }
]

SHIFT_HISTORY = [
    {
        "shift": "Night Shift (22:00 - 06:00 UTC)",
        "date": "2026-10-05",
        "operator": "Alex M. (L1.5 Lead)",
        "summary": "Handled P3 queue backlog (INC-1085) and stabilized Redis memory (INC-1088). Payment gateway spike (INC-1092) requires continuous monitoring.",
        "logged_at": "2026-10-05T06:00:00Z"
    },
    {
        "shift": "Afternoon Shift (14:00 - 22:00 UTC)",
        "date": "2026-10-04",
        "operator": "Sarah K. (L1.5 Lead)",
        "summary": "Logged SSL cert expiration warning (INC-1065). Responded to recurring DB batch pool locks (INC-1070).",
        "logged_at": "2026-10-04T22:00:00Z"
    },
    {
        "shift": "Morning Shift (06:00 - 14:00 UTC)",
        "date": "2026-10-04",
        "operator": "Carlos R. (L1.5 Lead)",
        "summary": "Routine shift. All system health metrics green. Pre-created ticket for SSL renewal.",
        "logged_at": "2026-10-04T14:00:00Z"
    },
    {
        "shift": "Night Shift (22:00 - 06:00 UTC)",
        "date": "2026-10-03",
        "operator": "Priya N. (L1.5 Lead)",
        "summary": "Resolved Elasticsearch indexing ingestion lag (INC-1062) by triggering shard rebalance.",
        "logged_at": "2026-10-03T06:00:00Z"
    },
    {
        "shift": "Afternoon Shift (14:00 - 22:00 UTC)",
        "date": "2026-10-02",
        "operator": "Alex M. (L1.5 Lead)",
        "summary": "Escalated Kafka consumer loop failure (INC-1058) to L2 Platform. Issue resolved in 2.5 hours.",
        "logged_at": "2026-10-02T22:00:00Z"
    },
    {
        "shift": "Morning Shift (06:00 - 14:00 UTC)",
        "date": "2026-10-01",
        "operator": "David T. (L1.5 Lead)",
        "summary": "Billing engine settlement delay (INC-1052) detected and lock released. System operating normally.",
        "logged_at": "2026-10-01T14:00:00Z"
    },
    {
        "shift": "Night Shift (22:00 - 06:00 UTC)",
        "date": "2026-09-29",
        "operator": "Sarah K. (L1.5 Lead)",
        "summary": "Mitigated inventory sync deadlock (INC-1048) by switching to batch CSV mode.",
        "logged_at": "2026-09-29T06:00:00Z"
    },
    {
        "shift": "Afternoon Shift (14:00 - 22:00 UTC)",
        "date": "2026-09-25",
        "operator": "Carlos R. (L1.5 Lead)",
        "summary": "Flash sale traffic peak handled successfully after applying API Gateway rate limiting (INC-1040).",
        "logged_at": "2026-09-25T22:00:00Z"
    },
    {
        "shift": "Morning Shift (06:00 - 14:00 UTC)",
        "date": "2026-09-22",
        "operator": "Priya N. (L1.5 Lead)",
        "summary": "Cart service memory leak hotfix deployed to production cleanly (INC-1035).",
        "logged_at": "2026-09-22T14:00:00Z"
    },
    {
        "shift": "Night Shift (22:00 - 06:00 UTC)",
        "date": "2026-09-18",
        "operator": "Alex M. (L1.5 Lead)",
        "summary": "Recommendation ML inference latency resolved by switching node pools (INC-1025).",
        "logged_at": "2026-09-18T06:00:00Z"
    },
    {
        "shift": "Morning Shift (06:00 - 14:00 UTC)",
        "date": "2026-09-15",
        "operator": "David T. (L1.5 Lead)",
        "summary": "Auth OAuth token validation bug fixed by NTP clock resync across Kubernetes nodes (INC-1020).",
        "logged_at": "2026-09-15T14:00:00Z"
    },
    {
        "shift": "Afternoon Shift (14:00 - 22:00 UTC)",
        "date": "2026-09-12",
        "operator": "Sarah K. (L1.5 Lead)",
        "summary": "Ingress controller OOM kill resolved by increasing RAM allocation (INC-1015).",
        "logged_at": "2026-09-12T22:00:00Z"
    },
    {
        "shift": "Night Shift (22:00 - 06:00 UTC)",
        "date": "2026-09-10",
        "operator": "Carlos R. (L1.5 Lead)",
        "summary": "Order Processing DB cleanup job rescheduled to prevent foreign key locks (INC-1010).",
        "logged_at": "2026-09-10T06:00:00Z"
    },
    {
        "shift": "Morning Shift (06:00 - 14:00 UTC)",
        "date": "2026-09-08",
        "operator": "Priya N. (L1.5 Lead)",
        "summary": "SendGrid notification tier upgraded following 429 quota exhaustion (INC-1005).",
        "logged_at": "2026-09-08T14:00:00Z"
    },
    {
        "shift": "Morning Shift (06:00 - 14:00 UTC)",
        "date": "2026-09-05",
        "operator": "Alex M. (L1.5 Lead)",
        "summary": "Sandbox environment stub restarted (INC-1001). Monthly maintenance check completed.",
        "logged_at": "2026-09-05T14:00:00Z"
    }
]
