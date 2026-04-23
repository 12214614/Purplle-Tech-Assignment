from fastapi import FastAPI
from typing import List, Dict

app = FastAPI(title="Store Intelligence API")

# -----------------------------
# In-memory storage
# -----------------------------
events: List[Dict] = []


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {"message": "Store Intelligence API is running"}


# -----------------------------
# INGEST EVENTS
# -----------------------------
@app.post("/events/ingest")
def ingest_events(data: List[Dict]):
    events.extend(data)
    return {"status": "success", "events_received": len(data)}


# -----------------------------
# METRICS
# -----------------------------
@app.get("/stores/{store_id}/metrics")
def get_metrics(store_id: str):
    entry = set()
    purchase = set()
    zone_dwell = {}

    for event in events:
        vid = event["visitor_id"]
        etype = event["event_type"]
        zone = event.get("zone_id")
        dwell = event.get("dwell_ms", 0)

        if etype == "ENTRY":
            entry.add(vid)

        if etype == "ZONE_DWELL" and zone:
            zone_dwell.setdefault(zone, []).append(dwell)

        if zone == "BILLING":
            if dwell > 3000:
                purchase.add(vid)

    conversion_rate = len(purchase) / len(entry) if len(entry) > 0 else 0

    avg_dwell = {
        z: round(sum(v) / len(v), 2)
        for z, v in zone_dwell.items()
        if len(v) > 0
    }

    return {
        "store_id": store_id,
        "total_visitors": len(entry),
        "conversion_rate": round(conversion_rate, 2),
        "avg_dwell_per_zone": avg_dwell,
    }


# -----------------------------
# FUNNEL
# -----------------------------
@app.get("/stores/{store_id}/funnel")
def get_funnel(store_id: str):
    entry = set()
    zone_visit = set()
    billing = set()
    purchase = set()

    for event in events:
        vid = event["visitor_id"]
        etype = event["event_type"]
        zone = event.get("zone_id")
        dwell = event.get("dwell_ms", 0)

        if etype == "ENTRY":
            entry.add(vid)

        if etype in ["ZONE_ENTER", "ZONE_DWELL"]:
            zone_visit.add(vid)

        if zone == "BILLING":
            billing.add(vid)

            if dwell > 3000:
                purchase.add(vid)

    return {
        "entry": len(entry),
        "zone_visit": len(zone_visit),
        "billing": len(billing),
        "purchase": len(purchase),
        "drop_off": {
            "zone": len(entry - zone_visit),
            "billing": len(zone_visit - billing),
            "purchase": len(billing - purchase),
        },
    }


# -----------------------------
# ANOMALIES
# -----------------------------
@app.get("/stores/{store_id}/anomalies")
def get_anomalies(store_id: str):
    anomalies = []

    billing_count = sum(
        1 for e in events if e.get("zone_id") == "BILLING"
    )

    if billing_count > 50:
        anomalies.append({
            "type": "QUEUE_SPIKE",
            "message": "High number of customers in billing area"
        })

    # detect dead zones
    zone_activity = {}
    for e in events:
        zone = e.get("zone_id")
        if zone:
            zone_activity[zone] = zone_activity.get(zone, 0) + 1

    for zone, count in zone_activity.items():
        if count < 5:
            anomalies.append({
                "type": "DEAD_ZONE",
                "message": f"Low activity in {zone}"
            })

    return anomalies