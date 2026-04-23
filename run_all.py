import subprocess
import time
import socket
import requests
import sys
from rich.console import Console
from rich.table import Table

console = Console()

# -----------------------------
# STEP 1: START API
# -----------------------------
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

if is_port_in_use(8000):
    console.print("[yellow]⚠️ API already running, skipping start[/yellow]")
    api_process = None
else:
    console.print("[green]🚀 Starting API...[/green]")
    api_process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app"]
    )
    time.sleep(3)


# -----------------------------
# STEP 2: RUN DETECTION
# -----------------------------
console.print("[bold blue]🎥 Processing Cameras...[/bold blue]")

subprocess.run([sys.executable, "pipeline/detect.py"])

console.print("[green]✅ Detection completed[/green]")

# wait for events to be processed
time.sleep(2)

# -----------------------------
# STEP 3: FETCH DATA
# -----------------------------
def fetch(url):
    return requests.get(url).json()


metrics = fetch("http://127.0.0.1:8000/stores/STORE_001/metrics")
funnel = fetch("http://127.0.0.1:8000/stores/STORE_001/funnel")
anomalies = fetch("http://127.0.0.1:8000/stores/STORE_001/anomalies")

# -----------------------------
# STEP 4: DISPLAY FINAL DASHBOARD
# -----------------------------
console.print("\n[bold yellow]📊 FINAL RESULTS[/bold yellow]\n")

table = Table(title="Store Metrics")
table.add_column("Metric")
table.add_column("Value")

table.add_row("Total Visitors", str(metrics.get("total_visitors")))
table.add_row("Conversion Rate", str(metrics.get("conversion_rate")))

console.print(table)

funnel_table = Table(title="Funnel")
funnel_table.add_column("Stage")
funnel_table.add_column("Count")

funnel_table.add_row("Entry", str(funnel.get("entry")))
funnel_table.add_row("Zone Visit", str(funnel.get("zone_visit")))
funnel_table.add_row("Billing", str(funnel.get("billing")))
funnel_table.add_row("Purchase", str(funnel.get("purchase")))

console.print(funnel_table)

console.print("\n⚠️ Anomalies:")
if anomalies:
    for a in anomalies:
        console.print(f"- {a['type']}: {a['message']}")
else:
    console.print("No anomalies detected")

# -----------------------------
# STEP 5: STOP API
# -----------------------------
if api_process is not None:
    api_process.terminate()
    console.print("\n[red]🛑 API stopped[/red]")