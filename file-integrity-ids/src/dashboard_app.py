import re
from collections import Counter
from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Host Security Dashboard",
    page_icon="🛡️",
    layout="wide"
)

project_folder = Path(__file__).resolve().parent.parent
alerts_file = project_folder / "reports" / "alerts.log"

alert_pattern = re.compile(
    r"^\[(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\]\s+"
    r"\[(\w+)\]\s+(.*)$"
)


def load_alerts():
    alerts = []

    if not alerts_file.exists():
        return alerts

    with open(alerts_file, "r", encoding="utf-8") as file:
        for line in file:
            match = alert_pattern.match(line.strip())

            if match:
                timestamp = match.group(1)
                alerts.append({
                    "timestamp": timestamp,
                    "date": timestamp[:10],
                    "severity": match.group(2).upper(),
                    "message": match.group(3)
                })

    return alerts


st.title("🛡️ Host Security Dashboard")
st.caption("File integrity and login activity from your local project")

if st.sidebar.button("Refresh alerts"):
    st.rerun()

st.sidebar.caption("Alert source: reports/alerts.log")
alerts = load_alerts()

if not alerts:
    st.info(
        "No timestamped alerts found yet. Run the file monitor or log analyzer, "
        "then refresh this dashboard."
    )

severity_counts = Counter(alert["severity"] for alert in alerts)

metric_columns = st.columns(4)
metric_columns[0].metric("Total alerts", len(alerts))
metric_columns[1].metric("Critical", severity_counts["CRITICAL"])
metric_columns[2].metric("High", severity_counts["HIGH"])
metric_columns[3].metric("Medium", severity_counts["MEDIUM"])

st.divider()

left_column, right_column = st.columns([1, 2])

with left_column:
    st.subheader("Alerts by day")

    daily_counts = Counter(alert["date"] for alert in alerts)

    if daily_counts:
        daily_rows = [
            {"Date": day, "Alerts": count}
            for day, count in sorted(daily_counts.items())[-7:]
        ]

        daily_data = pd.DataFrame(daily_rows).set_index("Date")
        st.bar_chart(daily_data, height=300)
    else:
        st.write("Daily alert counts will appear here.")

with right_column:
    st.subheader("Recent alerts")

    severities = sorted({alert["severity"] for alert in alerts})
    filter_options = ["All"] + severities
    selected_severity = st.selectbox("Filter by severity", filter_options)

    if selected_severity == "All":
        visible_alerts = alerts
    else:
        visible_alerts = [
            alert for alert in alerts
            if alert["severity"] == selected_severity
        ]

    visible_alerts = sorted(
        visible_alerts,
        key=lambda alert: alert["timestamp"],
        reverse=True
    )

    if visible_alerts:
        table_data = [
            {
                "Time": alert["timestamp"].replace("T", " "),
                "Severity": alert["severity"],
                "Alert": alert["message"]
            }
            for alert in visible_alerts
        ]

        st.dataframe(
            pd.DataFrame(table_data),
            width="stretch",
            hide_index=True
        )
    else:
        st.write("No alerts match this filter.")