# ruff: noqa
# Copyright 2026 Google LLC
# Licensed under the Apache License, Version 2.0

"""L1.5 IT Application Operations Shift Handover Agent with A2UI, Firestore backend, live health probes, notifications, DevOps platform API integrations, image generation, Agent Engine code execution, and Memory Bank integration."""

import asyncio
import datetime
import json
import time
import urllib.request
import urllib.error
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from a2ui.schema.manager import A2uiSchemaManager
from a2ui.basic_catalog.provider import BasicCatalog

from google import genai
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.code_executors import AgentEngineSandboxCodeExecutor
from google.adk.memory import VertexAiMemoryBankService
from google.adk.memory.memory_entry import MemoryEntry
from google.adk.models import Gemini
from google.adk.tools import ToolContext, load_memory, preload_memory
from google.genai import types
from google.cloud import firestore, storage
from google.api_core.exceptions import NotFound

from .a2ui_utils import a2ui_callback
from .mock_ops_data import INCIDENTS, PENDING_ACTIONS, RUNBOOKS, SHIFT_HISTORY

# IMPORTANT: Hardcoded GCP Project ID and Cloud Storage Bucket Name
FIRESTORE_PROJECT_ID = "qwiklabs-gcp-02-5f5b32433c64"
BUCKET_NAME = "qwiklabs-gcp-02-5f5b32433c64-static-assets-bucket"

# Load remote Agent Engine runtime ID from deployment_metadata.json for Code Execution Sandbox and Memory Bank
DEPLOYMENT_METADATA_PATH = Path(__file__).parent.parent / "deployment_metadata.json"
REMOTE_RUNTIME_ID = "projects/333685870271/locations/us-central1/reasoningEngines/972636232267857920"

if DEPLOYMENT_METADATA_PATH.exists():
    try:
        with open(DEPLOYMENT_METADATA_PATH, "r") as f:
            metadata = json.load(f)
            REMOTE_RUNTIME_ID = metadata.get("remote_agent_runtime_id", REMOTE_RUNTIME_ID)
    except Exception:
        pass

# Extract Agent Engine ID (last segment of resource path)
AGENT_ENGINE_ID = REMOTE_RUNTIME_ID.split("/")[-1]

# Configure Code Executor using Agent Engine Sandbox
sandbox_code_executor = AgentEngineSandboxCodeExecutor(
    agent_engine_resource_name=REMOTE_RUNTIME_ID
)

# Configure Memory Bank Service for persistent memory operations
memory_service = VertexAiMemoryBankService(
    project=FIRESTORE_PROJECT_ID,
    location="us-central1",
    agent_engine_id=AGENT_ENGINE_ID,
)


def _get_firestore_client() -> firestore.Client:
    """Instantiates a Firestore client with the explicitly hardcoded GCP project ID."""
    return firestore.Client(project=FIRESTORE_PROJECT_ID)


