import requests
import uuid
from datetime import datetime

API_URL = "http://127.0.0.1:8000/events/ingest"


# -----------------------------
# Generate timestamp
# -----------------------------
def get_timestamp():
    return datetime.utcnow().isoformat() + "Z"


# -----------------------------
# Create event (FULL SCHEMA)
# -----------------------------
def create_event(store_id, camera_id, visitor_id, event_type,
                 zone_id=None, dwell_ms=0, is_staff=False,
                 confidence=0.9, metadata=None):

    event = {
        "event_id": str(uuid.uuid4()),
        "store_id": store_id,
        "camera_id": camera_id,
        "visitor_id": f"VIS_{visitor_id}",
        "event_type": event_type,
        "timestamp": get_timestamp(),
        "zone_id": zone_id,
        "dwell_ms": dwell_ms,
        "is_staff": is_staff,
        "confidence": round(confidence, 2),
        "metadata": metadata or {}
    }

    return event


# -----------------------------
# Send event to API
# -----------------------------
def emit_event(event):
    try:
        requests.post(API_URL, json=[event])
    except Exception as e:
        print("Failed to send event:", e)


# -----------------------------
# Entry Event
# -----------------------------
def emit_entry(store_id, camera_id, visitor_id, confidence):
    event = create_event(
        store_id=store_id,
        camera_id=camera_id,
        visitor_id=visitor_id,
        event_type="ENTRY",
        confidence=confidence,
        metadata={"session_seq": 1}
    )

    emit_event(event)
    print("ENTRY EVENT:", event)


# -----------------------------
# Exit Event
# -----------------------------
def emit_exit(store_id, camera_id, visitor_id, confidence):
    event = create_event(
        store_id=store_id,
        camera_id=camera_id,
        visitor_id=visitor_id,
        event_type="EXIT",
        confidence=confidence
    )

    emit_event(event)
    print("EXIT EVENT:", event)


# -----------------------------
# Re-entry Event
# -----------------------------
def emit_reentry(store_id, camera_id, visitor_id, confidence):
    event = create_event(
        store_id=store_id,
        camera_id=camera_id,
        visitor_id=visitor_id,
        event_type="REENTRY",
        confidence=confidence
    )

    emit_event(event)
    print("REENTRY EVENT:", event)