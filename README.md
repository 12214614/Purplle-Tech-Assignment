# 🏬 Retail Intelligence System (CCTV Analytics)

---

## 📌 Overview

This project converts raw CCTV footage into meaningful retail insights such as:

* 👥 Total visitors
* ⏱️ Time spent in different zones
* 🛒 Conversion rate (visitors → buyers)
* ⚠️ Anomaly detection (low activity, billing congestion)

The system processes multiple camera feeds and produces structured analytics using an end-to-end pipeline.

---

## 🧠 How the System Works

```text
CCTV Videos → Detection → Event Generation → API → Analytics → Dashboard
```

### Step-by-step flow:

1. CCTV videos are processed using YOLOv8
2. People are detected and tracked
3. Events are generated:

   * ENTRY
   * EXIT
   * ZONE_ENTER
   * ZONE_DWELL
4. Events are sent to FastAPI backend
5. API calculates:

   * Metrics
   * Funnel
   * Anomalies
6. Dashboard displays final results

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd Purplle Tech
```

---

### 2. Create virtual environment

```bash
python -m venv .venv
```

Activate:

**Windows:**

```bash
.venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run (One Command Execution)

```bash
python run_all.py
```

---

## ⏳ What Happens After Running

When you run the above command, the system performs the following steps automatically:

---

### 🚀 Step 1: API Initialization

* FastAPI server starts
* Prepares endpoints for data ingestion and analytics

---

### 🎥 Step 2: Video Processing (Camera-wise)

Each CCTV video is processed one by one:

```text
Processing CAM_ENTRY_DOOR...
Processing CAM_FLOOR_MAIN...
Processing CAM_FLOOR_SECONDARY...
Processing CAM_BILLING_COUNTER...
```

During this step:

* People are detected
* Movements are tracked
* Events are generated

⏱️ This step may take **30–90 seconds depending on system performance**

---

### 📡 Step 3: Event Streaming

* Generated events are automatically sent to API
* No manual input required

---

### 📊 Step 4: Analytics Computation

The system calculates:

* Total visitors
* Conversion rate
* Funnel stages
* Anomalies

---

### 📺 Step 5: Final Dashboard Output

After processing completes, a clean summary is displayed:

```text
📊 Store Metrics
Total Visitors: 5
Conversion Rate: 0.6

🔄 Funnel
Entry: 5
Billing: 3
Purchase: 2

⚠️ Anomalies:
- DEAD_ZONE: Low activity in FLOOR
```

---

## 🧪 Manual Execution (Alternative)

If needed, each component can be run individually:

### Start API

```bash
python -m uvicorn app.main:app
```

---

### Run detection

```bash
python pipeline/detect.py
```

---

### Run dashboard

```bash
python app/dashboard.py
```

---

## 📂 Project Structure

```text
Purplle Tech/
├── app/
│   ├── main.py
│   ├── dashboard.py
│
├── pipeline/
│   ├── detect.py
│   ├── emit.py
│   ├── zones.py
│
├── data/
├── run_all.py
├── requirements.txt
├── DESIGN.md
├── CHOICES.md
```

---

## ⚡ Performance Optimizations

* Frame skipping to reduce computation
* Resolution scaling for faster processing
* Lightweight YOLOv8 model used

---

## ⚠️ Limitations

* Data stored in memory (resets on restart)
* Cross-camera identity tracking is approximate
* Purchase inferred from billing zone activity

---

## 🚀 Future Improvements

* Persistent database (PostgreSQL)
* Advanced re-identification across cameras
* Web-based dashboard
* GPU acceleration

---

## 💡 Summary

This project demonstrates how raw CCTV footage can be transformed into actionable business insights through a complete, automated pipeline with minimal manual intervention.

---
