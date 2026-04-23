from rich.console import Console
from rich.table import Table
import requests

console = Console()

API_URL = "http://127.0.0.1:8000"


def fetch_metrics():
    return requests.get(f"{API_URL}/stores/STORE_001/metrics").json()


def fetch_funnel():
    return requests.get(f"{API_URL}/stores/STORE_001/funnel").json()


def fetch_anomalies():
    return requests.get(f"{API_URL}/stores/STORE_001/anomalies").json()


def display_dashboard():
    console.clear()

    metrics = fetch_metrics()
    funnel = fetch_funnel()
    anomalies = fetch_anomalies()

    # Metrics
    table = Table(title="📊 Store Metrics")
    table.add_column("Metric")
    table.add_column("Value")

    table.add_row("Total Visitors", str(metrics.get("total_visitors")))
    table.add_row("Conversion Rate", str(metrics.get("conversion_rate")))

    console.print(table)

    # Funnel
    funnel_table = Table(title="🔄 Funnel")
    funnel_table.add_column("Stage")
    funnel_table.add_column("Count")

    funnel_table.add_row("Entry", str(funnel.get("entry")))
    funnel_table.add_row("Zone Visit", str(funnel.get("zone_visit")))
    funnel_table.add_row("Billing", str(funnel.get("billing")))
    funnel_table.add_row("Purchase", str(funnel.get("purchase")))

    console.print(funnel_table)

    # Anomalies
    console.print("\n⚠️ Anomalies:")
    if anomalies:
        for a in anomalies:
            console.print(f"- {a['type']}: {a['message']}")
    else:
        console.print("No anomalies detected")


if __name__ == "__main__":
    display_dashboard()