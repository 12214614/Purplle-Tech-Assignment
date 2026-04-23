# ⚙️ CHOICES.md – Engineering Decisions

## 📌 Overview

This document explains key design and technology decisions made while building the system.

---

## 🤖 1. Why YOLOv8?

* Lightweight and fast for real-time inference
* Works well on CPU without GPU dependency
* Easy integration using Ultralytics API

Trade-off:

* Slightly lower accuracy compared to heavier models (e.g., YOLOv8x)

---

## 🔍 2. Why Tracking Instead of Frame-wise Detection?

* Required to maintain visitor identity across frames
* Enables:

  * Entry/Exit detection
  * Dwell time calculation
  * Funnel tracking

Trade-off:

* ID switching can occur during occlusion

---

## 🗺️ 3. Why Manual Zone Definition?

* Store layout is known and static
* Simpler and more reliable than ML-based segmentation
* Allows easy debugging and visualization

Trade-off:

* Not adaptable to dynamic layouts

---

## 📦 4. Why JSONL Event Format?

* Each event is independent (stream-friendly)
* Easy to append and process
* Compatible with real-time pipelines (Kafka-like systems)

---

## ⚡ 5. Why FastAPI?

* Lightweight and fast
* Built-in Swagger UI for easy testing
* Minimal setup required

---

## 📊 6. Why Rule-Based Analytics?

* Simpler and explainable
* Matches assignment requirement for reasoning
* No need for training data

Trade-off:

* Less adaptive than ML-based analytics

---

## 🔁 7. Re-entry Handling Approach

* Based on time threshold logic
* If same ID appears within short time → REENTRY

Trade-off:

* Not fully accurate without face recognition

---

## 👥 8. Staff vs Customer Handling

* Currently heuristic-based (zone/time presence)
* Marked using `is_staff` flag (extendable)

Trade-off:

* May misclassify in edge cases

---

## 🛒 9. Purchase Detection Logic

* Approximated using dwell time in billing zone
* Assumes longer dwell → higher purchase likelihood

Trade-off:

* No direct POS integration

---

## 📉 10. Anomaly Detection Strategy

* Threshold-based:

  * Queue spike (>5 people)
  * Low conversion (<20%)
  * Dead zones (low activity)

Trade-off:

* Static thresholds may not generalize

---

## 🧠 Key Philosophy

> “Build a simple system that works end-to-end, then improve accuracy.”

This approach ensures:

* Completeness over perfection
* Clear reasoning over complexity