def save_handover_note_to_memory(
    note: str,
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Saves an operational handover note or shift update into the Vertex AI Memory Bank so all users and shifts remember it.

    Args:
        note: The handover note, operational summary, or operator update to remember.
        tool_context: Injected ADK ToolContext used for memory operations.

    Returns:
        Confirmation payload indicating memory storage status.
    """
    try:
        content = types.Content(
            parts=[types.Part.from_text(text=f"Shift Handover Memory Note: {note}")],
            role="user"
        )
        entry = MemoryEntry(content=content)
        asyncio.run(memory_service.add_memory(app_name="app", user_id="user", memories=[entry]))
        storage_status = "Vertex AI Memory Bank"
    except Exception as e:
        storage_status = f"Local Memory Service ({e})"

    if tool_context is not None:
        try:
            tool_context.add_memory(note)
        except Exception:
            pass

    return {
        "status": "SUCCESS",
        "storage": storage_status,
        "message": "Handover note successfully remembered in Memory Bank.",
        "note": note
    }


async def generate_shift_dashboard_image(
    prompt: str = "A sleek, modern IT operations shift handover summary dashboard showing system status, P1 incident metrics, and SLA timelines",
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Generates an IT operations shift handover summary or dashboard image using gemini-3.1-flash-lite-image in the global region.

    Saves the generated image to Playground artifacts via tool_context and uploads the image bytes directly to a public Cloud Storage bucket.

    Args:
        prompt: Visual description of the IT operations shift summary dashboard or system topology diagram.
        tool_context: Injected ADK ToolContext used for saving playground artifacts.

    Returns:
        Dictionary containing the public Cloud Storage https URL (https://storage.googleapis.com/<bucket>/<object>), filename, and status.
    """
    genai_client = genai.Client(
        vertexai=True,
        project=FIRESTORE_PROJECT_ID,
        location="global"
    )
    response = genai_client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=prompt
    )

    part = response.candidates[0].content.parts[0]
    image_bytes = part.inline_data.data
    mime_type = part.inline_data.mime_type or "image/jpeg"
    ext = "png" if "png" in mime_type else "jpg"

    filename = f"shift_handover_dashboard_{uuid.uuid4().hex[:8]}.{ext}"

    # 1. Save artifact to Playground if tool_context is provided
    if tool_context is not None:
        try:
            await tool_context.save_artifact(
                filename=filename,
                artifact=types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            )
        except Exception:
            pass

    # 2. Upload image bytes directly to public Cloud Storage bucket
    storage_client = storage.Client(project=FIRESTORE_PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"

    return {
        "status": "SUCCESS",
        "public_url": public_url,
        "artifact_filename": filename,
        "bucket": BUCKET_NAME
    }


def get_devops_platform_status(platform: str = "github") -> Dict[str, Any]:
    """Queries a free public API (GitHub Status API) to fetch real-time operational health, component status, and active platform incidents.

    Args:
        platform: Name of the external platform to query (defaults to 'github').

    Returns:
        Dictionary containing overall platform status, component health, and active incident count.
    """
    url = "https://www.githubstatus.com/api/v2/summary.json"
    req = urllib.request.Request(url, headers={"User-Agent": "L1.5-ShiftHandoverAgent/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode("utf-8"))
            components_status = [
                {"name": comp["name"], "status": comp["status"]}
                for comp in data.get("components", [])
                if comp.get("name") and not comp["name"].startswith("Visit")
            ]
            return {
                "platform": "GitHub Platform",
                "overall_status": data.get("status", {}).get("description", "Unknown"),
                "indicator": data.get("status", {}).get("indicator", "none"),
                "active_incidents_count": len(data.get("incidents", [])),
                "active_incidents": data.get("incidents", []),
                "components": components_status[:8],
                "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "platform": "GitHub Platform",
            "overall_status": "UNREACHABLE",
            "error": str(e),
            "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


def check_service_health(url: str = "https://httpbin.org/status/200") -> Dict[str, Any]:
    """Performs a real-time HTTP GET probe to measure service availability, HTTP status code, and latency in milliseconds.

    Args:
        url: Full URL of the endpoint to check (e.g. 'https://httpbin.org/status/200', 'https://api.github.com').

    Returns:
        Dictionary containing real-time status code, response latency in ms, health classification, and timestamp.
    """
    start_time = time.time()
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "L1.5-ShiftHandoverAgent/1.0"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            latency_ms = round((time.time() - start_time) * 1000, 2)
            status_code = response.getcode()
            is_healthy = 200 <= status_code < 300
            return {
                "url": url,
                "status_code": status_code,
                "latency_ms": latency_ms,
                "is_healthy": is_healthy,
                "status": "OPERATIONAL" if is_healthy else "DEGRADED",
                "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
    except urllib.error.HTTPError as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "url": url,
            "status_code": e.code,
            "latency_ms": latency_ms,
            "is_healthy": False,
            "status": f"HTTP_ERROR_{e.code}",
            "error": str(e),
            "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    except Exception as e:
        latency_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "url": url,
            "status_code": 0,
            "latency_ms": latency_ms,
            "is_healthy": False,
            "status": "UNREACHABLE",
            "error": str(e),
            "checked_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


def send_handover_notification(webhook_url: str = "https://httpbin.org/post", message: str = "") -> Dict[str, Any]:
    """Posts a shift handover alert or report notification to an external chat webhook or operational channel.

    Args:
        webhook_url: Target webhook endpoint URL (defaults to 'https://httpbin.org/post').
        message: The shift handover summary message or critical P1 alert text to dispatch.

    Returns:
        Dictionary confirming notification delivery status, response status code, and timestamp.
    """
    payload = json.dumps({"text": message, "source": "L1.5 Shift Handover Agent"}).encode("utf-8")
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "L1.5-ShiftHandoverAgent/1.0"}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return {
                "status": "DELIVERED",
                "status_code": response.getcode(),
                "delivered_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
    except Exception as e:
        return {
            "status": "FAILED",
            "error": str(e),
            "delivered_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }


def get_incidents_from_firestore(status: str = "all", severity: str = "all") -> List[Dict[str, Any]]:
    """Reads incident documents from the Firestore 'incidents' collection.

    Args:
        status: Filter by status ('Active', 'Resolved', 'Recurring', or 'all').
        severity: Filter by severity ('P1', 'P2', 'P3', 'P4', or 'all').

    Returns:
        List of incident document dictionaries stored in Firestore.
    """
    try:
        db = _get_firestore_client()
        docs = db.collection("incidents").stream()
        results = [doc.to_dict() for doc in docs]
        if not results:
            results = INCIDENTS
    except Exception:
        results = INCIDENTS

    if status.lower() != "all":
        results = [i for i in results if i.get("status", "").lower() == status.lower()]
    if severity.lower() != "all":
        results = [i for i in results if i.get("severity", "").lower() == severity.lower()]
    return results


def add_incident_to_firestore(
    incident_id: str,
    title: str,
    severity: str,
    service: str,
    summary: str,
    pending_action: str
) -> Dict[str, Any]:
    """Writes a new incident document to the Firestore 'incidents' collection.

    Args:
        incident_id: Unique incident key (e.g. 'INC-1095').
        title: Short title description.
        severity: Priority level ('P1', 'P2', 'P3', 'P4').
        service: Affected microservice or component.
        summary: Technical summary of the issue.
        pending_action: Action required by the next shift team.

    Returns:
        Confirmation payload of the stored incident.
    """
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    sla_hours = 4 if severity.upper() in ["P1", "P2"] else 8
    sla_dt = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=sla_hours)

    doc_data = {
        "incident_id": incident_id,
        "title": title,
        "severity": severity.upper(),
        "status": "Active",
        "service": service,
        "assigned_to": "L1.5 Operations Lead",
        "opened_at": now_iso,
        "sla_deadline": sla_dt.isoformat(),
        "summary": summary,
        "actions_taken": "Logged via Shift Handover Agent.",
        "pending_action": pending_action,
        "updated_at": now_iso
    }

    try:
        db = _get_firestore_client()
        db.collection("incidents").document(incident_id).set(doc_data)
        storage_type = "Firestore DB"
    except Exception:
        INCIDENTS.append(doc_data)
        storage_type = "In-Memory Store"

    return {
        "status": "SUCCESS",
        "storage": storage_type,
        "message": f"Incident {incident_id} successfully recorded in {storage_type}.",
        "incident": doc_data
    }


def update_incident_status_in_firestore(
    incident_id: str,
    status: str,
    actions_taken: str,
    pending_action: str
) -> Dict[str, Any]:
    """Updates an existing incident document's status, actions taken, and pending actions in Firestore.

    Args:
        incident_id: The ID of the incident to update (e.g. 'INC-1092').
        status: Updated status ('Active', 'Resolved', 'Recurring').
        actions_taken: Mitigation work completed during this shift.
        pending_action: Updated action items for the incoming shift.

    Returns:
        Confirmation dictionary with the updated document fields.
    """
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    update_data = {
        "status": status,
        "actions_taken": actions_taken,
        "pending_action": pending_action,
        "updated_at": now_iso
    }

    try:
        db = _get_firestore_client()
        doc_ref = db.collection("incidents").document(incident_id)
        doc_ref.update(update_data)
        storage_type = "Firestore DB"
    except Exception:
        for inc in INCIDENTS:
            if inc["incident_id"].lower() == incident_id.lower():
                inc.update(update_data)
                break
        storage_type = "In-Memory Store"

    return {
        "status": "SUCCESS",
        "storage": storage_type,
        "message": f"Incident {incident_id} updated in {storage_type}.",
        "updated_fields": update_data
    }


def get_runbook(query: str) -> Dict[str, Any]:
    """Retrieves standard operating procedures (SOP) or runbook for a specific service or issue keyword.

    Args:
        query: Keyword or service name (e.g. 'payment', 'redis', 'database', 'auth').

    Returns:
        Runbook procedure details including title, ID, and step-by-step mitigation instructions.
    """
    q = query.lower()
    for key, runbook in RUNBOOKS.items():
        if key in q or runbook["title"].lower().find(q) != -1 or runbook["id"].lower().find(q) != -1:
            return runbook
    return {
        "message": f"No specific runbook found for '{query}'. Please check the global operations portal.",
        "available_runbooks": [r["id"] + ": " + r["title"] for r in RUNBOOKS.values()]
    }


def get_pending_actions() -> List[Dict[str, Any]]:
    """Retrieves all active pending actions and handoff tasks that need attention during or after shift change.

    Returns:
        List of pending action records with action_id, incident_id, priority, assigned_team, description, and due_by.
    """
    return PENDING_ACTIONS


def calculate_sla_risk(incident_id: str) -> Dict[str, Any]:
    """Calculates the time remaining until SLA breach and computes breach risk for a given incident.

    Args:
        incident_id: The ID of the incident (e.g. 'INC-1092').

    Returns:
        SLA risk assessment with minutes remaining, risk level, and recommended escalation.
    """
    incidents = get_incidents_from_firestore()
    target = None
    for inc in incidents:
        if inc.get("incident_id", inc.get("id", "")).lower() == incident_id.lower():
            target = inc
            break

    if not target:
        return {"error": f"Incident {incident_id} not found."}

    now = datetime.datetime.now(datetime.timezone.utc)
    sla_dt = datetime.datetime.fromisoformat(target["sla_deadline"])
    delta = sla_dt - now
    minutes_left = int(delta.total_seconds() / 60)

    if minutes_left <= 60:
        risk_level = "CRITICAL (High SLA Breach Risk)"
    elif minutes_left <= 180:
        risk_level = "ELEVATED"
    else:
        risk_level = "LOW"

    return {
        "incident_id": target.get("incident_id", target.get("id")),
        "severity": target["severity"],
        "title": target["title"],
        "sla_deadline": target["sla_deadline"],
        "minutes_remaining": minutes_left,
        "sla_risk_level": risk_level,
        "recommended_action": f"Prioritize immediate mitigation for {target.get('incident_id')} ({target['service']})."
    }


def search_shift_history(query: str = "") -> List[Dict[str, Any]]:
    """Retrieves context from previous shifts over the last 30 days to answer questions like 'What happened while I was away?' or 'Show shift logs for September 25'.

    Args:
        query: Optional search keyword or date string to filter past shift logs.

    Returns:
        List of past shift summary logs.
    """
    if not query:
        return SHIFT_HISTORY
    
    q = query.lower().strip()
    month_map = {
        "january": "01", "jan": "01",
        "february": "02", "feb": "02",
        "march": "03", "mar": "03",
        "april": "04", "apr": "04",
        "may": "05",
        "june": "06", "jun": "06",
        "july": "07", "jul": "07",
        "august": "08", "aug": "08",
        "september": "09", "sep": "09", "sept": "09",
        "october": "10", "oct": "10",
        "november": "11", "nov": "11",
        "december": "12", "dec": "12"
    }
    
    normalized_q = q
    for m_name, m_num in month_map.items():
        if m_name in q:
            import re
            day_match = re.search(r'\b(\d{1,2})\b', q)
            if day_match:
                day_num = int(day_match.group(1))
                normalized_q = f"2026-{m_num}-{day_num:02d}"
            break

    matched = []
    for s in SHIFT_HISTORY:
        s_str = json.dumps(s).lower()
        if q in s_str or normalized_q in s_str:
            matched.append(s)

    return matched if matched else SHIFT_HISTORY[:5]


def create_handover_report(
    shift_name: str,
    summary: str,
    critical_issues: List[str],
    pending_actions: List[str],
    tool_context: Optional[ToolContext] = None
) -> Dict[str, Any]:
    """Generates and logs a new L1.5 shift handover record for the incoming shift team and stores it in the Memory Bank.

    Args:
        shift_name: Name of the outgoing shift (e.g. 'Day Shift 06:00 - 14:00 UTC').
        summary: Executive summary of shift operations.
        critical_issues: List of active P1/P2 incident IDs or titles.
        pending_actions: List of pending tasks assigned to the next shift.
        tool_context: Injected ADK ToolContext used for memory operations.

    Returns:
        Confirmation payload with the recorded handover summary.
    """
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
    new_entry = {
        "shift": shift_name,
        "operator": "L1.5 Operations Lead",
        "summary": summary,
        "critical_issues": critical_issues,
        "pending_actions": pending_actions,
        "logged_at": now_iso
    }
    SHIFT_HISTORY.append(new_entry)

    # Save handover note to Memory Bank
    note_text = f"Handover Report for {shift_name}: Summary: {summary}. Critical Issues: {', '.join(critical_issues)}. Pending Actions: {', '.join(pending_actions)}."
    try:
        content = types.Content(
            parts=[types.Part.from_text(text=note_text)],
            role="user"
        )
        entry = MemoryEntry(content=content)
        asyncio.run(memory_service.add_memory(app_name="app", user_id="user", memories=[entry]))
    except Exception:
        pass

    if tool_context is not None:
        try:
            tool_context.add_memory(note_text)
        except Exception:
            pass

    return {
        "status": "SUCCESS",
        "message": "Shift handover report created and saved to Memory Bank successfully.",
        "handover": new_entry
    }


# Build A2UI v0.8 System Prompt
a2ui_schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

SYSTEM_INSTRUCTION = a2ui_schema_manager.generate_system_prompt(
    role_description=(
        "You are an expert L1.5 IT Application Operations Shift Handover Agent for a 24/7 IT Operations Center. "
        "Your role is to assist support teams maintain 100% operational continuity between shifts. "
        "CRITICAL FORMATTING RULES FOR ALL OUTPUTS: "
        "1. Always use expressive emojis (such as 🚀, 📊, 🚨, 📜, 📅, ✅, 💡, ⚡) in all text outputs and card texts. "
        "2. NEVER use asterisks (*) anywhere in your text outputs (do NOT use * for bold, italics, markdown, or bullet points)."
    ),
    workflow_description=(
        "Analyze the L1.5 shift handover request, active incidents from Firestore, SLA risk calculations, "
        "and Memory Bank history. Perform necessary tool calls (such as health probes, image generation, "
        "or incident retrieval), then return structured UI cards and visual shift summaries when appropriate. "
        "Ensure all text responses use emojis and contain ZERO asterisks (*)."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Image. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "You may include one Image component, but only when you have a public https "
        "URL for the image (for example the public_url returned by generate_shift_dashboard_image). "
        "Set the Image url to that exact https link, for example "
        "{\"Image\": {\"url\": {\"literalString\": \"https://storage.googleapis.com/...\"}}}. "
        "Never point an Image at a bare filename, an artifact name, or a non-http(s) path. If you do "
        "not have a public URL, add a short Text line noting the image instead. "
        "No markdown or asterisks (*) in text; use expressive emojis and use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    after_model_callback=a2ui_callback,
    code_executor=sandbox_code_executor,
    tools=[
        save_handover_note_to_memory,
        generate_shift_dashboard_image,
        get_devops_platform_status,
        check_service_health,
        send_handover_notification,
        get_incidents_from_firestore,
        add_incident_to_firestore,
        update_incident_status_in_firestore,
        get_runbook,
        get_pending_actions,
        calculate_sla_risk,
        search_shift_history,
        create_handover_report,
        load_memory,
        preload_memory,
    ],
)

app = App(
    root_agent=root_agent,
    name="app",
)
