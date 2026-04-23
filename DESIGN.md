# 🏗️ DESIGN.md – System Architecture

## 📌 Overview

This system converts CCTV footage into structured retail analytics using a modular pipeline. The architecture is designed to be simple, extensible, and event-driven.

---

## 🔄 End-to-End Flow

```text
Video Input → Detection → Tracking → Event Generation → API → Analytics
```

---

## 🧩 Components

### 1. Video Processing (pipeline/detect.py)

* Input: CCTV video footage
* Performs:

  * Person detection using YOLOv8
  * Multi-object tracking (assigns unique IDs)
* Output:

  * Bounding boxes + visitor IDs

---

### 2. Zone Mapping (pipeline/zones.py)

* Defines store layout as rectangular regions
* Maps each person to a zone using centroid logic
* Enables:

  * Zone-based analytics
  * Movement tracking

---

### 3. Event Generation (pipeline/emit.py)

* Converts raw tracking into structured events
* Events include:

  * ENTRY, EXIT
  * ZONE_ENTER
  * ZONE_DWELL
* Stored in `.jsonl` format for streaming compatibility

---

### 4. API Layer (app/main.py)

* Built using FastAPI
* Responsibilities:

  * Ingest events
  * Store events in memory
  * Compute metrics and analytics

---

### 5. Analytics Engine

Derived from ingested events:

#### Metrics

* Total visitors
* Conversion rate
* Average dwell time

#### Funnel

* Entry → Zone → Billing → Purchase

#### Anomalies

* Queue spike detection
* Low conversion detection
* Dead zone detection

---

## 🧠 Design Principles

### 1. Event-Driven Architecture

Instead of tightly coupling components, the system emits events that can be processed independently.

---

### 2. Separation of Concerns

* Detection logic → pipeline/
* API logic → app/
* Event logic → emit.py

---

### 3. Simplicity First

* Used rule-based logic instead of complex ML
* Focused on working system over theoretical accuracy

---

### 4. Extensibility

* Event schema allows easy integration with databases
* API can be scaled to multiple stores

---

## ⚙️ Data Flow

```text
Frame → Detection → Tracking → Zone Mapping → Event → API → Metrics
```

---

## 📦 Storage Choice

* Used in-memory storage for simplicity
* Can be replaced with:

  * PostgreSQL
  * Kafka (for streaming)

---

## ⚠️ Trade-offs

* No full Re-ID across cameras
* Approximate purchase detection (billing dwell)
* Static zone definitions

---

## 🔮 Future Enhancements

* Multi-camera identity matching
* Real-time dashboard
* Cloud deployment with Docker + Kubernetes
