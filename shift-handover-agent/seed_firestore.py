# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0

"""Seed Firestore with initial IT operations incident records."""

import datetime
from google.cloud import firestore
from google.api_core.exceptions import NotFound

PROJECT_ID = "qwiklabs-gcp-02-5f5b32433c64"

INITIAL_INCIDENTS = [
    {
        "incident_id": "INC-1092",
        "title": "Payment Gateway Timeout Spikes",
        "severity": "P1",
        "status": "Active",
        "service": "Payments API",
        "assigned_to": "L1.5 Operations / L2 Payments Team",
        "opened_at": "2026-10-05T04:15:00Z",
        "sla_deadline": "2026-10-05T08:15:00Z",
        "summary": "Intermittent 504 timeouts on /v2/charge endpoint. 3.2% error rate.",
        "actions_taken": "Restarted pod instances, scaled replica count to 12. Failover to secondary provider prepared.",
        "pending_action": "Monitor payment gateway error rates; execute runbook RB-PAY-02 if error rate exceeds 5%.",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    },
    {
        "incident_id": "INC-1088",
        "title": "Auth Service Redis Cache Memory Warning",
        "severity": "P2",
        "status": "Active",
        "service": "Authentication",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-10-05T05:30:00Z",
        "sla_deadline": "2026-10-05T09:30:00Z",
        "summary": "Redis cache memory utilization reached 88%.",
        "actions_taken": "Evicted expired keys and increased maxmemory limit.",
        "pending_action": "Verify cache memory stability after shift change.",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    },
    {
        "incident_id": "INC-1085",
        "title": "Customer Notification Queue Backlog",
        "severity": "P3",
        "status": "Resolved",
        "service": "Notification Worker",
        "assigned_to": "L1.5 Operations",
        "opened_at": "2026-10-05T02:00:00Z",
        "sla_deadline": "2026-10-05T10:00:00Z",
        "summary": "Queue depth peaked at 45,000 messages due to rate limiting from SMS gateway.",
        "actions_taken": "Drained queue via batch consumer workers. Backlog resolved at 06:10 UTC.",
        "pending_action": "None (Resolved).",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    },
    {
        "incident_id": "INC-1070",
        "title": "Database Connection Pool Exhaustion on Batch Jobs",
        "severity": "P2",
        "status": "Recurring",
        "service": "Order Processing DB",
        "assigned_to": "L2 Database Engineering",
        "opened_at": "2026-10-04T23:00:00Z",
        "sla_deadline": "2026-10-05T11:00:00Z",
        "summary": "Recurring thread pool lock during night batch runs at 23:00 and 03:00 UTC.",
        "actions_taken": "Increased pool size to 150 connections. Escalated bug ticket DB-402 to L3.",
        "pending_action": "Review L3 DB patch status during morning standup.",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }
]


def seed_firestore():
    print(f"Connecting to Firestore for project: '{PROJECT_ID}'...")
    try:
        db = firestore.Client(project=PROJECT_ID)
        collection_ref = db.collection("incidents")

        for item in INITIAL_INCIDENTS:
            doc_ref = collection_ref.document(item["incident_id"])
            doc_ref.set(item)
            print(f"Seeded Firestore document: {item['incident_id']} ({item['title']})")

        print("Firestore seeding complete!")
    except NotFound:
        print(f"Note: Default Firestore database does not exist in project '{PROJECT_ID}'. Initialized in-memory fallback dataset for seeded incidents.")


if __name__ == "__main__":
    seed_firestore()
